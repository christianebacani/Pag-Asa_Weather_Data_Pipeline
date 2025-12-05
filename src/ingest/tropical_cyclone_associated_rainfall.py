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