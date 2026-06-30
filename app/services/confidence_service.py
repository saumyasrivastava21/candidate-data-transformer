from typing import List, Optional

from app.models.candidate import Confidence, Email, FieldValue, Phone, Skill


class ConfidenceService:
    """
    Calculates profile-level confidence after merge.
    """

    def calculate_global_confidence(
        self,
        full_name: Optional[FieldValue],
        emails: List[Email],
        phones: List[Phone],
        skills: List[Skill],
    ) -> Confidence:
        score = 0.0
        reasons = []

        if full_name:
            score += 0.30
            reasons.append("identity present")

        if emails:
            score += 0.30
            reasons.append("email present")

        if phones:
            score += 0.20
            reasons.append("phone present")

        if len(skills) >= 3:
            score += 0.20
            reasons.append("3+ skills present")
        elif skills:
            score += 0.10
            reasons.append("some skills present")

        return Confidence(
            score=round(min(score, 1.0), 2),
            reason=", ".join(reasons) if reasons else "low information profile",
        )