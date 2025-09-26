import re
import unicodedata
from pathlib import Path
from typing import Optional


def clean_job_description() -> str:
    """
    Read the job description from /data/job_description.txt, clean it by removing 
    non-ASCII characters, unicode characters, excessive whitespace, newlines, 
    and structure it for AI model consumption.
    
    Returns:
        Cleaned and structured job description text, or error message if file cannot be read
    """

    project_root = Path(__file__).parent.parent.parent.parent
    file_path = project_root / "data" / "job_description.txt"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_job_description = file.read()

        normalized_job_description = unicodedata.normalize('NFKD', raw_job_description)
        ascii_text = normalized_job_description.encode('ascii', 'ignore').decode('ascii')
        cleaned_job_description = re.sub(r'\s+', ' ', ascii_text)
        cleaned_job_description = cleaned_job_description.replace('\n', ' ').replace('\r', ' ')
        cleaned_job_description = re.sub(r'[\t\f\v]', ' ', cleaned_job_description)
        cleaned_job_description = re.sub(r'\s+', ' ', cleaned_job_description)
        cleaned_job_description = cleaned_job_description.strip()

        return cleaned_job_description

    except FileNotFoundError:
        return f"Error: Job description file not found at: {file_path}"
    except Exception as e:
        return f"Error reading job description file: {str(e)}"