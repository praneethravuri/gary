import os
import gspread
from typing import List, Tuple, Optional
from google.oauth2.service_account import Credentials
from gary.models import JobDetails
from gary.utils.clean_job_description import clean_job_description
from gary.config import DEFAULT_WORKSHEET_NAME, CREDENTIALS_FILE
from gary.exceptions import GoogleSheetsError


class GoogleSheetsClient:
    def __init__(self, credentials_file: str = CREDENTIALS_FILE):
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
            List[List[str]]: List of lists containing all row data

        Raises:
            GoogleSheetsError: If no worksheet is connected
        """
        if not self.worksheet:
            raise GoogleSheetsError("No worksheet connected. Call connect_to_sheet() first.")

        return self.worksheet.get_all_values()

    def get_all_records(self) -> List[dict]:
        """
        Extract all records from the worksheet as dictionaries.
        Uses first row as headers.

        Returns:
            List[dict]: List of dictionaries with column headers as keys

        Raises:
            GoogleSheetsError: If no worksheet is connected
        """
        if not self.worksheet:
            raise GoogleSheetsError("No worksheet connected. Call connect_to_sheet() first.")

        return self.worksheet.get_all_records()

    def get_row(self, row_number: int) -> List[str]:
        """
        Get a specific row by number.

        Args:
            row_number: Row number (1-indexed)

        Returns:
            List[str]: List of values in the specified row

        Raises:
            GoogleSheetsError: If no worksheet is connected
        """
        if not self.worksheet:
            raise GoogleSheetsError("No worksheet connected. Call connect_to_sheet() first.")

        return self.worksheet.row_values(row_number)

    def update_cell(self, row: int, col: int, value: str) -> None:
        """
        Update a specific cell in the worksheet.

        Args:
            row: Row number (1-indexed)
            col: Column number (1-indexed)
            value: Value to set in the cell

        Raises:
            GoogleSheetsError: If no worksheet is connected
        """
        if not self.worksheet:
            raise GoogleSheetsError("No worksheet connected. Call connect_to_sheet() first.")

        self.worksheet.update_cell(row, col, value)

    def get_last_row_as_job_details(self) -> Tuple[int, JobDetails]:
        """
        Get the last row from the worksheet (cells 1-5) and return as JobDetails.

        Returns:
            Tuple of (row_number, JobDetails model)

        Raises:
            GoogleSheetsError: If no worksheet is connected, worksheet is empty, or insufficient data
        """
        try:
            if not self.worksheet:
                raise GoogleSheetsError("No worksheet connected. Call connect_to_sheet() first.")

            all_rows = self.worksheet.get_all_values()

            if not all_rows:
                raise GoogleSheetsError("Worksheet is empty")

            last_row = all_rows[-1]
            last_row_number = len(all_rows)

            if len(last_row) < 5:
                raise GoogleSheetsError(f"Last row has only {len(last_row)} cells, need at least 5")

            # Extract first 5 cells
            company_name, job_title, location, job_id, job_description = last_row[:5]

            # Create JobDetails instance
            job_details = JobDetails(
                company_name=company_name,
                job_title=job_title,
                location=location,
                job_id=job_id if job_id else None,
                job_description=clean_job_description(job_description),
            )

            return last_row_number, job_details
        except Exception as e:
            if isinstance(e, GoogleSheetsError):
                raise
            raise GoogleSheetsError(f"Failed to retrieve job details: {e}") from e


def initialize_sheets_client(
    credentials_file: str = CREDENTIALS_FILE,
    worksheet_name: str = DEFAULT_WORKSHEET_NAME
) -> GoogleSheetsClient:
    """
    Initialize and connect Google Sheets client.

    Args:
        credentials_file: Path to the service account JSON file
        worksheet_name: Name of the worksheet (default: "Sheet1")

    Returns:
        Connected GoogleSheetsClient instance

    Raises:
        GoogleSheetsError: If GOOGLE_SHEETS_ID not found or connection fails
    """
    try:
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        if not sheet_id:
            raise GoogleSheetsError("GOOGLE_SHEETS_ID not found in environment variables")

        client = GoogleSheetsClient(credentials_file)
        client.connect_to_sheet(sheet_id, worksheet_name)
        return client
    except Exception as e:
        if isinstance(e, GoogleSheetsError):
            raise
        raise GoogleSheetsError(f"Failed to initialize Google Sheets client: {e}") from e