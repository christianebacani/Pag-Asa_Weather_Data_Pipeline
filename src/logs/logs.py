'''
    Data Pipeline Logs
'''
import sys
import os
sys.path.insert(0, os.path.abspath('src'))

import pandas as pd
from datetime import datetime

from ingest.daily_weather_forecast import init_soup_object
from ingest.daily_weather_forecast import get_issued_datetime
from ingest.daily_weather_forecast import get_synopsis
from ingest.daily_weather_forecast import get_forecast_weather_conditions
from ingest.daily_weather_forecast import get_forecast_wind_and_coastal_water_conditions
from ingest.daily_weather_forecast import get_temperature_and_relative_humidity

def generate_logs(log_message: str) -> None:
    '''
        Function to generate logs based on 
        the ETL Pipeline job/s.
    '''
    format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(format)

    # Generate logs using pandas for logs dataset (csv format)
    logs = pd.read_csv('src/logs/logs.csv')
    logs = pd.concat([logs, pd.DataFrame({'messages': [log_message], 'timestamps': [timestamp]})], ignore_index=True)
    logs.to_csv('src/logs/logs.csv', index=False)

if __name__ == '__main__':
    soup = init_soup_object('https://www.pagasa.dost.gov.ph/weather#daily-weather-forecast')

    if soup is not None:
        issued_datetime = get_issued_datetime(soup)
        synopsis = get_synopsis(soup)
        forecast_weather_conditions = get_forecast_weather_conditions(soup)
        forecast_wind_and_coastal_water_conditions = get_forecast_wind_and_coastal_water_conditions(soup)
        temperature_and_relative_humidity = get_temperature_and_relative_humidity(soup)

    else:
        issued_datetime = ''
        synopsis = ''
        forecast_weather_conditions = {
            'place': [],
            'weather_condition': [],
            'caused_by': [],
            'impacts': []
        }
        forecast_wind_and_coastal_water_conditions = {
            'place': [],
            'speed': [],
            'direction': [],
            'coastal_water': []
        }
        temperature_and_relative_humidity = {
            'maximum_temperature': [],
            'time_of_maximum_temperature': [],
            'minimum_temperature': [],
            'time_of_minimum_temperature': [],
            'maximum_relative_humidity_percentage': [],
            'time_of_maximum_relative_humidity_percentage': [],
            'minimum_relative_humidity_percentage': [],
            'time_of_minimum_relative_humidity_percentage': []
        }

    generate_logs('(DEV): Ingest daily weather forecast data')