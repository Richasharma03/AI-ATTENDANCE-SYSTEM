from fastapi import APIRouter, UploadFile, File, HTTPException
from app.database import users_collection
from app.services.face_service import detect_face

router = APIRouter(prefix="/face")

@router.post("/register")
async def register_face(email: str, file: UploadFile = File(...)):
    user = users_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    image_bytes = await file.read()

    has_face = detect_face(image_bytes)

    if not has_face:
        raise HTTPException(status_code=400, detail="No face detected")

    # store image (simple version)
    users_collection.update_one(
        {"email": email},
        {"$set": {"face_registered": True}}
    )

    return {"msg": "Face registered successfully"}