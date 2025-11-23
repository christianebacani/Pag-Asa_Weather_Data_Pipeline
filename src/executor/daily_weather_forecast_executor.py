'''
    Module to execute functions for ingesting, transformation, 
    loading, and etc. of daily weather forecast from the website of
    pag-asa dost.
'''
from ingest.daily_weather_forecast import create_daily_weather_forecast_subdir
from ingest.daily_weather_forecast import extract_daily_weather_forecast_soup
from ingest.daily_weather_forecast import extract_daily_weather_forecast_issued_datetime
from ingest.daily_weather_forecast import save_daily_forecast_issued_datetime_to_json
from ingest.daily_weather_forecast import extract_synopsis
from ingest.daily_weather_forecast import save_synopsis_to_json
from ingest.daily_weather_forecast import extract_forecast_weather_conditions
from ingest.daily_weather_forecast import save_forecast_weather_conditions_to_json
from ingest.daily_weather_forecast import extract_forecast_wind_and_coastal_water_conditions
from ingest.daily_weather_forecast import save_forecast_wind_and_coastal_water_conditions_to_json
from ingest.daily_weather_forecast import extract_temperature_and_relative_humidity
from ingest.daily_weather_forecast import save_temperature_and_relative_humidity_to_json

def execute_functions_to_ingest_daily_weather_forecast() -> None:
    '''
        Function to execute all functions from the
        daily_weather_forecast module of src/ingest/ package
        to ingest the data of daily weather forecast from the
        website of pag-asa dost.
    '''
    # Execute all the functions to ingest the data of daily weather forecast from the website of pag-asa dost
    create_daily_weather_forecast_subdir()
    daily_weather_forecast_soup = extract_daily_weather_forecast_soup('https://www.pagasa.dost.gov.ph/weather#daily-weather-forecast')

    daily_weather_forecast_issued_datetime = extract_daily_weather_forecast_issued_datetime(daily_weather_forecast_soup)
    save_daily_forecast_issued_datetime_to_json(daily_weather_forecast_issued_datetime)

    synopsis = extract_synopsis(daily_weather_forecast_soup)
    save_synopsis_to_json(synopsis)

    forecast_weather_conditions = extract_forecast_weather_conditions(daily_weather_forecast_soup)
    save_forecast_weather_conditions_to_json(forecast_weather_conditions)

    forecast_wind_and_coastal_water_conditions = extract_forecast_wind_and_coastal_water_conditions(daily_weather_forecast_soup)
    save_forecast_wind_and_coastal_water_conditions_to_json(forecast_wind_and_coastal_water_conditions)

    temperature_and_relative_humidity = extract_temperature_and_relative_humidity(daily_weather_forecast_soup)
    save_temperature_and_relative_humidity_to_json(temperature_and_relative_humidity)