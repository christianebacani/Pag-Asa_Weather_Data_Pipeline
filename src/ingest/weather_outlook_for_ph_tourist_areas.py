'''
    Module to ingest the data of the weather outlook for
    selected Philippine tourist areas from the PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir() -> None:
    '''
        Function to create data/raw/weather_outlook_for_ph_tourist_areas/
        subdirectory to store dedicated json files
        for the ingested data of weather outlook for selected
        Philippine tourist areas from the PAGASA-DOST website.
    '''
    # Create the data/raw/weather_outlook_for_ph_cities/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weather_outlook_for_ph_tourist_areas'):
        os.makedirs('data/raw/weather_outlook_for_ph_tourist_areas')

def extract_beautiful_soup_object(url: str) -> BeautifulSoup | None:
    '''
    Function to extract the BeautifulSoup object of weather
    outlook for selected Philippine cities from the PAGASA-DOST 
    website.

    :param url: Url of the PAGASA-DOST website that consist of weather outlook for selected Philippine tourist areas
    :type url: str
    :return: BeautifulSoup object to navigate and manipulate the entire content of the web-page
    :rtype: BeautifulSoup
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
    weather outlook for selected Philippine tourist areas 
    from the PAGASA-DOST website.

    :param soup: BeautifulSoup object to navigate and manipulate the entire content of the web-page
    :type soup: BeautifulSoup

    :return: Issued datetime of weather outlook for selected Philippine tourist areas
    :rtype: str
    '''
    issued_datetime = ''

    # Extract the necessary html tags to get the issued datetime of weather outlook for selected Philippine tourist areas
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_and_valid_period_tag = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    # We need to check if the div_tag_with_validity_class is not missing
    if div_tag_with_validity_class is not None:
        issued_datetime_tag = div_tag_with_validity_class.find('b')
        issued_datetime = str(issued_datetime_tag.text).strip()
    
    return issued_datetime

def save_issued_datetime_to_json(issued_datetime: str) -> None:
    '''
    Function to save the issued datetime of weather outlook for
    selected Philippine tourist areas to a dedicated json file of the 
    data/raw/weather_outlook_for_ph_tourist_areas/ subdirectory from your local machine.

    :param issued_datetime: Issued datetime of weather outlook for selected Philippine tourist areas
    :type issued_datetime: str
    '''
    # Create a dictionary that stores the issued datetime of weather outlook for selected Philippine tourist areas
    data = {
        "issued_datetime": issued_datetime
    }

    # Save the dictionary to a json file using open() method and json module
    with open('data/raw/weather_outlook_for_ph_tourist_areas/issued_datetime.json') as json_file:
        json.dump(data, json_file, indent=4)
    
    json_file.close()