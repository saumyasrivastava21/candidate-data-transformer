from app.models.candidate import (
    CandidateFragment,
    CandidateProfile,
    Confidence,
    Email,
    FieldValue,
    Phone,
    Skill,
    SourceType,
)
from app.normalizers.email_normalizer import normalize_email
from app.normalizers.phone_normalizer import normalize_phone
from app.normalizers.skill_normalizer import normalize_skill
from app.services.merge_service import MergeService
from app.services.normalization_service import NormalizationService
from app.services.parser_service import ParserService
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


def test_candidate_fragment_model():
    fragment = CandidateFragment(
        source=SourceType.RECRUITER_CSV,
        source_file="recruiter.csv",
        full_name=FieldValue(value="Saumya Srivastava"),
        emails=[Email(value="saumya@example.com")],
    )

    assert fragment.source == SourceType.RECRUITER_CSV
    assert fragment.full_name.value == "Saumya Srivastava"


def test_parser_service_parses_inputs():
    service = ParserService()
    fragments = service.parse_input_directory(INPUT_DIR)

    assert len(fragments) == 3

    sources = [fragment.source for fragment in fragments]

    assert SourceType.RECRUITER_CSV in sources
    assert SourceType.ATS_JSON in sources
    assert SourceType.NOTES in sources


def test_phone_normalization_indian_number():
    assert normalize_phone("9876543210") == "+919876543210"
    assert normalize_phone("+91 9876543210") == "+919876543210"


def test_email_normalization():
    assert normalize_email("SAUMYA@Example.COM ") == "saumya@example.com"


def test_skill_normalization():
    assert normalize_skill("springboot") == "Spring Boot"
    assert normalize_skill("ml") == "Machine Learning"


def test_normalization_service_only_normalizes_fragments():
    parser_service = ParserService()
    normalization_service = NormalizationService()

    fragments = parser_service.parse_input_directory(INPUT_DIR)
    normalized_fragments = normalization_service.normalize_fragments(fragments)

    all_phones = []
    for fragment in normalized_fragments:
        all_phones.extend([phone.value for phone in fragment.phones])

    assert "+919876543210" in all_phones


def test_merge_service_deduplicates_phone_and_skills():
    parser_service = ParserService()
    normalization_service = NormalizationService()
    merge_service = MergeService()

    fragments = parser_service.parse_input_directory(INPUT_DIR)
    normalized_fragments = normalization_service.normalize_fragments(fragments)
    candidate = merge_service.merge_fragments(normalized_fragments)

    assert len(candidate.phones) == 1
    assert candidate.phones[0].value == "+919876543210"

    skill_names = [skill.value for skill in candidate.skills]

    assert "Spring Boot" in skill_names
    assert len(skill_names) == len(set(skill_names))


def test_merge_service_selects_highest_confidence_name():
    low = CandidateFragment(
        source=SourceType.NOTES,
        source_file="notes.txt",
        full_name=FieldValue(
            value="S. Srivastava",
            confidence=Confidence(score=0.5),
        ),
    )

    high = CandidateFragment(
        source=SourceType.RECRUITER_CSV,
        source_file="recruiter.csv",
        full_name=FieldValue(
            value="Saumya Srivastava",
            confidence=Confidence(score=0.98),
        ),
    )

    merge_service = MergeService()
    candidate = merge_service.merge_fragments([low, high])

    assert candidate.full_name.value == "Saumya Srivastava"