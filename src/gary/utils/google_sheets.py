import gspread
import os
from typing import List, Optional
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from gary.models import JobDetails
from gary.utils.clean_job_description import clean_job_description

load_dotenv()


class GoogleSheetsClient:
    def __init__(self, credentials_file: str = "googleSheetsCredentials.json"):
        """
        Initialize Google Sheets client with service account credentials.

        Args:
            credentials_file: Path to the service account JSON file
        """
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
        ]

        self.creds = Credentials.from_service_account_file(
            credentials_file, scopes=self.scopes
        )

        self.client = gspread.authorize(self.creds)
        self.sheet = None
        self.worksheet = None

    def connect_to_sheet(self, sheet_id: str, worksheet_name: str = "Sheet1"):
        """
        Connect to a specific Google Sheet and worksheet.

        Args:
            sheet_id: The Google Sheets document ID
            worksheet_name: Name of the worksheet (default: "Sheet1")
        """
        self.sheet = self.client.open_by_key(sheet_id)
        self.worksheet = self.sheet.worksheet(worksheet_name)

    def get_all_rows(self) -> List[List[str]]:
        """
        Extract all rows from the connected worksheet.

        Returns:
            List of lists containing all row data

        Raises:
            ValueError: If no worksheet is connected
        """
        if not self.worksheet:
            raise ValueError("No worksheet connected. Call connect_to_sheet() first.")

        return self.worksheet.get_all_values()

    def get_all_records(self) -> List[dict]:
        """
        Extract all records from the worksheet as dictionaries.
        Uses first row as headers.

        Returns:
            List of dictionaries with column headers as keys

        Raises:
            ValueError: If no worksheet is connected
        """
        if not self.worksheet:
            raise ValueError("No worksheet connected. Call connect_to_sheet() first.")

        return self.worksheet.get_all_records()

    def get_row(self, row_number: int) -> List[str]:
        """
        Get a specific row by number.

        Args:
            row_number: Row number (1-indexed)

        Returns:
            List of values in the specified row

        Raises:
            ValueError: If no worksheet is connected
        """
        if not self.worksheet:
            raise ValueError("No worksheet connected. Call connect_to_sheet() first.")

        return self.worksheet.row_values(row_number)

    def update_cell(self, row: int, col: int, value: str) -> None:
        """
        Update a specific cell in the worksheet.

        Args:
            row: Row number (1-indexed)
            col: Column number (1-indexed)
            value: Value to set in the cell

        Raises:
            ValueError: If no worksheet is connected
        """
        if not self.worksheet:
            raise ValueError("No worksheet connected. Call connect_to_sheet() first.")

        self.worksheet.update_cell(row, col, value)

    def process_ungenerated_resumes(self) -> List[JobDetails]:
        """
        Process rows where "Resume Generated" column is empty.
        Creates JobDetails objects from the row data and updates "Resume Generated" to "done".

        Returns:
            List of JobDetails objects for unprocessed rows

        Raises:
            ValueError: If no worksheet is connected or required columns not found
        """
        if not self.worksheet:
            raise ValueError("No worksheet connected. Call connect_to_sheet() first.")

        all_rows = self.worksheet.get_all_values()

        if len(all_rows) < 1:
            raise ValueError("Worksheet has no data")

        # Get headers and find column indices
        headers = all_rows[0]

        # Create a mapping of header names to indices
        header_map = {header: idx for idx, header in enumerate(headers)}

        # Find required column indices
        try:
            resume_gen_col_idx = header_map["Resume Generated"]
        except KeyError:
            raise ValueError("Column 'Resume Generated' not found in headers")

        job_details_list = []

        # Process rows 2 onwards (skip header row)
        for row_idx, row in enumerate(all_rows[1:], start=2):  # start=2 for 1-indexed row numbers
            # Extend row if it's shorter than expected
            while len(row) <= resume_gen_col_idx:
                row.append("")

            # Check if "Resume Generated" is empty
            if not row[resume_gen_col_idx].strip():
                # Print columns 1-5 (indices 0-4)
                print(f"Row {row_idx}: {row[:5]}")

                # Create JobDetails object from row data
                # Assuming columns are: company_name, job_title, location, job_id, job_description
                job_details = JobDetails(
                    company_name=row[0] if len(row) > 0 else "",
                    job_title=row[1] if len(row) > 1 else "",
                    location=row[2] if len(row) > 2 else "",
                    job_id=row[3] if len(row) > 3 and row[3] else None,
                    job_description= clean_job_description(row[4]) if len(row) > 4 else ""
                )

                job_details_list.append(job_details)
                print(f"Created JobDetails: {job_details.model_dump()}")

                # Update "Resume Generated" cell to "done"
                # Column is 1-indexed in gspread
                self.worksheet.update_cell(row_idx, resume_gen_col_idx + 1, "done")

        return job_details_list
    
sheets_client = GoogleSheetsClient("googleSheetsCredentials.json")
sheet_id = os.getenv("GOOGLE_SHEETS_ID")
if sheet_id:
    sheets_client.connect_to_sheet(sheet_id)
    # all_rows = sheets_client.get_all_rows()
    # print(all_rows)
    sheets_client.process_ungenerated_resumes()
else:
    print("GOOGLE_SHEETS_ID not found in environment variables")