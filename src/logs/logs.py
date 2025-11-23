'''
    Module to generate logs when executing different jobs
    of the etl pipeline for processing the data from the
    website of pag-asa dost.
'''
import sys
import os
sys.path.insert(0, os.path.abspath('src'))

import pandas as pd
from datetime import datetime

from executor.daily_weather_forecast_executor import ingest_data_of_daily_weather_forecast

def generate_logs(log_message: str) -> None:
    '''
        Function to generate logs when executing
        different jobs of the etl pipeline for
        processing the data from the website of
        pag-asa dost.
    '''
    format = '%Y-%m-%d %H:%M:%S' # Format: YYYY-MM-DD HH:MM:SS
    now = datetime.now()
    timestamp = now.strftime(format)

    # Generate logs using pandas for logs dataset (csv format)
    logs = pd.read_csv('src/logs/logs.csv')
    logs = pd.concat([logs, pd.DataFrame({'messages': [log_message], 'timestamps': [timestamp]})], ignore_index=True)
    logs.to_csv('src/logs/logs.csv', index=False)

if __name__ == '__main__':
    ingest_data_of_daily_weather_forecast()
    generate_logs('(DEV): Ingest the data for the daily weather forecast.')