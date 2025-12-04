'''
    Module for executing ingestion, transformation,
    and loading functions for the daily temperature
    including top 10 lowest and top 10 highest
    temperatures recorded across different weather
    stations from the PAGASA-DOST website.
'''
from ingest.daily_temperature import create_subdir
from ingest.daily_temperature import extract_beautiful_soup_object
from ingest.daily_temperature import extract_top_10_lowest_temps_table_tag
from ingest.daily_temperature import extract_recorded_date_from_top_10_lowest_temps
from ingest.daily_temperature import save_recorded_date_from_lowest_temps_to_json
from ingest.daily_temperature import extract_station_names_from_top_10_lowest_temps
from ingest.daily_temperature import extract_temperatures_from_top_10_lowest_temps
from ingest.daily_temperature import map_station_names_to_lowest_temps
from ingest.daily_temperature import save_top_10_lowest_temps_to_json
from ingest.daily_temperature import extract_top_10_highest_temps_table_tag
from ingest.daily_temperature import extract_recorded_date_from_top_10_highest_temps

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

    top_10_lowest_temps_table_tag = extract_top_10_lowest_temps_table_tag(soup)

    recorded_date_from_top_10_lowest_temps = extract_recorded_date_from_top_10_lowest_temps(
        top_10_lowest_temps_table_tag
    )
    save_recorded_date_from_lowest_temps_to_json(
        recorded_date_from_top_10_lowest_temps
    )

    station_names_from_top_10_lowest_temps = extract_station_names_from_top_10_lowest_temps(
        top_10_lowest_temps_table_tag
    )
    temperatures_from_top_10_lowest_temps = extract_temperatures_from_top_10_lowest_temps(
        top_10_lowest_temps_table_tag
    )
    top_10_lowest_temperatures = map_station_names_to_lowest_temps(
        station_names_from_top_10_lowest_temps,
        temperatures_from_top_10_lowest_temps   
    )
    save_top_10_lowest_temps_to_json(
        top_10_lowest_temperatures
    )

    top_10_highest_temps_table_tag = extract_top_10_highest_temps_table_tag(
        soup
    )

    recorded_date_from_top_10_highest_temps = extract_recorded_date_from_top_10_highest_temps(
        top_10_highest_temps_table_tag
    )