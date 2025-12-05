'''
    Module to ingest regional forecast
    specifically for the Province of Tarlac
    and Bataan from the PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Creates the
        data/raw/regional_forecast/
        subdirectory to store JSON files
        for regional forecast specifically
        for the Province of Tarlac and Bataan
        from the PAGASA-DOST website.
    '''
    # Create the data/raw/regional_forecast/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/regional_forecast'):
        os.makedirs('data/raw/regional_forecast')

def extract_beautiful_soup_object(
        url: str
) -> BeautifulSoup | None:
    '''
    Extracts the BeautifulSoup object
    of the regional forecast specifically
    for the Province of Tarlac and Bataan
    from the PAGASA-DOST website.

    :param url: URL of the PAGASA-DOST
        page containing the regional
        forecast
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

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_issued_datetime_of_tarlac_weather_forecast(
        soup: BeautifulSoup | None
) -> str:
    '''
    Extracts the issued datetime of the regional forecast
    specifically for the Province of Tarlac from the
    PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating
        and manipulating the page content, or
        None if extraction fails
    :type soup: BeautifulSoup | None

    :return: Issued datetime of the weather forecast for the
        Province of Tarlac
    :rtype: str
    '''
    issued_datetime = ''