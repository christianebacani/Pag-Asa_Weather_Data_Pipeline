'''
    Weather Outlook for Selected PH Cities Module
'''
import requests
from bs4 import BeautifulSoup

def get_ph_city_weather_outlook_soup(url: str) -> BeautifulSoup | None:
    '''
        Function to get the parsed beautiful soup object to extract
        weather outlook for selected ph cities from pag-asa dost website.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser') # Parse to a Beautiful Soup Object
    return soup

def get_ph_city_outlook_issued_datetime(soup: BeautifulSoup) -> str:
    '''
        Function to get the issued datetime of weather outlook for
        selected ph cities from pag-asa dost website.
    '''
    issued_datetime = ''

    issued_datetime_and_valid_period_tag = soup.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    if div_tag_with_validity_class is not None:
        issued_datetime = div_tag_with_validity_class.find_all('b')[0]
        issued_datetime = str(issued_datetime.text)
        issued_datetime = ' '.join(issued_datetime.split())

    return issued_datetime

def get_ph_city_outlook_valid_period(soup: BeautifulSoup) -> str:
    '''
        Function to get the valid period of weather outlook
        for selected ph cities from pag-asa dost website.
    '''
    valid_period = ''

    issued_datetime_and_valid_period_tag = soup.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    if div_tag_with_validity_class is not None:
        valid_period = div_tag_with_validity_class.find_all('b')[1]
        valid_period = str(valid_period.text).strip()
    
    return valid_period

def get_all_selected_ph_cities(soup: BeautifulSoup) -> list[str]:
    '''
        
    '''