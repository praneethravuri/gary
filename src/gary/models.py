from pydantic import BaseModel, Field
from typing import List, Optional

# Job Description Analyst Model


class JobDetails(BaseModel):
    """Structured model for basic job information."""

    company_name: str = Field(..., description="The name of the hiring company.")
    job_title: str = Field(..., description="The title of the position.")
    location: str = Field(
        ..., description="The location of the job (e.g., City, State, Remote)."
    )
    job_id: Optional[str] = Field(None, description="The job identifier, if available.")


class Skills(BaseModel):
    """Structured model for categorized skills."""

    technical: List[str] = Field(
        default=[],
        description="List of technical or hard skills like Python, SQL, GCP, AWS, etc.",
    )
    soft: List[str] = Field(
        default=[],
        description="List of soft or interpersonal skills like communication, teamwork, etc.",
    )
    management: List[str] = Field(
        default=[],
        description="List of management or leadership skills like cross-functional collaboration, stakeholder management, etc.",
    )
    bonus: List[str] = Field(
        default=[],
        description="List of skills mentioned as a 'plus' or 'nice-to-have'.",
    )
    tools_and_technologies: List[str] = Field(
        default=[],
        description="Specific software, platforms, or tools mentioned like Tableau, Power BI, Looker, etc.",
    )


class JobAnalysis(BaseModel):
    """The complete structured output from the Job Description Analyst agent."""

    job_details: JobDetails = Field(
        ..., description="Core details about the job and company."
    )
    skills: Skills = Field(
        ..., description="A categorized breakdown of all required skills."
    )
    responsibilities_and_qualifications: List[str] = Field(
        ...,
        description="A verbatim list of responsibilities and qualifications from the job description like Responsibilities, Qualifications, Duties, etc.",
    )
    key_phrases: List[str] = Field(
        default=[],
        description="List of important or frequently repeated phrases indicating priority.",
    )
    company_culture_keywords: List[str] = Field(
        default=[],
        description="Keywords related to the company's mission, culture, and values like Mission, Vision, Values, etc.",
    )