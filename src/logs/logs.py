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
    # daily_weather_forecast = scrape_daily_weather_forecast_data('https://www.pagasa.dost.gov.ph/weather#daily-weather-forecast')
    
    # TODO: Debug the return value of this function
    weather_outlook_for_selected_ph_cities = scrape_weather_outlook_for_selected_ph_cities_data('https://www.pagasa.dost.gov.ph/weather/weather-outlook-selected-philippine-cities')