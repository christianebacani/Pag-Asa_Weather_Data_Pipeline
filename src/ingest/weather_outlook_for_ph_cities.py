'''
    Module to ingest the data of the weather outlook for the
    selected philippine cities from the website of pag-asa dost.
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
        philippine cities from the website of pag-asa dost.
    '''
    # Create the data/raw/weather_outlook_for_ph_cities/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weather_outlook_for_ph_cities'):
        os.makedirs('data/raw/weather_outlook_for_ph_cities')

def extract_beautiful_soup_object(url: str) -> BeautifulSoup | None:
    '''
        Function to extract beautiful soup object of weather outlook for
        the selected philippine cities from the website of pag-asa dost.
    '''
    response = requests.get(url)

    # We need to check if the status code of the response for the request is unsuccessful
    if response.status_code != 200:
        return None
    
    # Parse as a Beautiful Soup Object
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_issued_datetime(soup: BeautifulSoup) -> str:
    '''
        Function to extract the issued datetime of weather 
        outlook for selected philippine cities from the 
        website of pag-asa dost.
    '''
    issued_datetime = ''

    # Extract the necessary html tags to get the issued datetime of weather outlook for the selected philippine cities
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_and_valid_period_tag = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    # We need to check if the div_tag_with_validity_class is not missing
    if div_tag_with_validity_class is not None:
        issued_datetime_tag = div_tag_with_validity_class.find('b')
        issued_datetime = str(issued_datetime_tag.text).strip()
        issued_datetime = ' '.join(issued_datetime.split()) # Using split() method to remove extra whitespace in between words

    return issued_datetime

def save_issued_datetime_to_json(issued_datetime: str) -> None:
    '''
        Function to save issued datetime of weather outlook for
        selected philippine cities to a dedicated json file of the 
        data/raw/weather_outlook_for_ph_cities/ subdirectory from your local machine.
    '''
    # Create a dictionary that stores issued datetime of the weather outlook for the selected philippine cities
    data = {
        "issued_datetime": issued_datetime
    }

    # Save the dictionary to a json file using open() method and json module
    with open('data/raw/weather_outlook_for_ph_cities/issued_datetime.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()