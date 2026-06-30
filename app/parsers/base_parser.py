from abc import ABC, abstractmethod
from pathlib import Path

from app.models.candidate import CandidateFragment


class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: Path) -> CandidateFragment:
        pass