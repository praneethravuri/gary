import os
import gspread
from typing import List
from google.oauth2.service_account import Credentials
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

    def append_row(self, row_data: List[str]) -> None:
        """
        Append a row to the worksheet.

        Args:
            row_data: List of values to append as a new row

        Raises:
            GoogleSheetsError: If no worksheet is connected
        """
        if not self.worksheet:
            raise GoogleSheetsError("No worksheet connected. Call connect_to_sheet() first.")

        self.worksheet.append_row(row_data)


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