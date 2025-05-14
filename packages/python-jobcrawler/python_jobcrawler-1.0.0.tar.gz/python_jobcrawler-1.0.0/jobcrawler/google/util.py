import re

from jobcrawler.util import create_logger

from datetime import datetime, timedelta, timezone
import re

log = create_logger("Google")


def find_job_info(jobs_data: list | dict) -> list | None:
    """Iterates through the JSON data to find the job listings"""
    if isinstance(jobs_data, dict):
        for key, value in jobs_data.items():
            if key == "520084652" and isinstance(value, list):
                return value
            else:
                result = find_job_info(value)
                if result:
                    return result
    elif isinstance(jobs_data, list):
        for item in jobs_data:
            result = find_job_info(item)
            if result:
                return result
    return None


def find_job_info_initial_page(html_text: str):
    pattern = f'520084652":(' + r"\[.*?\]\s*])\s*}\s*]\s*]\s*]\s*]\s*]"
    results = []
    matches = re.finditer(pattern, html_text)

    import json

    for match in matches:
        try:
            parsed_data = json.loads(match.group(1))
            results.append(parsed_data)

        except json.JSONDecodeError as e:
            log.error(f"Failed to parse match: {str(e)}")
            results.append({"raw_match": match.group(0), "error": str(e)})
    return results

def parse_relative_date(text: str) -> datetime:
    
    text = text.lower().strip()
    now = datetime.now(timezone.utc)  # current time in UTC

    match = re.match(r"(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago", text)
    if not match:
        raise ValueError(f"Unrecognized time format: '{text}'")

    quantity = int(match.group(1))
    unit = match.group(2)

    if unit == "second":
        delta = timedelta(seconds=quantity)
    elif unit == "minute":
        delta = timedelta(minutes=quantity)
    elif unit == "hour":
        delta = timedelta(hours=quantity)
    elif unit == "day":
        delta = timedelta(days=quantity)
    elif unit == "week":
        delta = timedelta(weeks=quantity)
    elif unit == "month":
        delta = timedelta(days=30 * quantity)
    elif unit == "year":
        delta = timedelta(days=365 * quantity)

    return now - delta
