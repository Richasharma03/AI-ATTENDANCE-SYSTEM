from fastapi import APIRouter, HTTPException, Depends
from app.database import attendance_collection
from app.dependencies.auth import get_current_user
import requests
import os
from dotenv import load_dotenv

router = APIRouter(prefix="/ai", tags=["AI"])

load_dotenv()


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


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

        # 🌐 Call OpenRouter API
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        result = response.json()

        # ⚠️ Safe handling
        if "choices" not in result:
            return {"answer": "AI error, try again"}

        answer = result["choices"][0]["message"]["content"]

        return {"answer": answer}

    except Exception as e:
        print("AI ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))