'''
    Module for executing ingestion, transformation,
    and loading functions for the daily temperature
    including top 10 lowest and top 10 highest
    temperatures recorded across different weather
    stations from the PAGASA-DOST website.
'''
from ingest.daily_temperature import create_subdir
from ingest.daily_temperature import extract_beautiful_soup_object
from ingest.daily_temperature import extract_lowest_temperature_table_tag

def ingest_daily_temperature(
) -> None:
    '''
        Ingests the daily temperature
        from the PAGASA-DOST website by
        executing all functions in the
        daily_temperature module of
        src/ingest package.
    '''
    # Run all functions to ingest daily temperature
    create_subdir()
    soup = extract_beautiful_soup_object(
        'https://www.pagasa.dost.gov.ph/weather/low-high-temperature'
    )

    lowest_temperature_table_tag = extract_lowest_temperature_table_tag(soup)