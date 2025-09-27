import re
import unicodedata
from pathlib import Path
from typing import Optional, List
import json
from pydantic import BaseModel
from src.gary.models import Resume

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
RESUME_PATH = PROJECT_ROOT / "data" / "resume.json"
JOB_DESCRIPTION_PATH = PROJECT_ROOT / "data" / "job_description.txt"


def load_resume():
    """
    Load resume data from JSON file and return a Resume object.
    
    Returns:
        Resume: Parsed resume object
        
    Raises:
        FileNotFoundError: If resume file doesn't exist
        json.JSONDecodeError: If JSON is malformed
        ValueError: If resume data doesn't match Resume model
        Exception: For other unexpected errors
    """
    try:
        with open(RESUME_PATH, "r", encoding='utf-8') as f:
            resume_data = json.load(f)
        return Resume(**resume_data)
    except FileNotFoundError:
        raise FileNotFoundError(f"Resume file not found at: {RESUME_PATH}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in resume file: {e.msg}", e.doc, e.pos)
    except Exception as e:
        if isinstance(e, (FileNotFoundError, json.JSONDecodeError)):
            raise
        raise Exception(f"Error loading resume: {str(e)}")

def load_job_description():
    """
    Load and clean job description from text file.
    
    Returns:
        str: Cleaned job description text
        
    Raises:
        FileNotFoundError: If job description file doesn't exist
        UnicodeDecodeError: If file encoding issues occur
        Exception: For other unexpected errors
    """
    try:
        with open(JOB_DESCRIPTION_PATH, 'r', encoding='utf-8') as file:
            raw_job_description = file.read()

        # Normalize unicode characters
        normalized_job_description = unicodedata.normalize('NFKD', raw_job_description)
        
        # Convert to ASCII, ignoring non-ASCII characters
        ascii_text = normalized_job_description.encode('ascii', 'ignore').decode('ascii')
        
        # Clean whitespace and special characters
        cleaned_job_description = re.sub(r'\s+', ' ', ascii_text)
        cleaned_job_description = cleaned_job_description.replace('\n', ' ').replace('\r', ' ')
        cleaned_job_description = re.sub(r'[\t\f\v]', ' ', cleaned_job_description)
        cleaned_job_description = re.sub(r'\s+', ' ', cleaned_job_description)
        cleaned_job_description = cleaned_job_description.strip()

        return cleaned_job_description

    except FileNotFoundError:
        raise FileNotFoundError(f"Job description file not found at: {JOB_DESCRIPTION_PATH}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Unable to decode job description file with UTF-8 encoding: {e.reason}", e.object, e.start, e.end)
    except Exception as e:
        if isinstance(e, (FileNotFoundError, UnicodeDecodeError)):
            raise
        raise Exception(f"Error processing job description file: {str(e)}")