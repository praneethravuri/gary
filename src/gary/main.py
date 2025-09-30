#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from gary.crew import Gary
from gary.utils.read_json import read_resume_json
from gary.models import Resume, JobDetails
from gary.utils.resume_word_doc_generator import generate_word_resume
from gary.utils.google_sheets import initialize_sheets_client
from gary.utils.result_parser import parse_crew_result
from gary.utils.clean_job_description import clean_job_description

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def get_job_details_from_cli() -> JobDetails:
    """
    Collect job details from CLI prompts.

    Returns:
        JobDetails: Populated job details model
    """
    print("="*80)
    print("JOB DETAILS INPUT")
    print("="*80)

    company_name = input("Company Name: ").strip()
    job_title = input("Job Title: ").strip()
    location = input("Location: ").strip()
    job_id = input("Job ID (optional, press Enter to skip): ").strip()

    print("\nJob Description (paste below, then type 'END' on a new line and press Enter):")
    description_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        description_lines.append(line)

    job_description = "\n".join(description_lines).strip()

    # Automatically set date to today in MM-DD-YYYY format
    date_applied = datetime.now().strftime("%m-%d-%Y")

    # Create JobDetails with cleaned description
    job_details = JobDetails(
        company_name=company_name,
        job_title=job_title,
        location=location,
        job_id=job_id if job_id else None,
        job_description=clean_job_description(job_description),
        date_applied=date_applied
    )

    print(f"\n✓ Job details collected for {company_name} - {job_title} (Applied: {date_applied})")
    return job_details


def run() -> None:
    """
    Run the crew with comprehensive error handling.
    """
    try:
        # 1. Collect job details from CLI
        job_details = get_job_details_from_cli()

        # 2. Read master resume from resume.json
        master_resume = read_resume_json()

        # 3. Extract resume content (without header) for crew processing
        resume_content_dict = {
            "professional_summary": master_resume.professional_summary.model_dump(),
            "work_experience": [exp.model_dump() for exp in master_resume.work_experience],
            "education": [edu.model_dump() for edu in master_resume.education],
            "skills": [skill.model_dump() for skill in master_resume.skills],
            "projects": [proj.model_dump() for proj in master_resume.projects],
        }

        # 4. Send resume content and job description to crew
        inputs = {
            "job_description": job_details.job_description,
            "master_resume": resume_content_dict,
        }

        gary_crew = Gary().crew()
        result = gary_crew.kickoff(inputs=inputs)
        print(result)

        # 5. Prepare final resume with updated header location
        header = master_resume.header.model_copy()
        header.location = job_details.location

        # Parse CrewAI result
        result_data = parse_crew_result(result)
        from gary.models import ResumeContent
        resume_content = ResumeContent(**result_data)
        final_resume = Resume(header=header, resume_content=resume_content)

        print("\n" + "="*80)
        print("FINAL RESUME")
        print("="*80)
        print(final_resume.model_dump_json(indent=2))

        # 5. Generate Word document
        print("\n" + "="*80)
        print("GENERATING WORD DOCUMENT")
        print("="*80)
        file_path = generate_word_resume(final_resume, job_details)
        print(f"✓ Resume generated successfully: {file_path}")

        # 6. Append job details to Google Sheets
        sheets_client = initialize_sheets_client()
        row_data = [
            job_details.date_applied,
            job_details.company_name,
            job_details.job_title,
            job_details.location,
            job_details.job_id or "",
            job_details.job_description,
            "Done"
        ]
        sheets_client.append_row(row_data)
        print(f"✓ Job details logged to Google Sheets")

        # Display usage metrics if available
        if hasattr(gary_crew, "usage_metrics") and gary_crew.usage_metrics:
            print(gary_crew.usage_metrics)

    except KeyboardInterrupt:
        print("\nExecution interrupted by user. Exiting...")
        sys.exit(0)
    except SystemExit:
        raise
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()
