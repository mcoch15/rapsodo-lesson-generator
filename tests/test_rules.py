from schemas import PitchingInput, HittingInput
from rules import generate_pitching_lesson, generate_hitting_lesson

def test_pitching_fastball_efficiency_flag():
    p = PitchingInput(
        velocity=88, total_spin=2200, pitch_type="Four-Seam Fastball",
        spin_efficiency=82, gyro_degree=25, vertical_break=8, horizontal_break=5
    )
    res = generate_pitching_lesson(p)
    assert res.mode == "pitching"
    assert any("Spin Efficiency" in k for k in res.metric_flags.keys())

def test_hitting_launch_angle_flag():
    h = HittingInput(exit_velocity=84, distance=180, launch_angle=2, exit_direction=10)
    res = generate_hitting_lesson(h)
    assert res.mode == "hitting"
    assert "Launch Angle" in res.metric_flags
