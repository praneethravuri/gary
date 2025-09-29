import os
import json
from pathlib import Path
from typing import Type
from crewai.tools import BaseTool
from docxtpl import DocxTemplate
from pydantic import BaseModel, Field
from src.gary.models import Resume, JobDetails

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
RESUMES_DIR = PROJECT_ROOT /  "resumes"
RESUME_WORD_TEMPLATE = PROJECT_ROOT / "templates" / "resume_word_template.docx"

def generate_word_resume(resume: Resume, job_details: JobDetails) -> str:
    try:
        os.makedirs(RESUMES_DIR, exist_ok=True)

        # Generate filename from job details and candidate name
        company_name = job_details.company_name.replace(" ", "_").replace("/", "_")
        job_title = job_details.job_title.replace(" ", "_").replace("/", "_")
        job_id = job_details.job_id if job_details.job_id else ""
        candidate_name = "_".join(resume.header.name.lower().split(" "))

        file_name = f"{candidate_name}_{company_name}_{job_title}"
        if job_id:
            file_name += f"_{job_id}"
        file_name += ".docx"

        file_path = os.path.join(RESUMES_DIR, file_name)


        doc = DocxTemplate(RESUME_WORD_TEMPLATE)
        doc.render(resume.model_dump(mode="json"))
        doc.save(file_path)

        return file_path
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Template file not found: {str(e)}")
    except ValueError as e:
        raise ValueError(f"Invalid resume data: {str(e)}")
    except PermissionError as e:
        raise PermissionError(
            f"Cannot write to output directory: {str(e)}")