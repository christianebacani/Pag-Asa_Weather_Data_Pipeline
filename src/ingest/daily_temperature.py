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

def extract_lowest_temp_table_tag(
        soup: BeautifulSoup
) -> BeautifulSoup | None:
    '''
    Extracts top 10 lowest temperature table
    tag to get it's corresponding data from the
    PAGASA-DOST website.

    :param soup: BeautifulSoup object for
        navigating and manipulating the page
        content
    :type soup: BeautifulSoup

    :return: Top 10 lowest temperature table
        HTML tag
    :rtype: BeautifulSoup | None
    '''
    # Extract HTML tags to get the data for the top 10 lowest temperature table
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    lowest_temperature_table_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-md-6'
        }
    )
    div_tag_with_panel_class = lowest_temperature_table_tag.find('div', attrs={'class': 'panel'})
    lowest_temperature_table_tag = div_tag_with_panel_class

    return lowest_temperature_table_tag