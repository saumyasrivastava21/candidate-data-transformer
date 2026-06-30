from app.models.candidate import (
    CandidateProfile,
    Confidence,
    Email,
    FieldValue,
    Phone,
    Skill,
)
from app.settings import CONFIG_DIR, INPUT_DIR, OUTPUT_DIR


def test_directories_exist():
    assert INPUT_DIR.exists()
    assert CONFIG_DIR.exists()
    assert OUTPUT_DIR.exists()


def test_sample_inputs_exist():
    assert (INPUT_DIR / "recruiter.csv").exists()
    assert (INPUT_DIR / "ats.json").exists()
    assert (INPUT_DIR / "notes.txt").exists()


def test_custom_config_exists():
    assert (CONFIG_DIR / "custom_config.json").exists()


def test_candidate_profile_validates():
    candidate = CandidateProfile(
        candidate_id="cand_001",
        full_name=FieldValue(value="Saumya Srivastava"),
        emails=[Email(value="saumya@example.com")],
        phones=[Phone(value="+919876543210")],
        skills=[Skill(value="Python")],
        global_confidence=Confidence(score=0.95),
    )

    assert candidate.candidate_id == "cand_001"
    assert candidate.emails[0].value == "saumya@example.com"
    assert candidate.global_confidence.score == 0.95


def test_email_validation_fails():
    try:
        Email(value="wrong-email")
        assert False
    except ValueError:
        assert True