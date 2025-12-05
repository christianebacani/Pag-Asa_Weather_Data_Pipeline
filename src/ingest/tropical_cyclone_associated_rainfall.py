'''
    Module to ingest tropical cyclone
    associated rainfall from the PAGASA-
    DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir():
    '''
        Creates the
        data/raw/tropical_cyclone_associated_rainfall/
        subdirectory to store JSON files for
        tropical cyclone associated rainfall from the
        PAGASA-DOST website.
    '''
    # Create the data/raw/tropical_cyclone_associated_rainfall/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/tropical_cyclone_associated_rainfall'):
        os.makedirs('data/raw/tropical_cyclone_associated_rainfall')

def extract_beautiful_soup_object(
        url: str
) -> BeautifulSoup | None:
    '''
    Extracts the BeautifulSoup object
    of the tropical cyclone associated
    rainfall from the PAGASA-DOST website.

    :param url: URL of the PAGASA-DOST
        page containing the tropical
        cyclone associated rainfall
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

    # Parse as a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_tropical_cyclone_associated_rainfall(
        soup: BeautifulSoup | None
) -> str:
    '''
    Extracts the tropical cyclone associated
    rainfall from the PAGASA-DOST website.

    :param soup: BeautifulSoup object
        for navigating and manipulating
        the page content, or None if
        extraction fails
    :type soup: BeautifulSoup | None

    :return: Tropical Cyclone Associated Rainfall
    :rtype: str
    '''
    tropical_cyclone_associated_rainfall = ''

    # We need to check if the BeautifulSoup object is missing
    if soup is None:
        return tropical_cyclone_associated_rainfall

    # Extract HTML tags for tropical cyclone associated rainfall
    div_tag_with_row_climate_page_class = soup.find('div', attrs={'class': 'row climate-page'})
    tropical_cyclone_associated_rainfall_tag = div_tag_with_row_climate_page_class.find(
        'div',
        attrs={
            'class': 'col-md-12 article-content'
        }
    )
    div_tag_with_panel_class = tropical_cyclone_associated_rainfall_tag.find(
        'div',
        attrs={
            'class': 'panel'
        }
    )

    # We need to check if div_tag_with_panel_class is missing
    if div_tag_with_panel_class is None:
        return tropical_cyclone_associated_rainfall

    tropical_cyclone_associated_rainfall_tag = div_tag_with_panel_class.find(
        'div',
        attrs={
            'class': 'col-md-8'
        }
    )
    img_tag = tropical_cyclone_associated_rainfall_tag.find('img')
    tropical_cyclone_associated_rainfall = img_tag['src']
    tropical_cyclone_associated_rainfall = str(tropical_cyclone_associated_rainfall).strip()

    return tropical_cyclone_associated_rainfall