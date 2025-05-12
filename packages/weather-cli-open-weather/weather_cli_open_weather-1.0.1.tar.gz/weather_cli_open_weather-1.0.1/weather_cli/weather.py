import requests
import typer
from rich.console import Console
from rich.table import Table
import os
from dotenv import load_dotenv

app = typer.Typer()
console = Console()

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    console.print("[bold red]Error: OPENWEATHER_API_KEY not set in .env file.[/bold red]")
    raise SystemExit(1)


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def fetch_weather(city: str):
    """Fetch the current weather for a city."""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    return response

def fetch_forecast(city: str):
    """Fetch 5-day forecast for a city."""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(FORECAST_URL, params=params)
    return response

@app.command()
def get(city: str):
    """Get the current weather for a city."""
    response = fetch_weather(city)
    
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']

        # Print weather in a pretty table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Condition")
        table.add_column("Temperature (°C)")
        table.add_column("Feels Like (°C)")
        table.add_column("Humidity (%)")
        
        table.add_row(weather, f"{temp}°C", f"{feels_like}°C", f"{humidity}%")
        
        console.print(f"\nWeather in [bold green]{city.title()}[/bold green]:")
        console.print(table)
    else:
        console.print(f"[bold red]Failed to get weather for {city}. Please check the city name.[/bold red]")

@app.command()
def forecast(city: str):
    """Get 5-day weather forecast for a city."""
    response = fetch_forecast(city)
    
    if response.status_code == 200:
        data = response.json()
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Date/Time")
        table.add_column("Condition")
        table.add_column("Temperature (°C)")
        
        for forecast in data['list']:  # Limit to next 5 days' forecast
            dt = forecast['dt_txt']
            weather = forecast['weather'][0]['description']
            temp = forecast['main']['temp']
            
            table.add_row(dt, weather, f"{temp}°C")
        
        console.print(f"\n5-Day Forecast for [bold green]{city.title()}[/bold green]:")
        console.print(table)
    else:
        console.print(f"[bold red]Failed to get forecast for {city}. Please check the city name.[/bold red]")

@app.command()
def help():
    """Show the help message."""
    console.print("[bold cyan]Weather CLI Tool Help[/bold cyan]")
    console.print("\n[bold]Commands:[/bold]")
    console.print("  [bold]weather get <city>[/bold]   Get current weather for the city.")
    console.print("  [bold]weather forecast <city>[/bold]   Get a 5-day forecast for the city.")
    console.print("\n[bold]Example usage:[/bold]")
    console.print("  weather get London")
    console.print("  weather forecast New York")
    console.print("\n[bold]For more information, check the project repository.[/bold]")

if __name__ == "__main__":
    app()
