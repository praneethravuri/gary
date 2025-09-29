"""Centralized configuration for file paths and constants."""
from pathlib import Path

# Project root directory (3 levels up from this file: gary/src/gary/config.py)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RESUME_PATH = DATA_DIR / "resume.json"
HEADER_PATH = DATA_DIR / "header.json"

# Output directories
RESUMES_DIR = PROJECT_ROOT / "resumes"

# Template directories
TEMPLATES_DIR = PROJECT_ROOT / "templates"
RESUME_WORD_TEMPLATE = TEMPLATES_DIR / "resume_word_template.docx"

# Google Sheets configuration
DEFAULT_WORKSHEET_NAME = "Sheet1"
CREDENTIALS_FILE = "googleSheetsCredentials.json"