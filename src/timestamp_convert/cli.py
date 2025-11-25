"""CLI interface for timestamp conversion."""

import sys
import click
from datetime import datetime, timezone
from typing import Optional
from .converter import TimestampConverter


@click.group()
@click.version_option()
def cli():
    """Timestamp conversion utility with timezone support."""
    pass


@cli.command()
@click.argument("timestamp", required=False)
@click.option("--to", "-t", default="iso", help="Output format: iso, rfc, unix, unix-ms, custom")
@click.option("--format", "-f", help="Custom strftime format string")
@click.option("--timezone", "-z", default="UTC", help="Target timezone")
@click.option("--from-tz", default="UTC", help="Source timezone for naive timestamps")
def convert(timestamp: Optional[str], to: str, format: Optional[str], timezone: str, from_tz: str):
    """Convert timestamp to specified format."""
    converter = TimestampConverter()

    if timestamp is None:
        dt = datetime.now(timezone.utc)
    else:
        try:
            dt = converter.parse_timestamp(timestamp, from_tz)
        except Exception as e:
            click.echo(click.style(f"Error parsing timestamp: {e}", fg="red"), err=True)
            sys.exit(1)

    if timezone != "UTC":
        dt = converter.convert_timezone(dt, timezone)

    try:
        if to == "iso":
            result = converter.to_iso8601(dt)
        elif to == "rfc":
            result = converter.to_rfc3339(dt)
        elif to == "unix":
            result = str(converter.datetime_to_unix(dt))
        elif to == "unix-ms":
            result = str(converter.datetime_to_unix(dt, milliseconds=True))
        elif to == "custom":
            if not format:
                click.echo(click.style("--format required for custom output", fg="red"), err=True)
                sys.exit(1)
            result = converter.to_custom(dt, format)
        else:
            click.echo(click.style(f"Unknown format: {to}", fg="red"), err=True)
            sys.exit(1)

        click.echo(click.style(result, fg="green"))
    except Exception as e:
        click.echo(click.style(f"Conversion error: {e}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.argument("timestamp")
@click.option("--reference", "-r", help="Reference timestamp (default: now)")
def relative(timestamp: str, reference: Optional[str]):
    """Show relative time (e.g., '2 hours ago')."""
    converter = TimestampConverter()

    try:
        dt = converter.parse_timestamp(timestamp)
        ref_dt = converter.parse_timestamp(reference) if reference else None
        result = converter.relative_time(dt, ref_dt)
        click.echo(click.style(result, fg="cyan"))
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.option("--input", "-i", type=click.File("r"), default=sys.stdin, help="Input file")
@click.option("--to", "-t", default="iso", help="Output format")
@click.option("--timezone", "-z", default="UTC", help="Target timezone")
def batch(input, to: str, timezone: str):
    """Process multiple timestamps from stdin or file."""
    converter = TimestampConverter()

    for line in input:
        line = line.strip()
        if not line:
            continue

        try:
            dt = converter.parse_timestamp(line)
            if timezone != "UTC":
                dt = converter.convert_timezone(dt, timezone)

            if to == "iso":
                result = converter.to_iso8601(dt)
            elif to == "unix":
                result = str(converter.datetime_to_unix(dt))
            else:
                result = converter.to_rfc3339(dt)

            click.echo(f"{line} -> {click.style(result, fg='green')}")
        except Exception as e:
            click.echo(f"{line} -> {click.style(f'ERROR: {e}', fg='red')}")


if __name__ == "__main__":
    cli()