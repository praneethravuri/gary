import json
from gary.models import ResumeContent, Header
from gary.config import HEADER_PATH, RESUME_PATH
from gary.exceptions import DataLoadError


def read_header_json() -> Header:
    """
    Read header.json from the data directory and return as Header model.

    Returns:
        Header: Parsed header data

    Raises:
        DataLoadError: If header.json does not exist, is invalid, or doesn't match schema
    """
    try:
        if not HEADER_PATH.exists():
            raise DataLoadError(f"header.json not found at {HEADER_PATH}")

        with open(HEADER_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        return Header(**data)
    except (json.JSONDecodeError, ValueError) as e:
        raise DataLoadError(f"Failed to parse header.json: {e}") from e
    except Exception as e:
        raise DataLoadError(f"Failed to read header.json: {e}") from e


def read_resume_json() -> ResumeContent:
    """
    Read resume.json from the data directory and return as ResumeContent model.

    Returns:
        ResumeContent: Parsed resume data

    Raises:
        DataLoadError: If resume.json does not exist, is invalid, or doesn't match schema
    """
    try:
        if not RESUME_PATH.exists():
            raise DataLoadError(f"resume.json not found at {RESUME_PATH}")

        with open(RESUME_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        return ResumeContent(**data)
    except (json.JSONDecodeError, ValueError) as e:
        raise DataLoadError(f"Failed to parse resume.json: {e}") from e
    except Exception as e:
        raise DataLoadError(f"Failed to read resume.json: {e}") from e