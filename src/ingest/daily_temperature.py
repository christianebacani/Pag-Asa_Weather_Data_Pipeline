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

def extract_top_10_lowest_temp_table_tag(
        soup: BeautifulSoup | None
) -> BeautifulSoup | None:
    '''
    Extracts top 10 lowest temperature table
    tag to get it's corresponding data from the
    daily temperature page of the PAGASA-DOST
    website.

    :param soup: BeautifulSoup object for
        navigating and manipulating the page
        content, or None if extraction fails
    :type soup: BeautifulSoup | None

    :return: Top 10 lowest temperature table
        HTML tag, or None if extraction fails
    :rtype: BeautifulSoup | None
    '''
    # We need to check if the BeautifulSoup object is missing
    if soup is None:
        return None

    # Extract HTML tags to get the data for the top 10 lowest temperature table
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    top_10_lowest_temp_table_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-md-6'
        }
    )
    div_tag_with_panel_class = top_10_lowest_temp_table_tag.find('div', attrs={'class': 'panel'})
    top_10_lowest_temp_table_tag = div_tag_with_panel_class

    return top_10_lowest_temp_table_tag

def extract_top_10_lowest_temp_recorded_date(
        top_10_lowest_temp_table_tag: BeautifulSoup | None
) -> str:
    '''
    Extracts the recorded date of the top 10 lowest
    temperature table from the daily temperature page
    of the PAGASA-DOST website.

    :param lowest_temperature_table_tag: Top 10 lowest
        temperature table HTML tag, or None if extration
        fails
    :type lowest_temperature_table_tag: BeautifulSoup | None

    :return: Recorded date of the top 10 lowest temperature
        table
    :rtype: str
    '''
    lowest_temperature_recorded_date = ''

    # We need to check if the top 10 lowest temperature table HTML tag is missing
    if top_10_lowest_temp_table_tag is None:
        return lowest_temperature_recorded_date

    # We need to check if the top 10 lowest teperature table HTML tag is missing
    if top_10_lowest_temp_table_tag is None:
        return lowest_temperature_recorded_date

    lowest_temperature_header_tag = top_10_lowest_temp_table_tag.find(
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

def extract_top_10_lowest_temp_station_names(
        top_10_lowest_temp_table_tag: BeautifulSoup | None
) -> list[str]:
    '''
    Extracts the list of station names from the the top 10
    lowest temperature table of the daily temperature page
    from the PAGASA-DOST website.

    :param lowest_temperature_table_tag: Top 10 lowest
        temperature table HTML tag, or None if extration fails
    :type lowest_temperature_table_tag: BeautifulSoup | None

    :return: List of station names from the top 10 lowest
        temperature table
    :rtype: list[str]
    '''
    top_10_lowest_temp_station_names = []

    # We need to check if the top 10 lowest temperature table HTML tag is missing
    if top_10_lowest_temp_table_tag is None:
        return top_10_lowest_temp_station_names
    
    tbody_tag = top_10_lowest_temp_table_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return top_10_lowest_temp_station_names

    # Use find_all() method to access all station names
    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    # Loop through rows containing HTML tags to extract all station names from top 10 lowest temp table
    for table_row_tag in list_of_all_table_row_tags:
        station_name_tag = table_row_tag.find('td')
        station_name = str(station_name_tag.text).strip()
        top_10_lowest_temp_station_names.append([station_name])

    return top_10_lowest_temp_station_names