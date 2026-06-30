from typing import Optional


SKILL_CANONICAL_MAP = {
    "python": "Python",
    "java": "Java",
    "springboot": "Spring Boot",
    "spring boot": "Spring Boot",
    "fastapi": "FastAPI",
    "fast api": "FastAPI",
    "yolo": "YOLO",
    "computer vision": "Computer Vision",
    "cv": "Computer Vision",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "dl": "Deep Learning",
    "healthcare ai": "Healthcare AI",
    "dsa": "DSA",
    "data structures": "DSA",
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    "docker": "Docker",
}


def normalize_skill(skill: str) -> Optional[str]:
    if not skill:
        return None

    raw = str(skill).strip()
    key = raw.lower().replace("-", " ").replace("_", " ")
    key = " ".join(key.split())

    compact_key = key.replace(" ", "")

    if key in SKILL_CANONICAL_MAP:
        return SKILL_CANONICAL_MAP[key]

    if compact_key in SKILL_CANONICAL_MAP:
        return SKILL_CANONICAL_MAP[compact_key]

    return raw.title()