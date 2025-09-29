import json
import os
from pathlib import Path
from gary.models import ResumeContent, Header

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
RESUME_PATH = PROJECT_ROOT / "data" / "resume.json"
HEADER_PATH = PROJECT_ROOT / "data" / "header.json"


def read_header_json() -> Header:
    """
    Read header.json from the data directory and return as Header model.

    Returns:
        Header: Parsed header data

    Raises:
        FileNotFoundError: If header.json does not exist
        ValueError: If JSON is invalid or doesn't match schema
    """
    if not os.path.exists(HEADER_PATH):
        raise FileNotFoundError(f"header.json not found at {HEADER_PATH}")

    with open(HEADER_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return Header(**data)


def read_resume_json() -> ResumeContent:
    """
    Read resume.json from the data directory and return as ResumeContent model.

    Returns:
        ResumeContent: Parsed resume data

    Raises:
        FileNotFoundError: If resume.json does not exist
        ValueError: If JSON is invalid or doesn't match schema
    """
    # Get the project root directory (3 levels up from this file)

    if not os.path.exists(RESUME_PATH):
        raise FileNotFoundError(f"resume.json not found at {RESUME_PATH}")

    with open(RESUME_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return ResumeContent(**data)