'''
    Module to execute functions for ingesting, transformation, 
    loading, and etc. of weather outlook for selected philippine
    cities from the website of pag-asa dost.
'''
from ingest.weather_outlook_for_ph_cities import create_weather_outlook_for_ph_cities_subdir
from ingest.weather_outlook_for_ph_cities import extract_weather_outlook_for_ph_cities_soup

def execute_functions_to_ingest_weather_outlook_for_ph_cities() -> None:
    '''
        Function to execute all functions from the
        weather_outlook_for_ph_cities module of src/ingest/ package
        to ingest the data of weather outlook for selected philippine
        cities from the website of pag-asa dost.
    '''
    create_weather_outlook_for_ph_cities_subdir()
    weather_outlook_for_ph_cities_soup = extract_weather_outlook_for_ph_cities_soup('https://www.pagasa.dost.gov.ph/weather/weather-outlook-selected-philippine-cities')
    print(weather_outlook_for_ph_cities_soup)