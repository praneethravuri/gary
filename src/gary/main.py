#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from typing import Optional, Dict, Any
from gary.crew import Gary
from gary.load_data import load_data
from gary.utils.read_json import read_header_json
from gary.models import Resume, ResumeContent
from gary.utils.resume_word_doc_generator import generate_word_resume
from gary.utils.google_sheets import sheets_client

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run() -> None:
    """
    Run the crew with comprehensive error handling.
    """
    try:

        last_row_number, job_details, master_resume = load_data()

        # Prepare inputs
        try:
            inputs = {
                "job_description": job_details.job_description,
                "master_resume": master_resume.model_dump(),
            }
        except Exception as e:
            print(f"Failed to prepare inputs: {e}")
            sys.exit(1)

        # Initialize and run crew
        try:
            gary_crew = Gary().crew()
            result = gary_crew.kickoff(inputs=inputs)
            print(result)

            # Load header and combine with result into Resume model
            header = read_header_json()

            # Update header location with job location
            header.location = job_details.location

            # Extract data from CrewOutput object
            import json
            if hasattr(result, 'raw'):
                # result is a CrewOutput object, extract the raw string
                result_data = json.loads(result.raw)
            elif isinstance(result, str):
                result_data = json.loads(result)
            elif isinstance(result, dict):
                result_data = result
            else:
                result_data = result

            # Parse as ResumeContent
            resume_content = ResumeContent(**result_data)

            # Create final Resume model
            final_resume = Resume(header=header, resume_content=resume_content)

            print("\n" + "="*80)
            print("FINAL RESUME")
            print("="*80)
            print(final_resume.model_dump_json(indent=2))

            # Generate Word document
            print("\n" + "="*80)
            print("GENERATING WORD DOCUMENT")
            print("="*80)
            try:
                file_path = generate_word_resume(final_resume, job_details)
                print(f"✓ Resume generated successfully: {file_path}")

                # Update Google Sheets to mark as "Done"
                print("\nUpdating Google Sheets status...")
                sheets_client.update_cell(last_row_number, 6, "Done")
                print(f"✓ Updated row {last_row_number}, column 6 to 'Done'")
            except Exception as e:
                print(f"✗ Failed to generate Word document: {e}")

            # Display usage metrics if available
            if hasattr(gary_crew, "usage_metrics") and gary_crew.usage_metrics:
                print(gary_crew.usage_metrics)

        except AttributeError as e:
            print(f"Gary crew initialization failed - missing attribute: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error during crew execution: {e}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nExecution interrupted by user. Exiting...")
        sys.exit(0)
    except SystemExit:
        # Re-raise SystemExit to preserve exit codes
        raise
    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()
