'''
    Module for executing ingestion, transformation,
    and loading functions for the daily temperature
    including top 10 lowest and top 10 highest
    temperatures recorded across different weather
    stations from the PAGASA-DOST website.
'''
from ingest.daily_temperature import create_subdir
from ingest.daily_temperature import extract_beautiful_soup_object
from ingest.daily_temperature import extract_top_10_lowest_temp_table_tag
from ingest.daily_temperature import extract_recorded_date_for_top_10_lowest_temp
from ingest.daily_temperature import extract_station_names_for_top_10_lowest_temp

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

    top_10_lowest_temp_table_tag = extract_top_10_lowest_temp_table_tag(soup)

    recorded_date_for_top_10_lowest_temp = extract_recorded_date_for_top_10_lowest_temp(
        top_10_lowest_temp_table_tag
    )
    top_10_lowest_temp_station_names = extract_station_names_for_top_10_lowest_temp(
        top_10_lowest_temp_table_tag
    )