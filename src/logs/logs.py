'''
    Module for generating logs when executing different 
    ETL pipeline jobs that process data from the PAGASA-DOST website.
'''
import sys
import os
sys.path.insert(0, os.path.abspath('src'))

import pandas as pd
from datetime import datetime

from executor.daily_weather_forecast_executor import execute_functions_to_ingest_daily_weather_forecast
from executor.weather_outlook_for_ph_cities_executor import execute_functions_to_ingest_weather_outlook_for_ph_cities
from executor.weather_outlook_for_ph_tourist_areas_executor import execute_functions_to_ingest_weather_outlook_for_ph_tourist_areas

def generate_logs(log_message: str) -> None:
    '''
    Function for generating logs when
    executing different ETL Pipeline jobs
    that process data from the PAGASA-DOST
    website.

    :param log_message: Log message when executing ETL Pipeline jobs
    :type log_message: str
    '''
    format = '%Y-%m-%d %H:%M:%S' # Format: YYYY-MM-DD HH:MM:SS
    now = datetime.now()
    timestamp = now.strftime(format)

    # Generate logs using pandas for logs dataset (csv format)
    logs = pd.read_csv('src/logs/logs.csv')
    logs = pd.concat([logs, pd.DataFrame({'messages': [log_message], 'timestamps': [timestamp]})], ignore_index=True)
    logs.to_csv('src/logs/logs.csv', index=False)

if __name__ == '__main__':
    # Ingest data for daily weather forecast
    execute_functions_to_ingest_daily_weather_forecast()
    generate_logs('(DEV): Ingest the data for the daily weather forecast.')

    # Ingest data for weather outlook for selected Philippine cities
    execute_functions_to_ingest_weather_outlook_for_ph_cities()
    generate_logs('(DEV): Ingest the data for the weather outlook for selected Philippine cities.')

    # Ingest data for weather outlook for selected Philippine tourist areas
    execute_functions_to_ingest_weather_outlook_for_ph_tourist_areas()
    generate_logs('(DEV): Ingest the data for the weather outlook for selected Philippine tourist areas.')