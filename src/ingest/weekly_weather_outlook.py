'''
    Module to ingest weekly weather outlook
    from the PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Creates the data/raw/weekly_weather_outlook/
        subdirectory to store JSON files for weekly
        weather outlook data ingested from the PAGASA-
        DOST website.
    '''
    # Create the data/raw/weekly_weather_outlook/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weekly_weather_outlook'):
        os.makedirs('data/raw/weekly_weather_outlook')
    
def extract_beautiful_soup_object(
        url: str
) -> BeautifulSoup | None:
    '''
    Extracts the BeautifulSoup object of the
    weekly weather outlook page from the
    PAGASA-DOST website.

    :param url: URL of the PAGASA-DOST page
    containing the weekly weather outlook
    :type url: str

    :return: BeautifulSoup object for navigating
    and manipulating the page content, or None if
    extraction fails
    :rtype: BeautifulSoup | None
    '''
    response = requests.get(url)

    # We need to check if the status code of the response for the request is unsuccessful
    if response.status_code != 200:
        return None
    
    # Parse as a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_issued_datetime(
        soup: BeautifulSoup
) -> str:
    '''
    Extracts the issued datetime of weekly
    weather outlook from the PAGASA-DOST
    website.

    :param soup: BeautifulSoup object for navigating
    and manipulating the page content
    :type soup: BeautifulSoup

    :return: Issued datetime of the weekly weather
    outlook
    :rtype: str
    '''
    issued_datetime = ''

    # Extract HTML tags for issued datetime of the weekly weather outlook
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_and_valid_period_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12 issue'
        }
    )
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find(
        'div',
        attrs={
            'class': 'validity'
        }
    )
    
    # We need to check if the div_tag_with_validity_class is not missing
    if div_tag_with_validity_class is not None:
        issued_datetime_tag = div_tag_with_validity_class.find('b')
        issued_datetime = str(issued_datetime_tag.text).strip()
    
    return issued_datetime

def save_issued_datetime_to_json(
        issued_datetime: str
) -> None:
    '''
    Saves the issued datetime of the
    weekly weather outlook to a JSON
    file in the data/raw/weeekly_weather_outlook/
    subdirectory on the local machine.

    :param issued_datetime: Issued datetime
    of the weekly weather outlook
    :type issued_datetime: str
    '''
    # Create a dictionary to store issued datetime of the weekly weather outlook
    data = {
        "issued_datetime": issued_datetime
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/weekly_weather_outlook/issued_datetime.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)
    
    json_file.close()

def extract_valid_period(
        soup: BeautifulSoup
) -> str:    
    '''
    Extracts the valid period of the weekly
    weather outlook from the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating
    and manipulating the page content
    :type soup: BeautifulSoup

    :return: Valid period of the weekly weather outlook
    :rtype: str
    '''
    valid_period = ''

    # Extract HTML tags for valid period of the weekly weather outlook
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_and_valid_period_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12 issue'
        }
    )
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find(
        'div',
        attrs={
            'class': 'validity'
        }
    )
    
    # We need to check if the div_tag_with_validity_class is not missing
    if div_tag_with_validity_class is not None:
        valid_period_tag = div_tag_with_validity_class.find_all('b')
        valid_period = str(valid_period_tag.text).strip()
    
    return valid_period