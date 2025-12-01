'''
    Module for executing ingestion, transformation,
    and loading functions for the weekly weather
    outlook from the PAGASA-DOST website.
'''
from ingest.weekly_weather_outlook import create_subdir
from ingest.weekly_weather_outlook import extract_beautiful_soup_object
from ingest.weekly_weather_outlook import extract_issued_datetime

def ingest_weekly_weather_outlook(
) -> None:
    '''
        Ingests the weekly weather outlook
        from the PAGASA-DOST website by
        executing all functions in the
        weekly_weather_outlook module of
        the src/ingest package..
    '''
    # Run all functions to ingest weekly weather outlook
    create_subdir()
    soup = extract_beautiful_soup_object(
        'https://www.pagasa.dost.gov.ph/weather/weather-outlook-weekly'
    )

    issued_datetime = extract_issued_datetime(soup)