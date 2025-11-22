'''
    Daily Weather Forecast Module
'''
import requests
import os
import json
from bs4 import BeautifulSoup

def create_daily_weather_forecast_subdir() -> None:
    '''
        Function to create data/raw/daily_weather_forecast/
        subdirectory to store dedicated json files
        for the ingested datas of daily weather forecast
        from the website of pag-asa dost website.
    '''
    # Create the data/raw/daily_weather_forecast/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/daily_weather_forecast'):
        os.makedirs('data/raw/daily_weather_forecast')

def extract_daily_weather_forecast_soup(url: str) -> BeautifulSoup | None:
    '''
        Function to extract beautiful soup object of daily weather
        forecast from the website of pag-asa dost.
    '''
    response = requests.get(url)

    # We need to check if the status code of the response for the request is unsuccessful
    if response.status_code != 200: 
        return None

    # Parse as a Beautiful Soup Object
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_daily_weather_forecast_issued_datetime(soup: BeautifulSoup) -> str:
    '''
        Function to extract the issued datetime of daily weather forecast
        from pag-asa dost website.
    '''
    issued_datetime = ''

    # Extract the necessary html tags to get the issued datetime of daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_tag = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    bold_tag = issued_datetime_tag.find('b')

    # We need to check if the bold_tag is not missing
    if bold_tag is not None:
        issued_datetime = str(bold_tag.text).strip()

    return issued_datetime

def save_daily_forecast_issued_datetime_to_json(daily_weather_forecast_issued_datetime: str) -> None:
    '''
        Function to save issued datetime of daily weather forecast to a dedicated json file
        of the data/raw/daily_weather_forecast subdirectory from your local machine.
    '''
    # Create a dictionary that stores daily weather forecast issued datetime
    data = {
        "issued_datetime": daily_weather_forecast_issued_datetime
    }

    # Save the dictionary to the json file using open() method and json module
    with open('data/raw/daily_weather_forecast/issued_datetime.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    json_file.close()

def extract_synopsis(soup: BeautifulSoup) -> str:
    '''
        Function to extract the synopsis of the
        daily weather forecast from the website
        of pag-asa dost.
    '''
    synopsis = ''

    # Extract the necessary html tags to get the synopsis of daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    synopsis_tag = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 col-lg-12'})
    div_tag_with_panel_body_class = synopsis_tag.find('div', attrs={'class': 'panel-body'})

    # We need to check if the div_tag_with_panel_body_class is not missing
    if div_tag_with_panel_body_class is not None: 
        synopsis = str(div_tag_with_panel_body_class.text).strip()

    return synopsis

def save_synopsis_to_json(synopsis: str) -> None:
    '''
        Function to save the synopsis of the daily
        weather forecast to a dedicated json file
        of the data/raw/daily_weather_forecast 
        subdirectory from your local machine.
    '''
    # Create a dictionary that stores the synopsis of the daily weather forecast
    data = {
        "synopsis": synopsis
    }

    # Save the dictionary to the json file using open() method and json module
    with open('data/raw/daily_weather_forecast/synopsis.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_forecast_weather_conditions(soup: BeautifulSoup) -> str:
    '''
        Function to extract the weather forecast conditions
        of the daily weather forecast from the website of pag-asa
        dost website.
    '''
    forecast_weather_conditions = {
        'place': [],
        'weather_condition': [],
        'caused_by': [],
        'impacts': []
    }

    # Extract the necessary html tags to get the forecast weather conditions of daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    forecast_weather_conditions_tag = div_tag_with_row_weather_page_class.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[1]
    tbody_tag = forecast_weather_conditions_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return forecast_weather_conditions

    list_of_all_table_row_tags = tbody_tag.find_all('tr')
    
    # Using for-loop to access rows that contain the necessary html tags for forecast weather conditions
    for table_row_tag in list_of_all_table_row_tags:
        # Using find_all() method to retrieve all the necessary data of forecast weather conditions
        list_of_all_table_data_tags = table_row_tag.find_all('td')

        place = str(list_of_all_table_data_tags[0].text).strip()
        forecast_weather_conditions['place'].append(place)

        weather_condition = str(list_of_all_table_data_tags[1].text).strip()
        forecast_weather_conditions['weather_condition'].append(weather_condition)

        caused_by = str(list_of_all_table_data_tags[2].text).strip()
        forecast_weather_conditions['caused_by'].append(caused_by)

        impacts = str(list_of_all_table_data_tags[3].text).strip()
        forecast_weather_conditions['impacts'].append(impacts)
    
    return forecast_weather_conditions

def save_forecast_weather_conditions_to_json(forecast_weather_conditions: dict[str, list]) -> None:
    '''
        Function to save the forecast weather conditions of daily weather forecast to a dedicated
        json file of the data/raw/daily_weather_forecast subdirectory from your local machine.
    '''