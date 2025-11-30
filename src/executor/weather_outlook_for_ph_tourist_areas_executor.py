'''
    Module for executing ingestion, transformation,
    and loading functions for the weather outlook of
    selected Philippine tourist areas from the PAGASA-DOST
    website.
'''
from ingest.weather_outlook_for_ph_tourist_areas import create_subdir
from ingest.weather_outlook_for_ph_tourist_areas import extract_beautiful_soup_object
from ingest.weather_outlook_for_ph_tourist_areas import extract_issued_datetime
from ingest.weather_outlook_for_ph_tourist_areas import save_issued_datetime_to_json
from ingest.weather_outlook_for_ph_tourist_areas import extract_valid_period
from ingest.weather_outlook_for_ph_tourist_areas import save_valid_period_to_json
from ingest.weather_outlook_for_ph_tourist_areas import extract_ph_tourist_area_tags
from ingest.weather_outlook_for_ph_tourist_areas import extract_ph_tourist_area_names
from ingest.weather_outlook_for_ph_tourist_areas import extract_weather_dates
from ingest.weather_outlook_for_ph_tourist_areas import map_weather_dates_to_ph_tourist_areas
from ingest.weather_outlook_for_ph_tourist_areas import extract_temperature_ranges
from ingest.weather_outlook_for_ph_tourist_areas import map_temperature_ranges_to_ph_tourist_areas
from ingest.weather_outlook_for_ph_tourist_areas import save_ph_tourist_areas_weather_outlook_to_json

def ingest_weather_outlook_for_ph_tourist_areas(
) -> None:
    '''
        Ingests the weather outlook for selected
        Philippine tourist areas from the PAGASA-DOST
        website by executing all functions in the
        weather_outlook_for_ph_tourist_areas module of
        the src/ingest package.
    '''
    # Run all functions to ingest weather outlook data for selected Philippine tourist areas
    create_subdir()
    soup = extract_beautiful_soup_object(
        'https://www.pagasa.dost.gov.ph/weather/weather-outlook-selected-tourist-areas'
    )

    issued_datetime = extract_issued_datetime(soup)
    save_issued_datetime_to_json(issued_datetime)

    valid_period = extract_valid_period(soup)
    save_valid_period_to_json(valid_period)

    list_of_all_ph_tourist_area_tags = extract_ph_tourist_area_tags(soup)
    ph_tourist_area_names = extract_ph_tourist_area_names(list_of_all_ph_tourist_area_tags)

    weather_dates = extract_weather_dates(soup)
    ph_tourist_areas_with_weather_dates = map_weather_dates_to_ph_tourist_areas(
        weather_dates,
        ph_tourist_area_names
    )

    temperature_ranges = extract_temperature_ranges(list_of_all_ph_tourist_area_tags)
    ph_tourist_areas_weather_outlook = map_temperature_ranges_to_ph_tourist_areas(
        temperature_ranges,
        ph_tourist_areas_with_weather_dates
    )

    save_ph_tourist_areas_weather_outlook_to_json(ph_tourist_areas_weather_outlook)