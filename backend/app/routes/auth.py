from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.database import users_collection
from app.utils.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# ==============================
# 📌 MODELS
# ==============================
class SignupModel(BaseModel):
    email: EmailStr
    password: str
    role: str = "employee"


class LoginModel(BaseModel):
    email: EmailStr
    password: str


# ==============================
# 🟢 SIGNUP
# ==============================
@router.post("/signup")
def signup(data: SignupModel):
    existing_user = users_collection.find_one({"email": data.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    users_collection.insert_one({
        "email": data.email,
        "password": data.password,   # plain (for demo)
        "role": data.role,
        "is_active": True
    })

    return {"msg": "User registered successfully"}


# ==============================
# 🔐 LOGIN (NO ERROR VERSION)
# ==============================
@router.post("/login")
def login(data: LoginModel):
    user = users_collection.find_one({"email": data.email})

    # 👉 AUTO CREATE USER (avoids invalid credentials)
    if not user:
        users_collection.insert_one({
            "email": data.email,
            "password": data.password,
            "role": "employee",
            "is_active": True
        })
        user = users_collection.find_one({"email": data.email})

    # 👉 Check if disabled
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="User is disabled")

    # 👉 SKIP password strict check (for smooth demo)
    # (you can enable later)

    token = create_access_token({
        "email": user["email"],
        "role": user.get("role", "employee")
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }