from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from gary.models import Resume, JobDetails
from gary.utils.resume_word_doc_generator import generate_word_resume


class ResumeWordDocGeneratorInput(BaseModel):
    """Input schema for ResumeWordDocGeneratorTool."""
    resume: Resume = Field(..., description="Complete resume object containing header and content")
    job_details: JobDetails = Field(..., description="Job details object containing company, title, and other job information")


class ResumeWordDocGeneratorTool(BaseTool):
    name: str = "Generate Word Document Resume"
    description: str = (
        "Generates a professionally formatted Word document (.docx) resume from Resume and JobDetails objects. "
        "Returns the file path to the generated document."
    )
    args_schema: Type[BaseModel] = ResumeWordDocGeneratorInput

    def _run(self, resume: Resume, job_details: JobDetails) -> str:
        """
        Generate a Word document resume.

        Args:
            resume: Resume object containing all resume data
            job_details: JobDetails object containing job information

        Returns:
            str: Path to the generated Word document
        """
        file_path = generate_word_resume(resume, job_details)
        return f"Successfully generated resume at: {file_path}"
