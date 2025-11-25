"""Tests for timestamp converter core functionality."""

import pytest
from datetime import datetime, timezone
import pytz
from timestamp_convert.converter import TimestampConverter


class TestUnixToDatetime:
    """Test Unix timestamp to datetime conversion."""

    def test_seconds_timestamp_utc(self):
        result = TimestampConverter.unix_to_datetime(1609459200)
        assert result.year == 2021
        assert result.month == 1
        assert result.day == 1
        assert result.tzinfo == timezone.utc

    def test_milliseconds_timestamp(self):
        result = TimestampConverter.unix_to_datetime(1609459200000)
        assert result.year == 2021
        assert result.month == 1

    def test_with_timezone(self):
        result = TimestampConverter.unix_to_datetime(1609459200, tz="America/New_York")
        assert result.tzinfo.zone == "America/New_York"

    def test_float_timestamp(self):
        result = TimestampConverter.unix_to_datetime(1609459200.5)
        assert isinstance(result, datetime)


class TestDatetimeToUnix:
    """Test datetime to Unix timestamp conversion."""

    def test_datetime_to_seconds(self):
        dt = datetime(2021, 1, 1, tzinfo=timezone.utc)
        result = TimestampConverter.datetime_to_unix(dt)
        assert result == 1609459200
        assert isinstance(result, int)

    def test_datetime_to_milliseconds(self):
        dt = datetime(2021, 1, 1, tzinfo=timezone.utc)
        result = TimestampConverter.datetime_to_unix(dt, milliseconds=True)
        assert result == 1609459200000
        assert isinstance(result, int)


class TestParseTimestamp:
    """Test automatic timestamp parsing."""

    def test_parse_unix_timestamp(self):
        result = TimestampConverter.parse_timestamp("1609459200")
        assert result.year == 2021

    def test_parse_iso8601(self):
        result = TimestampConverter.parse_timestamp("2021-01-01T00:00:00Z")
        assert result.year == 2021
        assert result.tzinfo is not None

    def test_parse_naive_datetime(self):
        result = TimestampConverter.parse_timestamp("2021-01-01 00:00:00", tz="UTC")
        assert result.year == 2021
        assert result.tzinfo is not None

    def test_parse_invalid_raises_error(self):
        with pytest.raises(Exception):
            TimestampConverter.parse_timestamp("invalid-timestamp")


class TestFormatConversions:
    """Test output format conversions."""

    def test_to_iso8601(self):
        dt = datetime(2021, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        result = TimestampConverter.to_iso8601(dt)
        assert "2021-01-01" in result
        assert "12:30:45" in result

    def test_to_rfc3339(self):
        dt = datetime(2021, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        result = TimestampConverter.to_rfc3339(dt)
        assert "2021-01-01T12:30:45" in result

    def test_to_custom_format(self):
        dt = datetime(2021, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        result = TimestampConverter.to_custom(dt, "%Y-%m-%d")
        assert result == "2021-01-01"


class TestTimezoneConversion:
    """Test timezone conversion."""

    def test_convert_utc_to_eastern(self):
        dt = datetime(2021, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = TimestampConverter.convert_timezone(dt, "America/New_York")
        assert result.tzinfo.zone == "America/New_York"
        assert result.hour == 7

    def test_convert_naive_datetime(self):
        dt = datetime(2021, 1, 1, 12, 0, 0)
        result = TimestampConverter.convert_timezone(dt, "America/New_York")
        assert result.tzinfo is not None


class TestRelativeTime:
    """Test human-readable relative time."""

    def test_just_now(self):
        dt = datetime.now(timezone.utc)
        result = TimestampConverter.relative_time(dt)
        assert result == "just now"

    def test_past_time(self):
        ref = datetime(2021, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        dt = datetime(2021, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        result = TimestampConverter.relative_time(dt, ref)
        assert "ago" in result
        assert "hour" in result

    def test_future_time(self):
        ref = datetime(2021, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        dt = datetime(2021, 1, 1, 14, 0, 0, tzinfo=timezone.utc)
        result = TimestampConverter.relative_time(dt, ref)
        assert "in" in result

    def test_naive_datetime_handling(self):
        dt = datetime(2021, 1, 1, 12, 0, 0)
        ref = datetime(2021, 1, 1, 10, 0, 0)
        result = TimestampConverter.relative_time(dt, ref)
        assert isinstance(result, str)