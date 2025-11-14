'''
    Daily Weather Forecast Module
'''
import requests
from bs4 import BeautifulSoup

def init_soup_object(url: str) -> object | None:
    '''
        Function to initialize Beautiful 
        Soup Object from the requested data
        from the website 
        (https://www.pagasa.dost.gov.ph/weather#daily-weather-forecast)
    '''
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup