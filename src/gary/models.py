from pydantic import BaseModel, Field, EmailStr
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
        description="List of technical, hard, tools, and technologies like Python, SQL, GCP, AWS, Tableau, Power BI, Looker, etc.",
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

class KeyTerms(BaseModel):
    """Structured model for key terms."""
    responsibilities_and_qualifications: List[str] = Field(
        ...,
        description="A verbatim list of responsibilities and qualifications from the job description like Responsibilities, Qualifications, Duties, etc.",
    )
    company_culture_keywords: List[str] = Field(
        ...,
        description="Keywords related to the company's mission, culture, and values like Mission, Vision, Values, etc.",
    )


class JobAnalysis(BaseModel):
    """The complete structured output from the Job Description Analyst agent."""

    job_details: JobDetails = Field(
        ..., description="Core details about the job and company."
    )
    skills: Skills = Field(
        ..., description="A categorized breakdown of all required skills."
    )
    key_terms: KeyTerms = Field(
        ...,
        description="A categorized breakdown of all required key terms.",
    )


# Resume Model


class Metadata(BaseModel):
    job_title: str = Field(..., description="Job title")
    company_name: str = Field(..., description="Company name")
    job_id: Optional[str] = Field(None, description="Job ID")
    location: str = Field(..., description="Location")


class Link(BaseModel):
    platform: str = Field(..., description="Platform name")
    url: str = Field(..., description="Platform URL")


class ProfessionalSummary(BaseModel):
    summary: str = Field(..., description="Professional summary")


class ContactInfo(BaseModel):
    name: str = Field(..., description="Name")
    phone: str = Field(..., description="Phone number")
    email: EmailStr = Field(..., description="Email address")
    links: List[Link] = Field(..., description="Links")


class WorkExperience(BaseModel):
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    dates: str = Field(..., description="Dates")
    responsibilities: List[str] = Field(..., description="Responsibilities")


class Education(BaseModel):
    degree: str = Field(..., description="Degree")
    institution: str = Field(..., description="Institution")
    dates: str = Field(..., description="Dates")
    coursework: List[str] = Field(..., description="Coursework")


class Skill(BaseModel):
    category: str = Field(..., description="Skill category")
    items: List[str] = Field(..., description="Skill items")


class Project(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")


class Resume(BaseModel):
    metadata: Metadata = Field(..., description="Metadata")
    contact_info: ContactInfo = Field(..., description="Contact information")
    professional_summary: ProfessionalSummary = Field(
        ..., description="Professional summary"
    )
    work_experience: List[WorkExperience] = Field(..., description="Work experience")
    education: List[Education] = Field(..., description="Education")
    skills: List[Skill] = Field(..., description="Skills")
    projects: List[Project] = Field(..., description="Projects")
