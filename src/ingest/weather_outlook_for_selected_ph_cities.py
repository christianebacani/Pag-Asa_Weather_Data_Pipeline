'''
    Module to ingest the data of the weather outlook for the
    selected philippine cities from the website of pag-asa dost.
'''
import os
from bs4 import BeautifulSoup

def create_weather_outlook_for_ph_cities_subdir() -> None:
    '''
        Function to create data/raw/weather_outlook_for_selected_ph_cities/
        subdirectory to store dedicated json files
        for the ingested data of weather outlook for selected philippine cities
        from the website of pag-asa dost website.
    '''
    # Create the data/raw/weather_outlook_for_selected_ph_cities/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weather_outlook_for_selected_ph_cities'):
        os.makedirs('data/raw/weather_outlook_for_selected_ph_cities')

def extract_weather_outlook_for_ph_cities_soup(url: str) -> BeautifulSoup:
    '''
        Function to extract beautiful soup object of weather outlook for
        the selected philippine cities from the website of pag-asa dost.
    '''