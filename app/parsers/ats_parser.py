import json
from pathlib import Path

from app.models.candidate import (
    CandidateFragment,
    Confidence,
    Email,
    FieldValue,
    Phone,
    Provenance,
    Skill,
    SourceType,
)
from app.parsers.base_parser import BaseParser


class ATSJSONParser(BaseParser):
    def parse(self, file_path: Path) -> CandidateFragment:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        fragment = CandidateFragment(
            source=SourceType.ATS_JSON,
            source_file=file_path.name,
            candidate_id=data.get("candidateId"),
            raw_payload=data,
        )

        if data.get("candidateName"):
            fragment.full_name = FieldValue(
                value=data["candidateName"],
                confidence=Confidence(score=0.95, reason="Structured ATS candidateName"),
                provenance=[
                    Provenance(
                        source=SourceType.ATS_JSON,
                        source_file=file_path.name,
                        field_path="candidateName",
                        extraction_method="json_field_mapping",
                        raw_value=data["candidateName"],
                    )
                ],
            )

        if data.get("mail"):
            fragment.emails.append(
                Email(
                    value=data["mail"],
                    confidence=Confidence(score=0.97, reason="Structured ATS email"),
                    provenance=[
                        Provenance(
                            source=SourceType.ATS_JSON,
                            source_file=file_path.name,
                            field_path="mail",
                            extraction_method="json_field_mapping",
                            raw_value=data["mail"],
                        )
                    ],
                )
            )

        if data.get("mobile"):
            fragment.phones.append(
                Phone(
                    value=data["mobile"],
                    confidence=Confidence(score=0.88, reason="Structured ATS mobile"),
                    provenance=[
                        Provenance(
                            source=SourceType.ATS_JSON,
                            source_file=file_path.name,
                            field_path="mobile",
                            extraction_method="json_field_mapping",
                            raw_value=data["mobile"],
                        )
                    ],
                )
            )

        if data.get("company"):
            fragment.current_company = FieldValue(
                value=data["company"],
                confidence=Confidence(score=0.88, reason="Structured ATS company"),
                provenance=[
                    Provenance(
                        source=SourceType.ATS_JSON,
                        source_file=file_path.name,
                        field_path="company",
                        extraction_method="json_field_mapping",
                        raw_value=data["company"],
                    )
                ],
            )

        if data.get("jobTitle"):
            fragment.current_title = FieldValue(
                value=data["jobTitle"],
                confidence=Confidence(score=0.88, reason="Structured ATS jobTitle"),
                provenance=[
                    Provenance(
                        source=SourceType.ATS_JSON,
                        source_file=file_path.name,
                        field_path="jobTitle",
                        extraction_method="json_field_mapping",
                        raw_value=data["jobTitle"],
                    )
                ],
            )

        skills_text = data.get("skillsText")
        if skills_text:
            skills = [skill.strip() for skill in skills_text.split(",") if skill.strip()]

            for skill in skills:
                fragment.skills.append(
                    Skill(
                        value=skill,
                        confidence=Confidence(score=0.9, reason="Extracted from ATS skillsText"),
                        provenance=[
                            Provenance(
                                source=SourceType.ATS_JSON,
                                source_file=file_path.name,
                                field_path="skillsText",
                                extraction_method="comma_split",
                                raw_value=skills_text,
                            )
                        ],
                    )
                )

        return fragment