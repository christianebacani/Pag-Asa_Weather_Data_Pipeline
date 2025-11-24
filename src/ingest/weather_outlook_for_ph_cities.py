'''
    Module to ingest the data of the weather outlook for
    selected Philippine cities from the PAGASA-DOST website.
'''
import requests
import os
import json
from bs4 import BeautifulSoup

def create_subdir() -> None:
    '''
        Function to create data/raw/weather_outlook_for_ph_cities/
        subdirectory to store dedicated json files
        for the ingested data of weather outlook for selected
        Philippine cities from the PAGASA-DOST website.
    '''
    # Create the data/raw/weather_outlook_for_ph_cities/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weather_outlook_for_ph_cities'):
        os.makedirs('data/raw/weather_outlook_for_ph_cities')

def extract_beautiful_soup_object(url: str) -> BeautifulSoup | None:
    '''
        Function to extract the BeautifulSoup object of weather 
        outlook for selected Philippine cities from the PAGASA-DOST 
        website.
    '''
    response = requests.get(url)

    # We need to check if the status code of the response for the request is unsuccessful
    if response.status_code != 200:
        return None
    
    # Parse as a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_issued_datetime(soup: BeautifulSoup) -> str:
    '''
        Function to extract the issued datetime of
        weather outlook for selected Philippine cities 
        from the PAGASA-DOST website.
    '''
    issued_datetime = ''

    # Extract the necessary html tags to get the issued datetime of weather outlook for selected Philippine cities
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_and_valid_period_tag = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    # We need to check if the div_tag_with_validity_class is not missing
    if div_tag_with_validity_class is not None:
        issued_datetime_tag = div_tag_with_validity_class.find('b')
        issued_datetime = str(issued_datetime_tag.text).strip()
        issued_datetime = ' '.join(issued_datetime.split()) # Using split() method to remove extra whitespaces in between words

    return issued_datetime

def save_issued_datetime_to_json(issued_datetime: str) -> None:
    '''
        Function to save the issued datetime of weather outlook for
        selected Philippine cities to a dedicated json file of the 
        data/raw/weather_outlook_for_ph_cities/ subdirectory from your local machine.
    '''
    # Create a dictionary that stores the issued datetime of weather outlook for selected Philippine cities
    data = {
        "issued_datetime": issued_datetime
    }

    # Save the dictionary to a json file using open() method and json module
    with open('data/raw/weather_outlook_for_ph_cities/issued_datetime.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_valid_period(soup: BeautifulSoup) -> str:
    '''
        Function to extract the valid period of weather
        outlook for selected Philippine cities from the
        PAGASA-DOST website.
    '''
    valid_period = ''

    # Extract the necessary html tags to get the valid period of weather outlook for selected Philippine cities
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_and_valid_period_tag = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    # We need to check if the div_tag_with_validity_class is not missing
    if div_tag_with_validity_class is not None:
        valid_period_tag = div_tag_with_validity_class.find_all('b')[1]
        valid_period = str(valid_period_tag.text).strip()

    return valid_period

def save_valid_period_to_json(valid_period: str) -> None:
    '''
        Function to save the valid period of weather outlook for
        selected Philippine cities to a dedicated json file of the 
        data/raw/weather_outlook_for_ph_cities/ subdirectory from your local machine.
    '''
    # Create a dictionary that stores the valid period of weather outlook for selected Philippine cities
    data = {
        "valid_period": valid_period
    }

    # Save the dictionary to a json file using open() method and json module
    with open('data/raw/weather_outlook_for_ph_cities/valid_period.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    json_file.close()