from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ai


# import routers
from app.routes import auth, face, attendance

# create app
app = FastAPI()

# ✅ CORS (VERY IMPORTANT for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ include routers
app.include_router(auth.router)
app.include_router(face.router)
app.include_router(attendance.router)
app.include_router(ai.router)

# ✅ root route
@app.get("/")
def root():
    return {"message": "AI Attendance System Running"}