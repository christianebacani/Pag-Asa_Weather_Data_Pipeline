'''
    Daily Weather Forecast Module
'''
import requests
from bs4 import BeautifulSoup

def extract_daily_weather_forecast_soup(url: str) -> BeautifulSoup | None:
    '''
        Function to extract beautiful soup object of daily weather
        forecast from pag-asa dost website.
    '''
    response = requests.get(url)

    if response.status_code != 200: # Validate first if the status code of the response is not successful
        return None

    soup = BeautifulSoup(response.text, 'html.parser') # Parse as a Beautiful Soup Object
    return soup