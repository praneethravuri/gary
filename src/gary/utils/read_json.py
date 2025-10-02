import json
from gary.models import MasterResume
from gary.config import RESUME_PATH
from gary.exceptions import DataLoadError


def read_resume_json() -> MasterResume:
    """
    Read resume.json from the data directory and return as MasterResume model.

    Returns:
        MasterResume: Parsed resume data containing header and content

    Raises:
        DataLoadError: If resume.json does not exist, is invalid, or doesn't match schema
    """
    try:
        if not RESUME_PATH.exists():
            raise DataLoadError(f"resume.json not found at {RESUME_PATH}")

        with open(RESUME_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        return MasterResume(**data)
    except (json.JSONDecodeError, ValueError) as e:
        raise DataLoadError(f"Failed to parse resume.json: {e}") from e
    except Exception as e:
        raise DataLoadError(f"Failed to read resume.json: {e}") from e
