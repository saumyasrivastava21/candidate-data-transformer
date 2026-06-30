from typing import Optional


def normalize_name(name: str) -> Optional[str]:
    if not name:
        return None

    name = str(name).strip()
    name = " ".join(name.split())

    if not name:
        return None

    return name.title()


def normalize_company(company: str) -> Optional[str]:
    if not company:
        return None

    company = str(company).strip()
    company = " ".join(company.split())

    suffixes = [" Pvt Ltd", " Private Limited", " LLC", " Inc.", " Inc", " Ltd"]

    for suffix in suffixes:
        if company.lower().endswith(suffix.lower()):
            company = company[: -len(suffix)]

    return company.strip()


def normalize_title(title: str) -> Optional[str]:
    if not title:
        return None

    title = str(title).strip()
    title = " ".join(title.split())

    return title