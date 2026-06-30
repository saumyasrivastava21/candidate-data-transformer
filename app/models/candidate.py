from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator


class SourceType(str, Enum):
    RECRUITER_CSV = "recruiter_csv"
    ATS_JSON = "ats_json"
    RESUME_PDF = "resume_pdf"
    GITHUB = "github"
    LINKEDIN = "linkedin"
    NOTES = "notes"


class Provenance(BaseModel):
    source: SourceType
    source_file: Optional[str] = None
    field_path: Optional[str] = None
    extraction_method: str = "manual_or_parser"
    raw_value: Optional[Any] = None


class Confidence(BaseModel):
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    reason: Optional[str] = None


class FieldValue(BaseModel):
    value: Any
    confidence: Confidence = Field(default_factory=Confidence)
    provenance: List[Provenance] = Field(default_factory=list)


class Email(FieldValue):
    value: str

    @field_validator("value")
    @classmethod
    def validate_email_basic(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email format")
        return value


class Phone(FieldValue):
    value: str

    @field_validator("value")
    @classmethod
    def validate_phone_basic(cls, value: str) -> str:
        value = value.strip()
        cleaned = value.replace(" ", "").replace("-", "")
        if not cleaned.startswith("+"):
            cleaned = "+" + cleaned
        if len(cleaned) < 8:
            raise ValueError("Invalid phone number")
        return cleaned


class Skill(FieldValue):
    value: str

    @field_validator("value")
    @classmethod
    def normalize_skill_text(cls, value: str) -> str:
        return value.strip()


class Experience(BaseModel):
    company: Optional[FieldValue] = None
    title: Optional[FieldValue] = None
    start_date: Optional[FieldValue] = None
    end_date: Optional[FieldValue] = None
    description: Optional[FieldValue] = None


class Education(BaseModel):
    institution: Optional[FieldValue] = None
    degree: Optional[FieldValue] = None
    start_year: Optional[FieldValue] = None
    end_year: Optional[FieldValue] = None


class Links(BaseModel):
    github: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None
    portfolio: Optional[HttpUrl] = None


class CandidateFragment(BaseModel):
    """
    Intermediate parser output.

    Every parser converts raw source data into CandidateFragment.
    Later phases will normalize and merge multiple fragments into CandidateProfile.
    """

    source: SourceType
    source_file: Optional[str] = None

    candidate_id: Optional[str] = None
    full_name: Optional[FieldValue] = None
    emails: List[Email] = Field(default_factory=list)
    phones: List[Phone] = Field(default_factory=list)

    current_company: Optional[FieldValue] = None
    current_title: Optional[FieldValue] = None
    skills: List[Skill] = Field(default_factory=list)

    raw_payload: Dict[str, Any] = Field(default_factory=dict)


class CandidateProfile(BaseModel):
    candidate_id: Optional[str] = None

    full_name: Optional[FieldValue] = None
    emails: List[Email] = Field(default_factory=list)
    phones: List[Phone] = Field(default_factory=list)

    current_company: Optional[FieldValue] = None
    current_title: Optional[FieldValue] = None

    skills: List[Skill] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)

    links: Links = Field(default_factory=Links)

    global_confidence: Confidence = Field(default_factory=Confidence)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_at_least_identity(self):
        if not self.full_name and not self.emails and not self.phones:
            raise ValueError("Candidate must have at least name, email, or phone")
        return self

    def to_clean_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)