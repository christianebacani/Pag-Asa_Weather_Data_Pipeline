'''
    Module for executing ingestion, transformation,
    and loading functions for the weather advisory
    from the PAGASA-DOST website.
'''
from ingest.weather_advisory import create_subdir
from ingest.weather_advisory import extract_beautiful_soup_object

def ingest_weather_advisory(
) -> None:
    '''
        Ingests the weather advisory
        from the PAGASA-DOST website
        by executing all functions in
        the weather_advisory module
        of the src/ingest package.
    '''
    # Run all functions to ingest weather advisory data
    create_subdir()
    soup = extract_beautiful_soup_object(
        'https://www.pagasa.dost.gov.ph/weather/weather-advisory'
    )