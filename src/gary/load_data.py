import os
from typing import Tuple
from gary.models import JobDetails, ResumeContent
from gary.utils.google_sheets import sheets_client
from gary.utils.read_json import read_resume_json


def load_data() -> Tuple[int, JobDetails, ResumeContent]:
    """
    Load job details from Google Sheets and resume data from JSON file.

    Returns:
        Tuple of (last_row_number, job_details, resume_content)

    Raises:
        ValueError: If Google Sheets is not connected or data is invalid
        FileNotFoundError: If resume.json does not exist
    """
    # Initialize Google Sheets connection if not already connected
    print("Initializing Google Sheets connection...")
    if not sheets_client.worksheet:
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        if not sheet_id:
            raise ValueError("GOOGLE_SHEETS_ID not found in environment variables")
        print(f"Connecting to Google Sheets: {sheet_id}")
        sheets_client.connect_to_sheet(sheet_id)
        print("Connected to Google Sheets successfully")
    else:
        print("Google Sheets already connected")

    print("Fetching job details from Google Sheets...")
    last_row_number, job_details = sheets_client.get_last_row_as_job_details()

    print("Loading resume from JSON...")
    resume_content = read_resume_json()

    print(f"✓ Loaded job details from row {last_row_number}")
    print(f"✓ Loaded resume with name: {resume_content}")
    print(f"✓ Job: {job_details}")
    return last_row_number, job_details, resume_content


if __name__ == "__main__":
    load_data()