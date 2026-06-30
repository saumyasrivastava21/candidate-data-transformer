from typing import Dict, List, Optional

from app.models.candidate import (
    CandidateFragment,
    CandidateProfile,
    Email,
    FieldValue,
    Phone,
    Skill,
)
from app.services.confidence_service import ConfidenceService


class MergeService:
    """
    Merge policy:
    1. Pick candidate_id from first available source.
    2. For scalar fields, choose the value with highest confidence.
    3. For list fields, deduplicate by normalized value.
    4. If duplicates exist, merge provenance and keep highest confidence.
    5. Never invent values.
    """

    def __init__(self):
        self.confidence_service = ConfidenceService()

    def merge_fragments(self, fragments: List[CandidateFragment]) -> CandidateProfile:
        candidate_id = self._pick_first_candidate_id(fragments)

        full_name = self._pick_best_field([f.full_name for f in fragments])
        current_company = self._pick_best_field([f.current_company for f in fragments])
        current_title = self._pick_best_field([f.current_title for f in fragments])

        emails = self._dedupe_emails(fragments)
        phones = self._dedupe_phones(fragments)
        skills = self._dedupe_skills(fragments)

        global_confidence = self.confidence_service.calculate_global_confidence(
            full_name=full_name,
            emails=emails,
            phones=phones,
            skills=skills,
        )

        return CandidateProfile(
            candidate_id=candidate_id,
            full_name=full_name,
            emails=emails,
            phones=phones,
            current_company=current_company,
            current_title=current_title,
            skills=skills,
            global_confidence=global_confidence,
            metadata={
                "status": "phase_4_success",
                "fragments_merged": len(fragments),
                "merge_policy": {
                    "scalar_fields": "highest_confidence_wins",
                    "list_fields": "dedupe_by_normalized_value",
                    "provenance": "merged_from_duplicate_values",
                    "missing_values": "left_null_or_empty",
                },
                "next_phase": "Configurable output projection",
            },
        )

    def _pick_first_candidate_id(self, fragments: List[CandidateFragment]) -> Optional[str]:
        for fragment in fragments:
            if fragment.candidate_id:
                return fragment.candidate_id
        return None

    def _pick_best_field(self, fields: List[Optional[FieldValue]]) -> Optional[FieldValue]:
        valid_fields = [field for field in fields if field and field.value]

        if not valid_fields:
            return None

        return max(valid_fields, key=lambda field: field.confidence.score)

    def _dedupe_emails(self, fragments: List[CandidateFragment]) -> List[Email]:
        email_map: Dict[str, Email] = {}

        for fragment in fragments:
            for email in fragment.emails:
                key = email.value.lower().strip()

                if key not in email_map:
                    email_map[key] = email
                else:
                    existing = email_map[key]
                    existing.provenance.extend(email.provenance)

                    if email.confidence.score > existing.confidence.score:
                        existing.confidence = email.confidence

        return list(email_map.values())

    def _dedupe_phones(self, fragments: List[CandidateFragment]) -> List[Phone]:
        phone_map: Dict[str, Phone] = {}

        for fragment in fragments:
            for phone in fragment.phones:
                key = phone.value.strip()

                if key not in phone_map:
                    phone_map[key] = phone
                else:
                    existing = phone_map[key]
                    existing.provenance.extend(phone.provenance)

                    if phone.confidence.score > existing.confidence.score:
                        existing.confidence = phone.confidence

        return list(phone_map.values())

    def _dedupe_skills(self, fragments: List[CandidateFragment]) -> List[Skill]:
        skill_map: Dict[str, Skill] = {}

        for fragment in fragments:
            for skill in fragment.skills:
                key = skill.value.lower().strip()

                if key not in skill_map:
                    skill_map[key] = skill
                else:
                    existing = skill_map[key]
                    existing.provenance.extend(skill.provenance)

                    if skill.confidence.score > existing.confidence.score:
                        existing.confidence = skill.confidence

        return list(skill_map.values())