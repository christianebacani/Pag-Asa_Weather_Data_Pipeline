'''
    Module to ingest the data of the weather outlook for
    selected Philippine tourist areas from the PAGASA-DOST website.
'''
import os

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