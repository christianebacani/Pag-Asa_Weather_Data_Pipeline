'''
    Data Pipeline Logs
'''
import sys
import os
sys.path.insert(0, os.path.abspath('src'))

import pandas as pd
from datetime import datetime

from ingest.daily_weather_forecast import extract_daily_weather_forecast_soup

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
    daily_weather_forecast_soup = extract_daily_weather_forecast_soup('https://www.pagasa.dost.gov.ph/weather#daily-weather-forecast')    
    generate_logs('(DEV): Ingest the weather outlook for selected ph cities data.')