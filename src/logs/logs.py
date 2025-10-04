'''
    Data Pipeline Logs
'''
import sys
import os
sys.path.append(os.path.abspath('src'))
import pandas as pd
from datetime import datetime
from ingest.ingest_weather_data import scrape_daily_weather_forecast_data
from ingest.ingest_weather_data import scrape_weather_outlook_for_selected_ph_cities_data
from ingest.ingest_weather_data import scrape_asian_cities_weather_forecast_data
from ingest.ingest_weather_data import scrape_weather_outlook_for_selected_tourist_areas_data
from ingest.ingest_weather_data import scrape_weekly_weather_outlook_data
from ingest.ingest_weather_data import scrape_weather_advisory_data
from ingest.ingest_weather_data import scrape_daily_temperature_data
from ingest.ingest_flood_data import scrape_flood_information_data
from ingest.ingest_tropical_cyclone_data import scrape_tropical_cyclone_bulletin_data

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
    '''
    # Weather Data
    daily_weather_forecast_data = scrape_daily_weather_forecast_data('https://www.pagasa.dost.gov.ph/weather#daily-weather-forecast')
    weather_outlook_for_selected_ph_cities_data = scrape_weather_outlook_for_selected_ph_cities_data('https://www.pagasa.dost.gov.ph/weather/weather-outlook-selected-philippine-cities')
    asian_cities_weather_forecast_data = scrape_asian_cities_weather_forecast_data('https://www.pagasa.dost.gov.ph/weather/weather-asian-cities-weather-forecast')
    weather_outlook_for_selected_tourist_areas_data = scrape_weather_outlook_for_selected_tourist_areas_data('https://www.pagasa.dost.gov.ph/weather/weather-outlook-selected-tourist-areas')
    weekly_weather_outlook_data = scrape_weekly_weather_outlook_data('https://www.pagasa.dost.gov.ph/weather/weather-outlook-weekly')
    daily_temperature_data = scrape_daily_temperature_data('https://www.pagasa.dost.gov.ph/weather/low-high-temperature')
    '''
    scrape_weather_advisory_data('https://www.pagasa.dost.gov.ph/weather/weather-advisory')

    '''
    # Flood data
    flood_information_data = scrape_flood_information_data('https://www.pagasa.dost.gov.ph/flood#flood-information')

    # Tropical cyclone data
    # tropical_cyclone_bulletin_data = scrape_tropical_cyclone_bulletin_data('https://www.pagasa.dost.gov.ph/tropical-cyclone/severe-weather-bulletin')
    '''