'''
    Module to ingest weekly weather outlook
    from the PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Creates the data/raw/weekly_weather_outlook/
        subdirectory to store JSON files for weekly
        weather outlook data ingested from the PAGASA-
        DOST website.
    '''
    # Create the data/raw/weekly_weather_outlook/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weekly_weather_outlook'):
        os.makedirs('data/raw/weekly_weather_outlook')