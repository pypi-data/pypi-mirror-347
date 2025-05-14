from jobcrawler.model import Compensation, CompensationInterval, Location, JobType
from datetime import datetime, timedelta
from tzlocal import get_localzone
import pytz


def parse_compensation(data: dict) -> Compensation | None:
    pay_period = data.get("payPeriod")
    adjusted_pay = data.get("payPeriodAdjustedPay")
    currency = data.get("payCurrency", "USD")
    if not pay_period or not adjusted_pay:
        return None

    interval = None
    if pay_period == "ANNUAL":
        interval = CompensationInterval.YEARLY
    elif pay_period:
        interval = CompensationInterval.get_interval(pay_period)
    min_amount = int(adjusted_pay.get("p10") // 1)
    max_amount = int(adjusted_pay.get("p90") // 1)
    return Compensation(
        interval=interval,
        min_amount=min_amount,
        max_amount=max_amount,
        currency=currency,
    )


def get_job_type_enum(job_type_str: str) -> list[JobType] | None:
    for job_type in JobType:
        if job_type_str in job_type.value:
            return [job_type]


def parse_location(location_name: str) -> Location | None:
    if not location_name or location_name == "Remote":
        return
    city, _, state = location_name.partition(", ")
    return Location(city=city, state=state)


def get_cursor_for_page(pagination_cursors, page_num):
    for cursor_data in pagination_cursors:
        if cursor_data["pageNumber"] == page_num:
            return cursor_data["cursor"]

from datetime import date, datetime, time

def get_midnight_utc_date(age_in_days: int, fallback_tz='America/New_York') -> str:
    try:
        local_tz = datetime.datetime.now().astimezone().tzinfo
    except Exception:
        local_tz = pytz.timezone(fallback_tz)
    
    now_local = datetime.now(local_tz)
    midnight_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=age_in_days)
    midnight_utc = midnight_local.astimezone(pytz.UTC)
    return midnight_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
