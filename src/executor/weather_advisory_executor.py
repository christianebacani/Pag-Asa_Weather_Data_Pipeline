'''
    Module for executing ingestion, transformation,
    and loading functions for the weather advisory
    from the PAGASA-DOST website.
'''
from ingest.ingest_weather_advisory import create_subdir
from ingest.ingest_weather_advisory import extract_beautiful_soup_object
from ingest.ingest_weather_advisory import extract_weather_advisory
from ingest.ingest_weather_advisory import save_weather_advisory_to_json

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

    weather_advisory = extract_weather_advisory(soup)
    save_weather_advisory_to_json(weather_advisory)