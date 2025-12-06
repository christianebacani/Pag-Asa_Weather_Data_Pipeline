'''
    Module for executing ingestion, transformation,
    and loading functions for the regional forecast
    specifically for the Province of Tarlac and Bataan
    from the PAGASA-DOST website.
'''
from ingest.regional_forecast import create_subdir
from ingest.regional_forecast import extract_beautiful_soup_object
from ingest.regional_forecast import extract_tarlac_weather_forecast_tag
from ingest.regional_forecast import extract_issued_datetime_of_tarlac_weather_forecast

def ingest_regional_forecast(
) -> None:
    '''
        Ingest the regional forecast
        specifically for the Province
        of Tarlac and Bataan from the
        PAGASA-DOST website by executing
        all functions in the regional_forecast
        module of the src/ingest package.
    '''
    # Run all functions to ingest weather advisory data
    create_subdir()
    soup = extract_beautiful_soup_object(
        'https://www.pagasa.dost.gov.ph/regional-forecast/ncrprsd'
    )

    tarlac_weather_forecast_tag = extract_tarlac_weather_forecast_tag(
        soup
    )
    issued_datetime_of_tarlac_weather_forecast = extract_issued_datetime_of_tarlac_weather_forecast(
        tarlac_weather_forecast_tag
    )