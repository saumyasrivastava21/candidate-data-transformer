from typing import List

from app.models.candidate import CandidateFragment
from app.normalizers.email_normalizer import normalize_email
from app.normalizers.phone_normalizer import normalize_phone
from app.normalizers.skill_normalizer import normalize_skill
from app.normalizers.text_normalizer import normalize_company, normalize_name, normalize_title


class NormalizationService:
    """
    Phase 4 update:
    This service ONLY normalizes CandidateFragment objects.
    It does not merge or deduplicate anymore.
    """

    def normalize_fragments(self, fragments: List[CandidateFragment]) -> List[CandidateFragment]:
        normalized_fragments = []

        for fragment in fragments:
            if fragment.full_name:
                normalized_name = normalize_name(fragment.full_name.value)
                if normalized_name:
                    fragment.full_name.value = normalized_name

            if fragment.current_company:
                normalized_company = normalize_company(fragment.current_company.value)
                if normalized_company:
                    fragment.current_company.value = normalized_company

            if fragment.current_title:
                normalized_title = normalize_title(fragment.current_title.value)
                if normalized_title:
                    fragment.current_title.value = normalized_title

            for email in fragment.emails:
                normalized_email = normalize_email(email.value)
                if normalized_email:
                    email.value = normalized_email

            for phone in fragment.phones:
                normalized_phone = normalize_phone(phone.value)
                if normalized_phone:
                    phone.value = normalized_phone

            for skill in fragment.skills:
                normalized_skill = normalize_skill(skill.value)
                if normalized_skill:
                    skill.value = normalized_skill

            normalized_fragments.append(fragment)

        return normalized_fragments