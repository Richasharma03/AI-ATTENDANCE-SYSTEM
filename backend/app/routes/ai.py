from fastapi import APIRouter, HTTPException, Depends
from app.database import attendance_collection
from app.dependencies.auth import get_current_user
from openai import OpenAI
import os
from dotenv import load_dotenv

router = APIRouter(prefix="/ai", tags=["AI"])

load_dotenv()

# ✅ Correct key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@router.post("/query")
async def ai_query(query: str, current_user: dict = Depends(get_current_user)):
    try:
        data = list(attendance_collection.find())

        for d in data:
            d["_id"] = str(d["_id"])

        prompt = f"""
You are an AI Attendance Assistant.

Analyze the following attendance data and answer clearly.

Rules:
- Be short and clear
- Focus only on relevant data
- If no data found, say "No records found"

Attendance Data:
{data}

User Question:
{query}
"""

        # ✅ OpenAI direct call (FIXED)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        return {"answer": answer}

    except Exception as e:
        print("AI ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))