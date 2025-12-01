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
        page of the PAGASA-DOST website.
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

def extract_lowest_temperature_table_tag(
        soup: BeautifulSoup
) -> BeautifulSoup | None:
    '''
    Extracts top 10 lowest temperature table
    tag to get it's corresponding data from the
    daily temperature page of the PAGASA-DOST
    website.

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

def extract_lowest_temperature_recorded_date(
        lowest_temperature_table_tag: BeautifulSoup
) -> str:
    '''
    Extracts the recorded date of the top 10 lowest
    temperature table from the daily temperature page
    of the PAGASA-DOST website.

    :param lowest_temperature_table_tag: Top 10 lowest
        temperature table HTML tag
    :type lowest_temperature_table_tag: BeautifulSoup

    :return: Recorded date of the top 10 lowest temperature
        table
    :rtype: str
    '''
    lowest_temperature_recorded_date = ''

    # We need to check if the top 10 lowest teperature table HTML tag is missing
    if lowest_temperature_table_tag is None:
        return lowest_temperature_recorded_date

    lowest_temperature_header_tag = lowest_temperature_table_tag.find(
        'div',
        attrs={
            'class': 'panel-heading'
        }
    )
    lowest_temperature_header = str(lowest_temperature_header_tag.text)
    lowest_temperature_recorded_date = lowest_temperature_header.replace(
        'Top 10 Lowest Temperature as of',
        ''
    ).strip()
    
    return lowest_temperature_recorded_date

    # TODO: 
    # - Test the function extract_lowest_temperature_recorded_date
    # - Check every function inside the ingest package to validate if the BeautifulSoup object is missing