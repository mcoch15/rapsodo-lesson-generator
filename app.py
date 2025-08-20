# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import PitchingInput, HittingInput, LessonResponse
from rules import generate_pitching_lesson, generate_hitting_lesson
from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="/docs", status_code=302)

import os

app = FastAPI(title="Rapsodo Lesson Generator")  # <-- must be named 'app'

allowed = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed if allowed != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/lesson/pitching", response_model=LessonResponse)
def lesson_pitching(payload: PitchingInput):
    try:
        return generate_pitching_lesson(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/lesson/hitting", response_model=LessonResponse)
def lesson_hitting(payload: HittingInput):
    try:
        return generate_hitting_lesson(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


