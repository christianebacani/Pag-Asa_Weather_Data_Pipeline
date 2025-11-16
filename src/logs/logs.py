'''
    Data Pipeline Logs
'''
import sys
import os
sys.path.insert(0, os.path.abspath('src'))

import pandas as pd
from datetime import datetime

from ingest.daily_weather_forecast import get_daily_weather_forecast_soup
from ingest.daily_weather_forecast import get_daily_forecast_issued_datetime
from ingest.daily_weather_forecast import get_synopsis
from ingest.daily_weather_forecast import get_forecast_weather_conditions
from ingest.daily_weather_forecast import get_forecast_wind_and_coastal_water_conditions
from ingest.daily_weather_forecast import get_temperature_and_relative_humidity

from ingest.weather_outlook_for_selected_ph_cities import get_ph_city_weather_outlook_soup
from ingest.weather_outlook_for_selected_ph_cities import get_ph_city_outlook_issued_datetime

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
    # Fetch the necessary data from the web-page contains of daily weather forecast
    daily_weather_forecast_soup = get_daily_weather_forecast_soup('https://www.pagasa.dost.gov.ph/weather#daily-weather-forecast')
    daily_forecast_issued_datetime = get_daily_forecast_issued_datetime(daily_weather_forecast_soup)
    synopsis = get_synopsis(daily_weather_forecast_soup)
    forecast_weather_conditions = get_forecast_weather_conditions(daily_weather_forecast_soup)
    forecast_wind_and_coastal_water_conditions = get_forecast_wind_and_coastal_water_conditions(daily_weather_forecast_soup)
    temperature_and_relative_humidity = get_temperature_and_relative_humidity(daily_weather_forecast_soup)
    generate_logs('(DEV): Ingest daily weather forecast data.')

    # Fetch the necessary data from the web-page contains of weather outlook for selected ph cities
    ph_city_weather_outlook_soup = get_ph_city_weather_outlook_soup('https://www.pagasa.dost.gov.ph/weather/weather-outlook-selected-philippine-cities')
    ph_city_outlook_issued_datetime = get_ph_city_outlook_issued_datetime(ph_city_weather_outlook_soup)
    generate_logs('(DEV): Ingest weather outlook for selected ph cities data.')