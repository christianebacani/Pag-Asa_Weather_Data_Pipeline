'''
    Data Ingestion Module to ingest
    Daily Weather Forecast.
'''
import requests
from bs4 import BeautifulSoup

def ingest_daily_weather_forecast_data(url: str) -> dict:
    '''
        Function to ingest daily weather forecast data.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print('The website does not allow to be scraped!')
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    div_tag_with_row_class = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'row'})