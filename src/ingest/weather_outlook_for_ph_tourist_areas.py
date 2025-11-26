'''
    Module to ingest the data of the weather outlook for
    selected Philippine tourist areas from the PAGASA-DOST website.
'''
import os
import requests
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