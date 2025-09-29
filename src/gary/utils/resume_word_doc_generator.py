from docxtpl import DocxTemplate
from gary.models import Resume, JobDetails
from gary.config import RESUMES_DIR, RESUME_WORD_TEMPLATE
from gary.exceptions import ResumeGenerationError

def generate_word_resume(resume: Resume, job_details: JobDetails) -> str:
    """
    Generate a Word document resume from Resume and JobDetails objects.

    Args:
        resume: Resume object containing all resume data
        job_details: JobDetails object containing job information

    Returns:
        str: Path to the generated Word document

    Raises:
        ResumeGenerationError: If template not found, resume data invalid, or cannot write output
    """
    try:
        RESUMES_DIR.mkdir(parents=True, exist_ok=True)

        # Generate filename from job details and candidate name
        company_name = job_details.company_name.replace(" ", "_").replace("/", "_")
        job_title = job_details.job_title.replace(" ", "_").replace("/", "_")
        job_id = job_details.job_id if job_details.job_id else ""
        candidate_name = "_".join(resume.header.name.lower().split(" "))

        file_name = f"{candidate_name}_{company_name}_{job_title}"
        if job_id:
            file_name += f"_{job_id}"
        file_name += ".docx"

        file_path = RESUMES_DIR / file_name

        if not RESUME_WORD_TEMPLATE.exists():
            raise ResumeGenerationError(f"Template file not found: {RESUME_WORD_TEMPLATE}")

        doc = DocxTemplate(RESUME_WORD_TEMPLATE)
        doc.render(resume.model_dump(mode="json"))
        doc.save(str(file_path))

        return str(file_path)
    except ResumeGenerationError:
        raise
    except (ValueError, KeyError) as e:
        raise ResumeGenerationError(f"Invalid resume data: {e}") from e
    except PermissionError as e:
        raise ResumeGenerationError(f"Cannot write to output directory: {e}") from e
    except Exception as e:
        raise ResumeGenerationError(f"Failed to generate resume: {e}") from e