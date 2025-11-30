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