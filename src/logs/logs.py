'''
    Module for generating logs during the execution of
    ETL pipeline jobs that process data from the
    PAGASA-DOST website.
'''
import sys
import os
sys.path.insert(0, os.path.abspath('src'))

import pandas as pd
from datetime import datetime

from executor.daily_weather_forecast_executor import ingest_daily_weather_forecast
from executor.weather_outlook_for_ph_cities_executor import ingest_weather_outlook_for_ph_cities
from executor.weather_outlook_for_ph_tourist_areas_executor import ingest_weather_outlook_for_ph_tourist_areas
from executor.weekly_weather_outlook_executor import ingest_weekly_weather_outlook

def generate_logs(
    log_message: str
) -> None:
    '''
    Generates logs for ETL
    pipeline jobs that process
    data from the PAGASA-DOST
    website.

    :param log_message: The message to log during ETL pipeline execution
    :type log_message: str
    '''
    format = '%Y-%m-%d %H:%M:%S' # Format: YYYY-MM-DD HH:MM:SS
    now = datetime.now()
    timestamp = now.strftime(format)

    # Generate logs using pandas for logs dataset (csv format)
    logs = pd.read_csv('src/logs/logs.csv')
    logs = pd.concat([
        logs,
        pd.DataFrame({
            'messages': [log_message],
            'timestamps': [timestamp]
        })
    ], ignore_index=True)
    logs.to_csv('src/logs/logs.csv', index=False)

if __name__ == '__main__':
    # Ingest data for daily weather forecast
    ingest_daily_weather_forecast()
    generate_logs(
        '(DEV): Ingest the data for the daily weather forecast.'
    )

    # Ingest data for weather outlook for selected Philippine cities
    ingest_weather_outlook_for_ph_cities()
    generate_logs(
        '(DEV): Ingest the data for the weather outlook for selected Philippine cities.'
    )

    # Ingest data for weather outlook for selected Philippine tourist areas
    ingest_weather_outlook_for_ph_tourist_areas()
    generate_logs(
        '(DEV): Ingest the data for the weather outlook for selected Philippine tourist areas.'
    )

    # Ingest data for weekly weather outlook
    ingest_weekly_weather_outlook()
    generate_logs(
        '(DEV): Ingest the data for the weekly weather outlook.'
    )