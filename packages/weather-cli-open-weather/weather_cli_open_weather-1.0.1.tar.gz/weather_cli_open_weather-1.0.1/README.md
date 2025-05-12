# Weather CLI

A simple command-line tool to fetch and display current weather information for any city using the OpenWeatherMap API.

## Features
- Get current weather for any city
- Colorful output using Rich
- Easy to use and extend

## Requirements
- Python 3.8+
- [OpenWeatherMap API key](https://openweathermap.org/api)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/HARIOM-JHA01/weather-cli.git
   cd weather-cli
   ```
2. Install dependencies:
   ```sh
   uv pip install -e .
   # or
   pip install -e .
   ```

## Usage

Set your OpenWeatherMap API key in a `.env` file:

```
OPENWEATHER_API_KEY=your_api_key_here
```

Get weather for a city:

```sh
weather get London
```

Show help:

```sh
weather --help
```

## Development
- All source code is in the `weather_cli/` directory.
- Tests can be added in a `tests/` directory.

## License
MIT License. See [LICENSE.txt](LICENSE.txt).
