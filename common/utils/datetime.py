from datetime import datetime
from pytz import timezone


def time_hour(dt: datetime, tz: str) -> str:
    return dt.astimezone(timezone(tz)).strftime("%H:%M")
