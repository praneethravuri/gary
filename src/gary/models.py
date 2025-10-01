from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

# Job Model


class JobDetails(BaseModel):
    """Structured model for job postings."""
    company_name: str = Field(...,
                              description="The name of the hiring company.")
    job_title: str = Field(..., description="The title of the position.")
    location: str = Field(...,
                          description="The location of the job (e.g., City, State, Remote).")
    job_id: Optional[str] = Field(
        None, description="The job identifier, if available.")
    job_description: str = Field(...,
                                 description="The full text of the job description.")
    date_applied: str = Field(...,
                              description="Date applied in MM-DD-YYYY format.")


class Skills(BaseModel):
    """Categorized skills extracted from job description."""

    technical: List[str] = Field(
        default=[],
        description="Programming languages, tools, platforms, certifications, methodologies. Use exact terminology with abbreviations and versions.",
    )
    soft: List[str] = Field(
        default=[],
        description="Interpersonal skills like communication, problem-solving, teamwork. Exclude generic buzzwords.",
    )
    management: List[str] = Field(
        default=[],
        description="Leadership, stakeholder management, strategic planning, cross-functional collaboration.",
    )
    bonus: List[str] = Field(
        default=[],
        description="Nice-to-have or preferred qualifications.",
    )


class JobAnalysis(BaseModel):
    """Structured output from job description analysis for ATS optimization."""

    skills: Skills = Field(
        default_factory=Skills,
        description="Categorized skills: technical, soft, management, bonus."
    )

    responsibilities_and_qualifications: List[str] = Field(
        default=[],
        description="Complete phrases covering duties, requirements, qualifications. Strip buzzwords but preserve meaning and industry terminology. Include quantifiable requirements. Flag repeated phrases as high priority.",
    )

    tone_and_priorities: List[str] = Field(
        default=[],
        description="Company tone indicators: fast-paced, collaborative, data-driven, innovative, results-oriented.",
    )

    culture_and_values: List[str] = Field(
        default=[],
        description="Cultural values: diversity, growth mindset, work-life balance, mission alignment. Exclude generic marketing language.",
    )


# Resume Content Model


class ProfessionalSummary(BaseModel):
    summary: str = Field(..., description="Professional summary")


class WorkExperience(BaseModel):
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    startDate: str = Field(..., description="Start date")
    endDate: str = Field(..., description="End date")
    responsibilities: List[str] = Field(..., description="Responsibilities")


class Education(BaseModel):
    degree: str = Field(..., description="Degree")
    institution: str = Field(..., description="Institution")
    startDate: str = Field(..., description="Start date")
    endDate: str = Field(..., description="End date")
    coursework: List[str] = Field(..., description="Coursework")


class Skill(BaseModel):
    category: str = Field(..., description="Skill category")
    items: List[str] = Field(..., description="Skill items")


class Project(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")


class ResumeContent(BaseModel):
    professional_summary: ProfessionalSummary = Field(
        ..., description="Professional summary"
    )
    work_experience: List[WorkExperience] = Field(
        ..., description="Work experience")
    education: List[Education] = Field(..., description="Education")
    skills: List[Skill] = Field(..., description="Skills")
    projects: List[Project] = Field(..., description="Projects")


# Resume Model

class Link(BaseModel):
    platform: str = Field(..., description="Platform name")
    url: str = Field(..., description="Platform URL")


class Header(BaseModel):
    name: str = Field(..., description="Name")
    phone: str = Field(..., description="Phone number")
    email: EmailStr = Field(..., description="Email address")
    links: List[Link] = Field(..., description="Links")
    location: str = Field(..., description="Location")


class Resume(BaseModel):
    header: Header = Field(..., description="Contact information")
    resume_content: ResumeContent = Field(..., description="Resume content")


class MasterResume(BaseModel):
    """Combined resume model containing both header and content."""
    header: Header = Field(..., description="Contact information")
    professional_summary: ProfessionalSummary = Field(
        ..., description="Professional summary")
    work_experience: List[WorkExperience] = Field(
        ..., description="Work experience")
    education: List[Education] = Field(..., description="Education")
    skills: List[Skill] = Field(..., description="Skills")
    projects: List[Project] = Field(..., description="Projects")


# Resume Validation Models

class KeywordIntegration(BaseModel):
    """Analysis of keyword integration in the resume."""
    total_keywords_from_job: int = Field(
        ..., description="Total number of keywords identified in the job description")
    keywords_integrated: int = Field(
        ..., description="Number of keywords successfully integrated into the resume")
    integration_rate: float = Field(...,
                                    description="Percentage of keywords integrated (0-100)")
    missing_critical_keywords: List[str] = Field(
        default=[], description="List of critical keywords that should be added")
    naturally_integrated_keywords: List[str] = Field(
        default=[], description="Keywords that were integrated naturally")
    forced_keywords: List[str] = Field(
        default=[], description="Keywords that appear forced or unnaturally placed")


class PhraseUsage(BaseModel):
    """Analysis of specific phrase usage from job description."""
    phrases_used_correctly: List[str] = Field(
        default=[], description="Phrases from job description used appropriately")
    phrases_used_incorrectly: List[str] = Field(
        default=[], description="Phrases that are misused or don't fit context")
    missing_important_phrases: List[str] = Field(
        default=[], description="Important phrases from job description not used")


class ValidationFeedback(BaseModel):
    """Detailed feedback on resume quality."""
    strengths: List[str] = Field(..., description="What the resume does well")
    weaknesses: List[str] = Field(...,
                                  description="Areas that need improvement")
    suggestions: List[str] = Field(
        ..., description="Specific actionable suggestions for improvement")
    ats_score: int = Field(..., description="ATS compatibility score (0-100)")
    human_readability_score: int = Field(
        ..., description="How natural and human-written the resume sounds (0-100)")


class ResumeValidationReport(BaseModel):
    """Complete validation report for a tailored resume."""
    passed_validation: bool = Field(
        ..., description="Whether the resume passes validation criteria")
    overall_score: int = Field(...,
                               description="Overall resume quality score (0-100)")
    keyword_analysis: KeywordIntegration = Field(
        ..., description="Analysis of keyword integration")
    phrase_analysis: PhraseUsage = Field(...,
                                         description="Analysis of phrase usage")
    feedback: ValidationFeedback = Field(...,
                                         description="Detailed feedback and suggestions")
    ready_for_generation: bool = Field(
        ..., description="Whether resume is ready for Word document generation")
