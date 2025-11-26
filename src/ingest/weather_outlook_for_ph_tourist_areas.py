'''
    Module to ingest the data of the weather outlook for
    selected Philippine tourist areas from the PAGASA-DOST website.
'''
import os
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

def extract_beautiful_soup_object(url: str) -> BeautifulSoup:
    '''
    Function to extract the BeautifulSoup object of weather
    outlook for selected Philippine cities from the PAGASA-DOST 
    website.

    :param url: Url of the PAGASA-DOST website that consist of weather outlook for selected Philippine tourist areas
    :type url: str
    :return:
    :rtype: BeautifulSoup
    '''