"""Core timestamp conversion logic."""

from datetime import datetime, timezone
from typing import Optional, Union
import pytz
from dateutil import parser
from dateutil.relativedelta import relativedelta


class TimestampConverter:
    """Handles all timestamp format conversions."""

    @staticmethod
    def unix_to_datetime(timestamp: Union[int, float], tz: str = "UTC") -> datetime:
        """Convert Unix timestamp to datetime object."""
        if timestamp > 1e12:
            timestamp = timestamp / 1000
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        if tz != "UTC":
            target_tz = pytz.timezone(tz)
            dt = dt.astimezone(target_tz)
        return dt

    @staticmethod
    def datetime_to_unix(dt: datetime, milliseconds: bool = False) -> Union[int, float]:
        """Convert datetime to Unix timestamp."""
        timestamp = dt.timestamp()
        return int(timestamp * 1000) if milliseconds else int(timestamp)

    @staticmethod
    def parse_timestamp(value: str, tz: str = "UTC") -> datetime:
        """Parse various timestamp formats automatically."""
        try:
            timestamp = float(value)
            return TimestampConverter.unix_to_datetime(timestamp, tz)
        except ValueError:
            dt = parser.parse(value)
            if dt.tzinfo is None:
                dt = pytz.timezone(tz).localize(dt)
            return dt

    @staticmethod
    def to_iso8601(dt: datetime) -> str:
        """Convert datetime to ISO 8601 format."""
        return dt.isoformat()

    @staticmethod
    def to_rfc3339(dt: datetime) -> str:
        """Convert datetime to RFC 3339 format."""
        return dt.strftime("%Y-%m-%dT%H:%M:%S%z")

    @staticmethod
    def to_custom(dt: datetime, fmt: str) -> str:
        """Convert datetime using custom strftime format."""
        return dt.strftime(fmt)

    @staticmethod
    def convert_timezone(dt: datetime, target_tz: str) -> datetime:
        """Convert datetime to different timezone."""
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        target = pytz.timezone(target_tz)
        return dt.astimezone(target)

    @staticmethod
    def relative_time(dt: datetime, reference: Optional[datetime] = None) -> str:
        """Generate human-readable relative time string."""
        if reference is None:
            reference = datetime.now(timezone.utc)
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        if reference.tzinfo is None:
            reference = pytz.utc.localize(reference)

        delta = relativedelta(reference, dt)
        future = dt > reference

        if abs((reference - dt).total_seconds()) < 60:
            return "just now"

        parts = []
        if delta.years:
            parts.append(f"{delta.years} year{'s' if delta.years != 1 else ''}")
        if delta.months:
            parts.append(f"{delta.months} month{'s' if delta.months != 1 else ''}")
        if delta.days:
            parts.append(f"{delta.days} day{'s' if delta.days != 1 else ''}")
        if delta.hours and not parts:
            parts.append(f"{delta.hours} hour{'s' if delta.hours != 1 else ''}")
        if delta.minutes and not parts:
            parts.append(f"{delta.minutes} minute{'s' if delta.minutes != 1 else ''}")

        if not parts:
            return "just now"

        time_str = ", ".join(parts[:2])
        return f"in {time_str}" if future else f"{time_str} ago"