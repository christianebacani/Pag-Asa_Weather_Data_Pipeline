'''
    Module to execute functions for ingesting, transformation, 
    loading, and etc. of weather outlook for selected Philippine
    tourist areas from the PAGASA-DOST website.
'''
from ingest.weather_outlook_for_ph_tourist_areas import create_subdir

def execute_functions_to_ingest_weather_outlook_for_ph_tourist_areas() -> None:
    '''
        Function to execute all functions from the
        weather_outlook_for_ph_tourist_areas module of src/ingest/ package
        to ingest the data of weather outlook for selected Philippine
        tourist areas from the PAGASA-DOST website.
    '''
    create_subdir()