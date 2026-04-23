from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from app.database import users_collection, attendance_collection
from app.dependencies.auth import get_current_user
from fastapi.responses import FileResponse
import numpy as np
import cv2
import pandas as pd
from datetime import datetime, date

router = APIRouter(prefix="/attendance", tags=["Attendance"])


# ==============================
# 🔵 PUNCH IN / OUT
# ==============================
@router.post("/punch")
async def punch(
    file: UploadFile = File(...),
    lat: float = Form(...),
    lng: float = Form(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        email = current_user["email"]

        user = users_collection.find_one({"email": email})

        if not user:
            raise HTTPException(404, "User not found")

        if user.get("is_active") is False:
            raise HTTPException(403, "User disabled")

        # 📸 Read image
        contents = await file.read()
        np_arr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(400, "Invalid image")

        # 🧠 Face detection
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 6, minSize=(50, 50))

        if len(faces) == 0:
            raise HTTPException(400, "No face detected")

        today = str(date.today())

        record = attendance_collection.find_one({
            "email": email,
            "date": today
        })

        # 🟢 PUNCH IN
        if not record:
            attendance_collection.insert_one({
                "email": email,
                "date": today,
                "in_time": datetime.now(),
                "out_time": None,
                "hours": 0,
                "status": "In Progress",
                "location": {"lat": lat, "lng": lng},

                "overtime_requested": False,
                "overtime_status": None,
                "overtime_eligible": False,

                "is_fake": False
            })

            return {"msg": "Punch IN successful"}

        # 🔵 PUNCH OUT
        if record["out_time"] is None:
            in_time = record["in_time"]
            out_time = datetime.now()

            hours = (out_time - in_time).total_seconds() / 3600

            # 🎯 FINAL LOGIC
            if hours > 8:
                status = "Present"
                overtime_flag = True
            elif hours >= 8:
                status = "Present"
                overtime_flag = False
            elif hours >= 4:
                status = "Half Day"
                overtime_flag = False
            else:
                status = "Incomplete"
                overtime_flag = False

            attendance_collection.update_one(
                {"_id": record["_id"]},
                {
                    "$set": {
                        "out_time": out_time,
                        "hours": round(hours, 2),
                        "status": status,
                        "overtime_eligible": overtime_flag,
                        "location": {"lat": lat, "lng": lng}
                    }
                }
            )

            return {
                "msg": "Punch OUT successful",
                "working_hours": round(hours, 2),
                "status": status,
                "overtime_eligible": overtime_flag
            }

        return {
            "msg": "Attendance already completed",
            "working_hours": record.get("hours", 0),
            "status": record.get("status", "")
        }

    except Exception as e:
        raise HTTPException(500, str(e))


# ==============================
# 🟢 EMPLOYEE → OWN DATA
# ==============================
@router.get("/records")
def get_records(current_user: dict = Depends(get_current_user)):
    email = current_user["email"]

    data = list(attendance_collection.find({"email": email}))

    for d in data:
        d["_id"] = str(d["_id"])

    return data


# ==============================
# 🔴 ADMIN → ALL DATA
# ==============================
@router.get("/all")
def get_all(current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(403, "Admin only")

    data = list(attendance_collection.find())

    for d in data:
        d["_id"] = str(d["_id"])

    return data


# ==============================
# 🟡 FILTER
# ==============================
@router.get("/filter")
def filter_data(
    user_email: str = None,
    date_filter: str = None,
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(403, "Admin only")

    query = {}

    if user_email:
        query["email"] = user_email

    if date_filter:
        query["date"] = date_filter

    data = list(attendance_collection.find(query))

    for d in data:
        d["_id"] = str(d["_id"])

    return data


# ==============================
# 🔴 MARK FAKE
# ==============================
@router.post("/mark-fake")
def mark_fake(record_id: str, current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(403, "Admin only")

    from bson import ObjectId

    attendance_collection.update_one(
        {"_id": ObjectId(record_id)},
        {"$set": {"is_fake": True}}
    )

    return {"msg": "Marked as fake"}


# ==============================
# ⚫ DISABLE USER
# ==============================
@router.post("/disable-user")
def disable_user(target_email: str, current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(403, "Admin only")

    users_collection.update_one(
        {"email": target_email},
        {"$set": {"is_active": False}}
    )

    return {"msg": "User disabled"}


# ==============================
# 🟡 OVERTIME WORKFLOW
# ==============================
@router.post("/request-ot")
def request_ot(current_user: dict = Depends(get_current_user)):

    email = current_user["email"]
    today = str(date.today())

    record = attendance_collection.find_one({
        "email": email,
        "date": today
    })

    if record.get("hours", 0) <= 8:
        raise HTTPException(400, "Only >8 hrs allowed")

    attendance_collection.update_one(
        {"_id": record["_id"]},
        {"$set": {"overtime_requested": True, "overtime_status": "Pending"}}
    )

    return {"msg": "OT requested"}


@router.get("/overtime-requests")
def view_ot(current_user: dict = Depends(get_current_user)):

    if current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(403, "Access denied")

    data = list(attendance_collection.find({"overtime_requested": True}))

    for d in data:
        d["_id"] = str(d["_id"])

    return data


@router.post("/overtime-action")
def ot_action(
    decision: str,
    target_email: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(403, "Access denied")

    today = str(date.today())

    attendance_collection.update_one(
        {"email": target_email, "date": today},
        {"$set": {"overtime_status": decision}}
    )

    return {"msg": f"{decision}"}


# ==============================
# 🟣 MANAGER → TEAM DATA
# ==============================
@router.get("/team")
def team_data(current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "manager":
        raise HTTPException(403, "Manager only")

    team = list(users_collection.find({"manager": current_user["email"]}))
    emails = [t["email"] for t in team]

    data = list(attendance_collection.find({"email": {"$in": emails}}))

    for d in data:
        d["_id"] = str(d["_id"])

    return data


# ==============================
# 🟢 EXPORT EXCEL
# ==============================
@router.get("/export")
def export_excel(current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(403, "Admin only")

    data = list(attendance_collection.find())

    for d in data:
        d["_id"] = str(d["_id"])

    df = pd.DataFrame(data)

    file_path = "attendance.xlsx"
    df.to_excel(file_path, index=False)

    return FileResponse(file_path, filename="attendance.xlsx")