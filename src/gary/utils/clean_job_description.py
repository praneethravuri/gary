import re
import unicodedata
from typing import Optional, List
import json
from pydantic import BaseModel
from src.gary.models import JobDetails

def clean_job_description(text: str) -> str:
    """
    Clean and normalize job description text.

    Args:
        text: Raw job description text
    Returns:
        str: Cleaned job description text
    """
    # Normalize unicode characters
    normalized_text = unicodedata.normalize('NFKD', text)
    
    # Convert to ASCII, ignoring non-ASCII characters
    ascii_text = normalized_text.encode('ascii', 'ignore').decode('ascii')

    cleaned_job_description = re.sub(r'\s+', ' ', ascii_text).strip()
    cleaned_job_description = cleaned_job_description.replace('\n', ' ').replace('\r', ' ')
    cleaned_job_description = re.sub(r'[\t\f\v]', ' ', cleaned_job_description)
    cleaned_job_description = re.sub(r'\s+', ' ', cleaned_job_description)
    cleaned_job_description = cleaned_job_description.strip()
    
    # Clean whitespace and special characters
    cleaned_text = re.sub(r'\s+', ' ', ascii_text).strip()
    
    return cleaned_text