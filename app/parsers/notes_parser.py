from pathlib import Path

from app.models.candidate import (
    CandidateFragment,
    Confidence,
    Provenance,
    Skill,
    SourceType,
)
from app.parsers.base_parser import BaseParser


KNOWN_SKILLS = [
    "Python",
    "Java",
    "Spring Boot",
    "FastAPI",
    "YOLO",
    "Computer Vision",
    "Machine Learning",
    "Deep Learning",
    "Healthcare AI",
    "DSA",
    "React",
    "Docker",
]


class NotesParser(BaseParser):
    def parse(self, file_path: Path) -> CandidateFragment:
        text = file_path.read_text(encoding="utf-8")

        fragment = CandidateFragment(
            source=SourceType.NOTES,
            source_file=file_path.name,
            raw_payload={"text": text},
        )

        lower_text = text.lower()

        for skill in KNOWN_SKILLS:
            if skill.lower() in lower_text:
                fragment.skills.append(
                    Skill(
                        value=skill,
                        confidence=Confidence(score=0.75, reason="Detected keyword in recruiter notes"),
                        provenance=[
                            Provenance(
                                source=SourceType.NOTES,
                                source_file=file_path.name,
                                field_path="text",
                                extraction_method="keyword_match",
                                raw_value=skill,
                            )
                        ],
                    )
                )

        return fragment