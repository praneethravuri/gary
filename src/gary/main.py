#!/usr/bin/env python
import sys
import warnings
from gary.crew import Gary
from gary.utils.read_json import read_header_json, read_resume_json
from gary.models import Resume, ResumeContent
from gary.utils.resume_word_doc_generator import generate_word_resume
from gary.utils.google_sheets import initialize_sheets_client
from gary.utils.result_parser import parse_crew_result
from src.gary.config import RESUME_GENERATED_GOOGLE_SHEETS_COLUMN, JOB_DESCRIPTION_GOOGLE_SHEETS_COLUMN

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run() -> None:
    """
    Run the crew with comprehensive error handling.
    """
    try:
        # 1. Connect to Google Sheets and extract last row as JobDetails
        sheets_client = initialize_sheets_client()
        last_row_number, job_details = sheets_client.get_last_row_as_job_details()

        # 2. Read resume from resume.json as ResumeContent
        master_resume = read_resume_json()

        # 3. Send resume and job description to crew
        inputs = {
            "job_description": job_details.job_description,
            "master_resume": master_resume.model_dump(),
        }

        gary_crew = Gary().crew()
        result = gary_crew.kickoff(inputs=inputs)
        print(result)

        # 4. Load header and prepare final resume
        header = read_header_json()
        header.location = job_details.location

        # Parse CrewAI result
        result_data = parse_crew_result(result)
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

        # 6. Update 7th cell of last row to "Done"
        sheets_client.update_cell(last_row_number, RESUME_GENERATED_GOOGLE_SHEETS_COLUMN, "Done")
        print(f"✓ Updated row {last_row_number}, column {RESUME_GENERATED_GOOGLE_SHEETS_COLUMN} to 'Done'")

        # 7. Update the 6th cell of last row with cleaned job description
        sheets_client.update_cell(last_row_number, JOB_DESCRIPTION_GOOGLE_SHEETS_COLUMN, job_details.job_description)
        print(f"✓ Updated row {last_row_number}, column {JOB_DESCRIPTION_GOOGLE_SHEETS_COLUMN} with cleaned job description")

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
