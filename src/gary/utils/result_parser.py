"""Utility for parsing CrewAI result outputs."""
import json
import re
from typing import Any, Dict


def parse_crew_result(result: Any) -> Dict[str, Any]:
    """
    Parse CrewAI result into a dictionary.

    Handles multiple result types from CrewAI:
    - CrewOutput objects with 'raw' attribute
    - String JSON (with potential extra text)
    - Dictionary objects
    - Other objects (returned as-is)

    Args:
        result: Result from CrewAI kickoff

    Returns:
        Dict[str, Any]: Parsed result as dictionary

    Raises:
        ValueError: If result cannot be parsed
    """
    # Handle CrewOutput objects with 'raw' attribute
    if hasattr(result, 'raw'):
        result = result.raw

    # Handle string results
    if isinstance(result, str):
        # Try to extract JSON from string (handles extra text after JSON)
        result = result.strip()

        # Try parsing as-is first
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            pass

        # Try to find JSON object/array in the string
        # Look for outermost {...} or [...]
        json_match = re.search(r'(\{.*\}|\[.*\])', result, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Could not parse result as JSON: {result[:200]}...")

    # Handle dictionary objects
    if isinstance(result, dict):
        return result

    # Fallback: try to convert to dict if possible
    raise ValueError(f"Unsupported result type: {type(result)}")