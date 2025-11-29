'''
    Module for executing ingestion, transformation,
    and loading functions for the weather outlook of
    selected Philippine cities from the PAGASA-DOST
    website.
'''
from ingest.weather_outlook_for_ph_cities import create_subdir
from ingest.weather_outlook_for_ph_cities import extract_beautiful_soup_object
from ingest.weather_outlook_for_ph_cities import extract_issued_datetime
from ingest.weather_outlook_for_ph_cities import save_issued_datetime_to_json
from ingest.weather_outlook_for_ph_cities import extract_valid_period
from ingest.weather_outlook_for_ph_cities import save_valid_period_to_json
from ingest.weather_outlook_for_ph_cities import extract_ph_city_tags
from ingest.weather_outlook_for_ph_cities import extract_ph_city_names
from ingest.weather_outlook_for_ph_cities import extract_weather_dates
from ingest.weather_outlook_for_ph_cities import map_weather_dates_to_ph_cities
from ingest.weather_outlook_for_ph_cities import extract_temperature_ranges
from ingest.weather_outlook_for_ph_cities import map_temperature_ranges_to_ph_cities

def ingest_weather_outlook_for_ph_cities(
) -> None:
    '''
        Ingests the weather outlook for selected
        Philippine cities from the PAGASA-DOST
        website by executing all functions in the
        weather_outlook_for_ph_cities module of
        the src/ingest package.
    '''
    # Run all functions to ingest weather outlook data for selected Philippine cities
    create_subdir()
    soup = extract_beautiful_soup_object(
        'https://www.pagasa.dost.gov.ph/weather/weather-outlook-selected-philippine-cities'
    )

    issued_datetime = extract_issued_datetime(soup)
    save_issued_datetime_to_json(issued_datetime)

    valid_period = extract_valid_period(soup)
    save_valid_period_to_json(valid_period)

    list_of_all_ph_city_tags = extract_ph_city_tags(soup)
    ph_city_names = extract_ph_city_names(list_of_all_ph_city_tags)

    weather_dates = extract_weather_dates(soup)
    ph_cities_with_weather_dates = map_weather_dates_to_ph_cities(
        weather_dates,
        ph_city_names
    )

    temperature_ranges = extract_temperature_ranges(list_of_all_ph_city_tags)
    ph_cities_weather_outlook = map_temperature_ranges_to_ph_cities(
        temperature_ranges,
        ph_cities_with_weather_dates
    )