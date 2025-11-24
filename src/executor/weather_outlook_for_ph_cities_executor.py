'''
    Module to execute functions for ingesting, transformation, 
    loading, and etc. of weather outlook for selected Philippine
    cities from the PAGASA-DOST website.
'''
from ingest.weather_outlook_for_ph_cities import create_subdir
from ingest.weather_outlook_for_ph_cities import extract_beautiful_soup_object
from ingest.weather_outlook_for_ph_cities import extract_issued_datetime
from ingest.weather_outlook_for_ph_cities import save_issued_datetime_to_json
from ingest.weather_outlook_for_ph_cities import extract_valid_period
from ingest.weather_outlook_for_ph_cities import save_valid_period_to_json
from ingest.weather_outlook_for_ph_cities import extract_ph_city_tags
from ingest.weather_outlook_for_ph_cities import extract_ph_city_names
from ingest.weather_outlook_for_ph_cities import map_weather_dates_to_ph_cities

def execute_functions_to_ingest_weather_outlook_for_ph_cities() -> None:
    '''
        Function to execute all functions from the
        weather_outlook_for_ph_cities module of src/ingest/ package
        to ingest the data of weather outlook for selected Philippine
        cities from the PAGASA-DOST website.
    '''
    # Execute all the functions to ingest the data of weather outlook for selected Philippine cities from the PAGASA-DOST website
    create_subdir()
    soup = extract_beautiful_soup_object('https://www.pagasa.dost.gov.ph/weather/weather-outlook-selected-philippine-cities')

    issued_datetime = extract_issued_datetime(soup)
    save_issued_datetime_to_json(issued_datetime)

    valid_period = extract_valid_period(soup)
    save_valid_period_to_json(valid_period)

    list_of_all_ph_city_tags = extract_ph_city_tags(soup)

    ph_city_names = extract_ph_city_names(list_of_all_ph_city_tags)
    map_weather_dates_to_ph_cities(list_of_all_ph_city_tags, ph_city_names)