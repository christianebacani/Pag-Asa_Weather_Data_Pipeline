'''
    Daily Weather Forecast Module
'''
import requests
import os
import json
from bs4 import BeautifulSoup

def extract_daily_weather_forecast_soup(url: str) -> BeautifulSoup | None:
    '''
        Function to extract beautiful soup object of daily weather
        forecast from the website of pag-asa dost.
    '''
    response = requests.get(url)

    if response.status_code != 200: # We need to check if the status code of the response for the request is unsuccessful
        return None

    soup = BeautifulSoup(response.text, 'html.parser') # Parse as a Beautiful Soup Object
    return soup

def extract_daily_weather_forecast_issued_datetime(soup: BeautifulSoup) -> str:
    '''
        Function to extract the issued datetime of daily weather forecast
        from pag-asa dost website.
    '''
    issued_datetime = ''

    # Extract the necessary html tags to get the issued datetime of daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_tag = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    bold_tag = issued_datetime_tag.find('b')

    if bold_tag is not None: # We need to check if the bold_tag is not missing
        issued_datetime = str(bold_tag.text).strip()

    return issued_datetime

def save_daily_forecast_issued_datetime_to_json(daily_weather_forecast_issued_datetime: str) -> None:
    '''
        Function to save daily weather forecast issued datetime to a dedicated json file 
        of the raw/ directory from your local machine.
    '''
    # Create a dictionary that stores daily weather forecast issued datetime
    data = {
        "issued_datetime": daily_weather_forecast_issued_datetime
    }

    # Save the dictionary to the json file using open() method and json module
    with open('data/raw/daily_weather_forecast_issued_datetime.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    json_file.close()

def extract_synopsis(soup: BeautifulSoup) -> str:
    '''
        Function to extract the synopsis of the
        daily weather forecast from the website
        of pag-asa dost.
    '''