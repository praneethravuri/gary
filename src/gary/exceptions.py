"""Custom exceptions for the Gary application."""


class GaryBaseException(Exception):
    """Base exception for all Gary application errors."""

    pass


class DataLoadError(GaryBaseException):
    """Raised when data loading from files or external sources fails."""

    pass


class GoogleSheetsError(GaryBaseException):
    """Raised when Google Sheets operations fail."""

    pass


class ResumeGenerationError(GaryBaseException):
    """Raised when resume generation fails."""

    pass


class CrewExecutionError(GaryBaseException):
    """Raised when CrewAI execution fails."""

    pass
