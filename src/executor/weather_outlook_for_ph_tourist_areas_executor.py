'''
    Module to execute functions for ingesting, transformation, 
    loading, and etc. of weather outlook for selected Philippine
    tourist areas from the PAGASA-DOST website.
'''
from ingest.weather_outlook_for_ph_tourist_areas import create_subdir

def ingest_weather_outlook_for_ph_tourist_areas() -> None:
    '''
        Function to ingest weather outlook for selected Philippine tourist
        areas from the PAGASA-DOST website by executing all functions from
        weather_outlook_for_ph_tourist_areas module of src/ingest/ package.
    '''
    create_subdir()