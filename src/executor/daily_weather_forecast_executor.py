'''
    Module for executing ingestion, transformation,
    and loading functions for the daily weather forecast
    from the PAGASA-DOST website.
'''
from ingest.daily_weather_forecast import create_subdir
from ingest.daily_weather_forecast import extract_beautiful_soup_object
from ingest.daily_weather_forecast import extract_issued_datetime
from ingest.daily_weather_forecast import save_issued_datetime_to_json
from ingest.daily_weather_forecast import extract_synopsis
from ingest.daily_weather_forecast import save_synopsis_to_json
from ingest.daily_weather_forecast import extract_tc_information
from ingest.daily_weather_forecast import save_tc_information_to_json
from ingest.daily_weather_forecast import extract_forecast_weather_conditions
from ingest.daily_weather_forecast import save_forecast_weather_conditions_to_json
from ingest.daily_weather_forecast import extract_forecast_wind_and_coastal_water_conditions
from ingest.daily_weather_forecast import save_forecast_wind_and_coastal_water_conditions_to_json
from ingest.daily_weather_forecast import extract_temperature_and_relative_humidity
from ingest.daily_weather_forecast import save_temperature_and_relative_humidity_to_json

def ingest_daily_weather_forecast(
) -> None:
    '''
        Ingests the daily weather forecast from the
        PAGASA-DOST website by executing all functions 
        in the daily_weather_forecast module of
        the src/ingest package.
    '''
    # Run all functions to ingest daily weather forecast
    create_subdir()
    soup = extract_beautiful_soup_object(
        'https://www.pagasa.dost.gov.ph/weather#daily-weather-forecast'
    )

    issued_datetime = extract_issued_datetime(soup)
    save_issued_datetime_to_json(issued_datetime)

    synopsis = extract_synopsis(soup)
    save_synopsis_to_json(synopsis)

    tc_information = extract_tc_information(soup)
    save_tc_information_to_json(tc_information)

    forecast_weather_conditions = extract_forecast_weather_conditions(soup)
    save_forecast_weather_conditions_to_json(forecast_weather_conditions)

    forecast_wind_and_coastal_water_conditions = extract_forecast_wind_and_coastal_water_conditions(soup)
    save_forecast_wind_and_coastal_water_conditions_to_json(forecast_wind_and_coastal_water_conditions)
    
    temperature_and_relative_humidity = extract_temperature_and_relative_humidity(soup)
    save_temperature_and_relative_humidity_to_json(temperature_and_relative_humidity)