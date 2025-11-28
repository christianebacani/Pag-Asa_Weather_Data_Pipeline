'''
    Module to execute functions for ingesting, transformation, 
    loading, and etc. of weather outlook for selected Philippine
    tourist areas from the PAGASA-DOST website.
'''
from ingest.weather_outlook_for_ph_tourist_areas import create_subdir
from ingest.weather_outlook_for_ph_tourist_areas import extract_beautiful_soup_object
from ingest.weather_outlook_for_ph_tourist_areas import extract_issued_datetime
from ingest.weather_outlook_for_ph_tourist_areas import save_issued_datetime_to_json
from ingest.weather_outlook_for_ph_tourist_areas import extract_valid_period
from ingest.weather_outlook_for_ph_tourist_areas import save_valid_period_to_json
from ingest.weather_outlook_for_ph_tourist_areas import extract_ph_tourist_area_tags

def ingest_weather_outlook_for_ph_tourist_areas(
) -> None:
    '''
        Function to ingest weather outlook for selected
        Philippine tourist areas from the PAGASA-DOST
        website by executing all functions from
        weather_outlook_for_ph_tourist_areas module of
        src/ingest/ package.
    '''
    # Execute all the functions to ingest the data of weather outlook for selected 
    # Philippine tourist areas from the PAGASA-DOST website
    create_subdir()
    soup = extract_beautiful_soup_object(
        'https://www.pagasa.dost.gov.ph/weather/weather-outlook-selected-tourist-areas'
    )

    issued_datetime = extract_issued_datetime(soup)
    save_issued_datetime_to_json(issued_datetime)

    valid_period = extract_valid_period(soup)
    save_valid_period_to_json(valid_period)

    list_of_all_ph_tourist_area_tags = extract_ph_tourist_area_tags(soup)