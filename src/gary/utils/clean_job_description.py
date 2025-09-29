import re
import unicodedata


def clean_job_description(text: str) -> str:
    """
    Clean and normalize job description text for AI model input.

    Args:
        text: Raw job description text
    Returns:
        str: Cleaned job description text
    """
    # Normalize unicode characters
    normalized_text = unicodedata.normalize('NFKD', text)

    # Convert to ASCII, ignoring non-ASCII characters
    ascii_text = normalized_text.encode('ascii', 'ignore').decode('ascii')

    # Replace literal \n, \r, \t sequences (escaped strings) with spaces
    cleaned_text = ascii_text.replace('\\n', ' ').replace('\\r', ' ').replace('\\t', ' ')

    # Replace actual newlines, carriage returns, and tabs with spaces
    cleaned_text = cleaned_text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    # Replace all other whitespace characters (tabs, form feeds, vertical tabs)
    cleaned_text = re.sub(r'[\t\f\v]', ' ', cleaned_text)

    # Remove special characters and extra punctuation (keep basic punctuation)
    cleaned_text = re.sub(r'[^\w\s.,;:!?()\-\']', ' ', cleaned_text)

    # Collapse multiple spaces into single space (this handles all whitespace)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

    # Remove spaces before punctuation
    cleaned_text = re.sub(r'\s+([.,;:!?])', r'\1', cleaned_text)

    # Remove extra whitespace at start and end
    cleaned_text = cleaned_text.strip()

    return cleaned_text