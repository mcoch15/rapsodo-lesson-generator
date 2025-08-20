# rules.py
from typing import Dict, List, Tuple
from schemas import PitchingInput, HittingInput, LessonResponse, LessonDrill

def _flag(name: str, value, target: str, note: str):
    return name, {"value": value, "target": target, "note": note, "flag": True}

def generate_pitching_lesson(p: PitchingInput) -> LessonResponse:
    flags: Dict[str, Dict] = {}
    priorities: List[str] = []
    drills: List[LessonDrill] = []

    # --- Baseline heuristics (adjust as needed) ---
    # 1) Fastball spin efficiency
    if "Fastball" in p.pitch_type or p.pitch_type == "Four-Seam Fastball":
        if p.spin_efficiency is not None and p.spin_efficiency < 90:
            k, v = _flag(
                "Spin Efficiency",
                p.spin_efficiency,
                "≥ 90% for 4S FB (tune for level)",
                "Below typical 4S efficiency—likely bleeding ride/carry."
            )
            flags[k] = v
            priorities.append("Improve 4S spin efficiency to boost carry/ride.")
            drills.append(LessonDrill(
                title="Clean 4-Seam Spin (Plyo/Grip Focus)",
                why="Efficient backspin helps vertical break and perceived rise.",
                steps=[
                    "Use 4S grip with seams true; cue 'through the ball'.",
                    "Plyo wall: focus on true backspin (no cut/run).",
                    "Grip experiment: pressure on index/middle, relaxed thumb.",
                    "Video the ball axis; compare to Rapsodo spin axis."
                ]
            ))

    # 2) Gyro on fastball
    if ("Fastball" in p.pitch_type) and p.gyro_degree is not None and p.gyro_degree > 20:
        k, v = _flag(
            "Gyro Degree",
            p.gyro_degree,
            "≤ 15–20° for 4S FB (tune)",
            "Too much gyro dilutes backspin and carry."
        )
        flags[k] = v
        if "Improve 4S spin efficiency to boost carry/ride." not in priorities:
            priorities.append("Reduce gyro on fastball to increase carry.")
        drills.append(LessonDrill(
            title="Axis Awareness Towel Drill",
            why="Reduces bullet-spin by reinforcing fingers-behind-ball release.",
            steps=[
                "Use towel drill emphasizing palm-to-target finish.",
                "Cue: 'Show the logo to the sky' through release.",
                "Short box throws; check Rapsodo gyro drop across reps."
            ]
        ))

    # 3) Sliders/cutters should NOT be too efficient
    if p.pitch_type in ("Slider", "Cutter") and p.spin_efficiency is not None and p.spin_efficiency > 40:
        k, v = _flag(
            "Spin Efficiency",
            p.spin_efficiency,
            "≤ ~35–40% for tight SL/CT (tune)",
            "Slider/cutter reading very efficient—likely backing up."
        )
        flags[k] = v
        priorities.append("Add gyro/sweep characteristics to breaking ball.")
        drills.append(LessonDrill(
            title="Bullet-Spin Builder (Slider)",
            why="Increases gyro to tighten tilt and reduce unintended backspin.",
            steps=[
                "Grip: offset fingers; cue 'door-knob' (supinate) late.",
                "Short spin throws to 45–60 ft focusing on tilt.",
                "Blend to full distance; keep velocity intent."
            ]
        ))

    # 4) Movement profile sanity checks (very general)
    if p.vertical_break is not None and "Fastball" in p.pitch_type and p.vertical_break < 10:
        k, v = _flag(
            "Vertical Break",
            p.vertical_break,
            "≈ 14–18 in ride for 4S (tune per velo/slot)",
            "Low ride may reduce swing-miss at top of zone."
        )
        flags[k] = v
        priorities.append("Increase ride on 4S to create top-of-zone margin.")
    if p.horizontal_break is not None and p.pitch_type in ("Two-Seam Fastball", "Sinker") and abs(p.horizontal_break) < 10:
        k, v = _flag(
            "Horizontal Break",
            p.horizontal_break,
            "≈ 12–18 in arm-side run (tune)",
            "Arm-side run is modest for a sinker profile."
        )
        flags[k] = v
        priorities.append("Enhance arm-side run on sinker/two-seam.")

    summary = "Focus on a cleaner spin axis and movement profile to amplify separation and miss barrels."
    if not priorities:
        priorities = ["Current metrics look balanced. Maintain patterns and build velocity safely."]
        summary = "Solid foundation—keep patterning. Layer intent and command work."

    return LessonResponse(
        mode="pitching",
        summary=summary,
        priorities=list(dict.fromkeys(priorities)),
        drills=drills[:3] or [LessonDrill(
            title="Baseline Patterning",
            why="Locks in current axis & release cues.",
            steps=[
                "Catch play with intent ladders (60→90→120 ft).",
                "5–10 plyo spins per pitch type; monitor axis.",
                "Finish with 8–12 pulldowns tracking spin metrics."
            ]
        )],
        metric_flags=flags
    )

def generate_hitting_lesson(h: HittingInput) -> LessonResponse:
    flags: Dict[str, Dict] = {}
    priorities: List[str] = []
    drills: List[LessonDrill] = []

    # 1) Launch angle shape
    if h.launch_angle > 35:
        k, v = _flag("Launch Angle", h.launch_angle, "Optimal band ≈ 10–30°", "Steep LA can produce pop-ups.")
        flags[k] = v
        priorities.append("Shallow the attack angle to stay through the zone.")
        drills.append(LessonDrill(
            title="High-Tee (Top-Half Contact)",
            why="Flattens entry; reduces undercut.",
            steps=[
                "Tee above belt; target hard line drives to CF.",
                "Cue: 'Match plane, not lift.'",
                "10× reps, then live flips; track LA on Rapsodo."
            ]
        ))
    elif h.launch_angle < 5:
        k, v = _flag("Launch Angle", h.launch_angle, "Optimal band ≈ 10–30°", "Flat LA drives balls into the ground.")
        flags[k] = v
        priorities.append("Increase attack angle and contact point lift.")
        drills.append(LessonDrill(
            title="Low-Tee Opposite Gap",
            why="Encourages upward path without collapsing backside.",
            steps=[
                "Tee below belt; aim oppo gap line drives (10–20°).",
                "Cue: 'Knob to inside bottom of ball.'",
                "Progress to flips; confirm LA shift."
            ]
        ))

    # 2) Exit velocity floor
    if h.exit_velocity < 80:
        k, v = _flag("Exit Velocity", h.exit_velocity, "Build toward ≥ 85–90 mph (level-dependent)", "Limited ball speed caps damage on contact.")
        flags[k] = v
        priorities.append("Improve bat speed and quality of contact.")
        drills.append(LessonDrill(
            title="Over/Under Weighted-Bat Contrast",
            why="Creates intent & bat-speed stimulus.",
            steps=[
                "5 swings +10% bat weight; 5 swings -10%; 5 gamer.",
                "Track EV; rest :45 between sets.",
                "2–3 sets; keep mechanics tight."
            ]
        ))

    # 3) Directional bias
    if h.exit_direction is not None and abs(h.exit_direction) > 25:
        side = "pull" if h.exit_direction < 0 else "opposite"
        k, v = _flag("Exit Direction", h.exit_direction, "Stay mostly within ±20°", f"Strong {side} bias may shrink timing window.")
        flags[k] = v
        priorities.append("Balance direction window (±20°) to unlock timing margin.")
        drills.append(LessonDrill(
            title="3-Cone Direction Ladder",
            why="Trains adjustable point-of-contact across the zone.",
            steps=[
                "Set 3 visual lanes: pull/middle/oppo.",
                "Call lanes randomly; drive line drives to each.",
                "Record direction dispersion over 15–20 swings."
            ]
        ))

    # 4) Distance vs EV quick check (very rough cueing)
    if h.distance < 200 and h.exit_velocity >= 90 and 10 <= h.launch_angle <= 30:
        k, v = _flag("Distance", h.distance, "Expect 250–350 ft w/ 90+ EV & 10–30° LA", "Ball not carrying relative to EV/LA.")
        flags[k] = v
        priorities.append("Optimize contact quality—center strikes and backspin control.")
        drills.append(LessonDrill(
            title="Barrel Centering (Sweet-Spot)",
            why="Centered contact maximizes carry for given EV.",
            steps=[
                "Use spray foot spray or marker on barrel.",
                "10–20 swings focusing on sweet-spot feedback.",
                "Review Rapsodo for carry gains."
            ]
        ))

    summary = "Shape your bat path and timing window to convert ball speed into damage."
    if not priorities:
        priorities = ["Good overall shape—maintain pattern and raise EV ceiling progressively."]
        summary = "Patterns look solid. Keep intent high and build EV safely."

    return LessonResponse(
        mode="hitting",
        summary=summary,
        priorities=list(dict.fromkeys(priorities)),
        drills=drills[:3] or [LessonDrill(
            title="EV Builder + Flight Window",
            why="Pairs speed intent with controlled LA.",
            steps=[
                "5× intent swings; 5× constraint swings (tee at belt).",
                "Alternate lanes CF/LF/RCF with cues.",
                "Track EV & LA; stop if shape degrades."
            ]
        )],
        metric_flags=flags
    )
