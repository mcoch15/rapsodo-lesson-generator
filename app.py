from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from schemas import PitchingInput, HittingInput, LessonResponse
from rules import generate_pitching_lesson, generate_hitting_lesson
import os

# must come first
app = FastAPI(title="Rapsodo Lesson Generator")

allowed = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed if allowed != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 routes can only come AFTER app is defined
@app.get("/", include_in_schema=False)
def root():
    return {"message": "Rapsodo Lesson Generator is running. See /docs"}

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/lesson/pitching", response_model=LessonResponse)
def lesson_pitching(payload: PitchingInput):
    return generate_pitching_lesson(payload)

@app.post("/lesson/hitting", response_model=LessonResponse)
def lesson_hitting(payload: HittingInput):
    return generate_hitting_lesson(payload)
