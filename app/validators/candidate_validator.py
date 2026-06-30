from typing import List

from pydantic import ValidationError

from app.models.candidate import CandidateProfile


def validate_candidate(candidate_data: dict) -> CandidateProfile:
    return CandidateProfile(**candidate_data)


def collect_validation_errors(candidate_data: dict) -> List[str]:
    try:
        CandidateProfile(**candidate_data)
        return []
    except ValidationError as error:
        return [str(err) for err in error.errors()]
    except ValueError as error:
        return [str(error)]