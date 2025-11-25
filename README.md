# timestamp-convert

A CLI utility for converting between timestamp formats with timezone support and batch processing

## Features

- Convert Unix timestamps (seconds/milliseconds) to ISO 8601, RFC 3339, and custom formats
- Parse ISO 8601 and RFC 3339 strings to Unix timestamps
- Convert between timezones with automatic DST handling
- Display human-readable relative time (e.g., '2 hours ago', 'in 3 days')
- Batch process multiple timestamps from stdin or file input
- Support custom output format strings using strftime patterns
- Handle both naive and timezone-aware timestamps
- Detect input format automatically when possible
- Output current timestamp in any supported format
- Colorized terminal output for better readability

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/timestamp-convert.git
cd timestamp-convert

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python using click

## Dependencies

- `click`
- `python-dateutil`
- `pytz`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
