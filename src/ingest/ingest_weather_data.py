'''
    Data Ingestion Module to ingest
    Daily Weather Forecast.
'''
import requests

def ingest_daily_weather_forecast_data(url: str) -> dict:
    '''
        Function to ingest daily weather forecast data.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print('The website does not allow to be scraped!')
        return {}