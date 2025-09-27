#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from typing import Optional, Dict, Any
from gary.crew import Gary

from src.gary.utils.file_operations import load_job_description, load_resume

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run() -> None:
    """
    Run the crew with comprehensive error handling.
    """
    try:
        # Load job description with error handling
        try:
            job_description = load_job_description()
        except Exception as e:
            print(f"Unexpected error loading job description: {e}")
            sys.exit(1)

        # Load resume with error handling
        try:
            master_resume = load_resume()
        except Exception as e:
            print(f"Failed to load resume: {e}")
            sys.exit(1)

        # Prepare inputs
        try:
            inputs = {
                "job_description": job_description,
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
