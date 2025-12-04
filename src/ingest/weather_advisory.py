'''
    Module to ingest weather advisory from the
    PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Creates the data/raw/weather_advisory/
        subdirectory to store JSON files for weather
        advisory from the PAGASA-DOST website.
    '''
    # Create the data/raw/weather_advisory/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weather_advisory'):
        os.makedirs('data/raw/weather_advisory')

def extract_beautiful_soup_object(
        url: str
) -> BeautifulSoup | None:
    '''
    Extracts the BeautifulSoup object
    of the weather advisory from the
    PAGASA-DOST website.

    :param url: URL of the PAGASA-DOST
        page containing the weather
        advisory
    :type url: str

    :return: BeautifulSoup object for navigating
        the page content, or None if extraction
        fails
    :rtype: BeautifulSoup | None
    '''
    response = requests.get(url)

    # We need to check if the status code of the response for the request is unsuccessful
    if response.status_code != 200:
        return None

    # Parse as a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_weather_advisory(
        soup: BeautifulSoup | None
) -> str:
    '''
    Extracts the weather advisory
    from the PAGASA-DOST website.

    :param soup: BeautifulSoup object
        for navigating and manipulating
        the page content, or None if
        extraction fails
    :type soup: BeautifulSoup | None

    :return: Weather Advisory
    :rtype: str
    '''
    weather_advisory = ''

    # We need to check if the BeautifulSoup object is missing
    if soup is None:
        return weather_advisory

    # Extract HTML tags for weather advisory
    div_tag_with_row_marine_class = soup.find('div', attrs={'class': 'row marine'})
    weather_advisory_tag = div_tag_with_row_marine_class.find(
        'div',
        attrs={
            'class': 'weekly-content-adv'
        }
    )

    # We need to check if weather_advisory_tag is missing
    if weather_advisory_tag is None:
        return weather_advisory
    
    iframe_tag = weather_advisory_tag.find('iframe')
    weather_advisory = iframe_tag['src']
    weather_advisory = str(weather_advisory).strip()

    return weather_advisory