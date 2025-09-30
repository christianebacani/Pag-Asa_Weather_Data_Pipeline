'''
    Data Pipeline Logs
'''
import sys
import os
sys.path.append(os.path.abspath('src'))
import pandas as pd
from datetime import datetime
from ingest.ingest import scrape_daily_weather_forecast_data
from ingest.ingest import scrape_weather_outlook_for_selected_ph_cities_data
from ingest.ingest import scrape_asian_cities_weather_forecast_data
from ingest.ingest import scrape_weather_outlook_for_selected_tourist_areas_data
from ingest.ingest import scrape_weekly_weather_outlook_data
from ingest.ingest import scrape_daily_temperature_data

def generate_logs_from_pipeline_job(job: str) -> None:
    '''
        Generate function to generate logs
        when executing different jobs of
        the pipeline
    '''
    format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(format)

    # Generate data pipeline logs
    logs = pd.read_csv('src/logs/logs.csv')
    logs = pd.concat([logs, pd.DataFrame({'jobs': [job], 'timestamps': [timestamp]})], ignore_index=True)
    logs.to_csv('src/logs/logs.csv', index=False)

if __name__ == '__main__':
    # Weather Data
    # daily_weather_forecast = scrape_daily_weather_forecast_data('https://www.pagasa.dost.gov.ph/weather#daily-weather-forecast')
    # weather_outlook_for_selected_ph_cities = scrape_weather_outlook_for_selected_ph_cities_data('https://www.pagasa.dost.gov.ph/weather/weather-outlook-selected-philippine-cities')
    # asian_cities_weather_forecast = scrape_asian_cities_weather_forecast_data('https://www.pagasa.dost.gov.ph/weather/weather-asian-cities-weather-forecast')
    # weather_outlook_for_selected_tourist_areas = scrape_weather_outlook_for_selected_tourist_areas_data('https://www.pagasa.dost.gov.ph/weather/weather-outlook-selected-tourist-areas')
    # weekly_weather_outlook = scrape_weekly_weather_outlook_data('https://www.pagasa.dost.gov.ph/weather/weather-outlook-weekly')
    scrape_daily_temperature_data('https://www.pagasa.dost.gov.ph/weather/low-high-temperature')