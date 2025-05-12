from setuptools import setup, find_packages

setup(
    name="weather_cli_open_weather",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        'requests',
        'typer',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'weather=weather_cli.weather:app',
        ],
    },
)
