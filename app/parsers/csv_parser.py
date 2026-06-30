from pathlib import Path

import pandas as pd

from app.models.candidate import (
    CandidateFragment,
    Confidence,
    Email,
    FieldValue,
    Phone,
    Provenance,
    SourceType,
)
from app.parsers.base_parser import BaseParser


class RecruiterCSVParser(BaseParser):
    def parse(self, file_path: Path) -> CandidateFragment:
        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError(f"CSV file is empty: {file_path}")

        row = df.iloc[0].to_dict()

        candidate_id = row.get("candidate_id")
        name = row.get("name")
        email = row.get("email")
        phone = row.get("phone")
        company = row.get("current_company")
        title = row.get("title")

        fragment = CandidateFragment(
            source=SourceType.RECRUITER_CSV,
            source_file=file_path.name,
            candidate_id=candidate_id,
            raw_payload=row,
        )

        if name:
            fragment.full_name = FieldValue(
                value=name,
                confidence=Confidence(score=0.98, reason="Structured recruiter CSV name"),
                provenance=[
                    Provenance(
                        source=SourceType.RECRUITER_CSV,
                        source_file=file_path.name,
                        field_path="name",
                        extraction_method="csv_column_mapping",
                        raw_value=name,
                    )
                ],
            )

        if email:
            fragment.emails.append(
                Email(
                    value=email,
                    confidence=Confidence(score=0.99, reason="Structured recruiter CSV email"),
                    provenance=[
                        Provenance(
                            source=SourceType.RECRUITER_CSV,
                            source_file=file_path.name,
                            field_path="email",
                            extraction_method="csv_column_mapping",
                            raw_value=email,
                        )
                    ],
                )
            )

        if phone:
            fragment.phones.append(
                Phone(
                    value=phone,
                    confidence=Confidence(score=0.9, reason="Structured recruiter CSV phone"),
                    provenance=[
                        Provenance(
                            source=SourceType.RECRUITER_CSV,
                            source_file=file_path.name,
                            field_path="phone",
                            extraction_method="csv_column_mapping",
                            raw_value=phone,
                        )
                    ],
                )
            )

        if company:
            fragment.current_company = FieldValue(
                value=company,
                confidence=Confidence(score=0.92, reason="Structured recruiter CSV company"),
                provenance=[
                    Provenance(
                        source=SourceType.RECRUITER_CSV,
                        source_file=file_path.name,
                        field_path="current_company",
                        extraction_method="csv_column_mapping",
                        raw_value=company,
                    )
                ],
            )

        if title:
            fragment.current_title = FieldValue(
                value=title,
                confidence=Confidence(score=0.92, reason="Structured recruiter CSV title"),
                provenance=[
                    Provenance(
                        source=SourceType.RECRUITER_CSV,
                        source_file=file_path.name,
                        field_path="title",
                        extraction_method="csv_column_mapping",
                        raw_value=title,
                    )
                ],
            )

        return fragment