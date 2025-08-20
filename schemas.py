# schemas.py
from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel, Field

PitchType = Literal[
    "Four-Seam Fastball", "Two-Seam Fastball", "Sinker", "Cutter",
    "Slider", "Curveball", "Changeup", "Splitter", "Sweeper", "Other"
]

class PitchingInput(BaseModel):
    velocity: float = Field(..., description="mph")
    total_spin: Optional[float] = Field(None, description="rpm")
    pitch_type: PitchType
    true_spin_rate: Optional[float] = Field(None, description="rpm (true spin)")
    spin_direction: Optional[float] = Field(None, ge=0, le=360, description="degrees (0-360)")
    gyro_degree: Optional[float] = Field(None, ge=0, le=90, description="degrees")
    spin_efficiency: Optional[float] = Field(None, ge=0, le=100, description="%")
    release_height: Optional[float] = Field(None, description="ft")
    horizontal_break: Optional[float] = Field(None, description="inches (+ to arm-side)")
    vertical_break: Optional[float] = Field(None, description="inches (+ 'ride')")

class HittingInput(BaseModel):
    exit_velocity: float = Field(..., description="mph")
    distance: float = Field(..., description="ft")
    launch_angle: float = Field(..., description="degrees")
    exit_direction: Optional[float] = Field(None, description="degrees (pull -/+)")
    total_spin: Optional[float] = Field(None, description="rpm")
    spin_direction: Optional[float] = Field(None, description="degrees")

class LessonDrill(BaseModel):
    title: str
    why: str
    steps: List[str]

class LessonResponse(BaseModel):
    mode: Literal["pitching", "hitting"]
    summary: str
    priorities: List[str]
    drills: List[LessonDrill]
    metric_flags: Dict[str, Dict[str, Any]]
