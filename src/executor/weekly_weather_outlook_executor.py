'''
    Module for executing ingestion, transformation,
    and loading functions for the weekly weather
    outlook from the PAGASA-DOST website.
'''
from ingest.weekly_weather_outlook import create_subdir
from ingest.weekly_weather_outlook import extract_beautiful_soup_object
from ingest.weekly_weather_outlook import extract_issued_datetime
from ingest.weekly_weather_outlook import save_issued_datetime_to_json
from ingest.weekly_weather_outlook import extract_valid_period
from ingest.weekly_weather_outlook import save_valid_period_to_json
from ingest.weekly_weather_outlook import extract_date_ranges
from ingest.weekly_weather_outlook import extract_weather_outlooks
from ingest.weekly_weather_outlook import map_date_ranges_to_weather_outlooks
from ingest.weekly_weather_outlook import save_weekly_weather_outlook_to_json

def ingest_weekly_weather_outlook(
) -> None:
    '''
        Ingests the weekly weather outlook
        from the PAGASA-DOST website by
        executing all functions in the
        weekly_weather_outlook module of
        the src/ingest package.
    '''
    # Run all functions to ingest weekly weather outlook
    create_subdir()
    soup = extract_beautiful_soup_object(
        'https://www.pagasa.dost.gov.ph/weather/weather-outlook-weekly'
    )

    issued_datetime = extract_issued_datetime(soup)
    save_issued_datetime_to_json(issued_datetime)

    valid_period = extract_valid_period(soup)
    save_valid_period_to_json(valid_period)

    date_ranges = extract_date_ranges(soup)
    weather_outlooks = extract_weather_outlooks(soup)
    weekly_weather_outlook = map_date_ranges_to_weather_outlooks(
        date_ranges,
        weather_outlooks
    )

    save_weekly_weather_outlook_to_json(weekly_weather_outlook)