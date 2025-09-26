#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from gary.crew import Gary

from src.gary.utils.job_description_cleaner import clean_job_description

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    # Get the cleaned job description
    job_description = clean_job_description()
    
    # Check if there was an error reading the job description
    if job_description.startswith("Error:"):
        print(f"Failed to read job description: {job_description}")
        sys.exit(1)
    
    inputs = {"job_description": job_description}

    try:
        gary_crew = Gary().crew()
        result = gary_crew.kickoff(inputs=inputs)
        print(result)
        print(gary_crew.usage_metrics)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")