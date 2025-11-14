'''
    Daily Weather Forecast Module
'''
import requests
from bs4 import BeautifulSoup

def init_soup_object(url: str) -> BeautifulSoup | None:
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

def get_issued_datetime(soup: BeautifulSoup) -> str:
    '''
        Function to get issued datetime
        from the daily weather forecast
    '''
    issued_datetime = ''

    issued_datetime_tag = soup.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    bold_tag = issued_datetime_tag.find('b')

    if bold_tag is not None:
        issued_datetime = str(bold_tag.text).strip()
    
    return issued_datetime