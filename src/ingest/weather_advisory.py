'''
    Module to ingest weather advisory from the
    PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Creates the data/raw/weather_advisory/
        subdirectory to store JSON files for weather
        advisory from the PAGASA-DOST website.
    '''
    # Create the data/raw/weather_advisory/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weather_advisory'):
        os.makedirs('data/raw/weather_advisory')