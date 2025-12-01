'''
    Module to ingest daily temperature
    including top 10 lowest and top 10
    highest temperatures recorded across
    different weather stations from the
    PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Creates the data/raw/daily_temperature/
        subdirectory to store JSON files for top
        10 lowest and top 10 highest temperature
        data ingested from the daily temperature
        page of PAGASA-DOST website.
    '''
    # Create the data/raw/daily_temperature/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/daily_temperature'):
        os.makedirs('data/raw/daily_temperature')

def extract_beautiful_soup_object(
        url: str
) -> BeautifulSoup | None:
    '''
    Extracts the BeautifulSoup object of
    the daily temperature page from the
    PAGASA-DOST website.

    :param url: URL of the PAGASA-DOST page
        containing the daily temperature
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

def extract_lowest_temperature_recorded_date(
        soup: BeautifulSoup
) -> str:
    '''
    Extracts the recorded date for the top 10
    lowest temperature table from the daily
    temperature page of PAGASA-DOST website.

    :param soup: BeautifulSoup object for
        navigating and manipulating the page
        content
    :type soup: BeautifulSoup
    '''