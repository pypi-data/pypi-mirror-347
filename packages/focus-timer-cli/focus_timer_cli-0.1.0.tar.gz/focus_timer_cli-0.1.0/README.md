# focus-timer-cli

A simple command-line focus timer to help you stay productive using the Pomodoro technique or custom intervals.

## Features

- Start a focus timer for a specified number of minutes
- Simple CLI interface
- Motivational banner display

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/HARIOM-JHA01/focus-timer-cli.git
   cd focus-timer-cli
   ```

2. (Recommended) Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install in editable mode:
   ```sh
   uv pip install --editable .
   ```

## Usage

To start a focus timer for 25 minutes:
```sh
focus-timer start 25
```

Replace `25` with any number of minutes you want.

## Requirements

- Python 3.11+
- [Typer](https://typer.tiangolo.com/)
- [Rich](https://rich.readthedocs.io/)
- [Click](https://click.palletsprojects.com/)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License

MIT
