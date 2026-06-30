from pathlib import Path
from typing import List

from app.models.candidate import CandidateFragment
from app.parsers.ats_parser import ATSJSONParser
from app.parsers.csv_parser import RecruiterCSVParser
from app.parsers.notes_parser import NotesParser


class ParserService:
    def __init__(self):
        self.csv_parser = RecruiterCSVParser()
        self.ats_parser = ATSJSONParser()
        self.notes_parser = NotesParser()

    def parse_input_directory(self, input_dir: Path) -> List[CandidateFragment]:
        fragments: List[CandidateFragment] = []

        for file_path in input_dir.iterdir():
            if file_path.name == "recruiter.csv":
                fragments.append(self.csv_parser.parse(file_path))

            elif file_path.name == "ats.json":
                fragments.append(self.ats_parser.parse(file_path))

            elif file_path.name == "notes.txt":
                fragments.append(self.notes_parser.parse(file_path))

        return fragments