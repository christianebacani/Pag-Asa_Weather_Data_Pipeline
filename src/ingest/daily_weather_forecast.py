'''
    Module to ingest daily weather forecast data
    from the PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Creates the data/raw/daily_weather_forecast/
        subdirectory to store JSON files for daily
        weather forecast data ingested from the
        PAGASA-DOST website.
    '''
    # Create the data/raw/daily_weather_forecast/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/daily_weather_forecast'):
        os.makedirs('data/raw/daily_weather_forecast')

def extract_beautiful_soup_object(
        url: str
) -> BeautifulSoup | None:
    '''
    Extracts the BeautifulSoup object of the
    daily weather forecast page from the
    PAGASA-DOST website.

    :param url: URL of the PAGASA-DOST page
        containing the daily weather forecast
    :type url: str

    :return: BeautifulSoup object for navigating
        and manipulating the page content, or
        None if extraction fails
    :rtype: BeautifulSoup | None
    '''
    response = requests.get(url)

    # We need to check if the status code of the response for the request is unsuccessful
    if response.status_code != 200: 
        return None

    # Parse as a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_issued_datetime(
    soup: BeautifulSoup
) -> str:
    '''
    Extracts the issued datetime of the daily
    weather forecast from the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating
        and manipulating the page content
    :type soup: BeautifulSoup

    :return: Issued datetime of the daily weather forecast
    :rtype: str
    '''
    issued_datetime = ''

    # Extract HTML tags for issued datetime of the daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12 issue'
        }
    )
    bold_tag = issued_datetime_tag.find('b')

    # We need to check if the bold_tag is not missing
    if bold_tag is not None:
        issued_datetime = str(bold_tag.text).strip()

    return issued_datetime

def save_issued_datetime_to_json(
        issued_datetime: str
) -> None:
    '''
    Saves the issued datetime of the daily
    weather forecast to a JSON file in the
    data/raw/daily_weather_forecast/
    subdirectory on the local machine.

    :param issued_datetime: Issued datetime
        of the daily weather forecast
    :type issued_datetime: str
    '''
    # Create a dictionary to store issued datetime of the daily weather forecast
    data = {
        "issued_datetime": issued_datetime
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/daily_weather_forecast/issued_datetime.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)
    
    json_file.close()

def extract_synopsis(
        soup: BeautifulSoup
) -> str:
    '''
    Extracts the synopsis of the daily weather
    forecast from the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating
        and manipulating the page content
    :type soup: BeautifulSoup

    :return: Synopsis of the daily weather forecast
    :rtype: str
    '''
    synopsis = ''

    # Extract HTML tags for synopsis of the daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    synopsis_tag = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 col-lg-12'})
    div_tag_with_panel_body_class = synopsis_tag.find('div', attrs={'class': 'panel-body'})

    # We need to check if the div_tag_with_panel_body_class is not missing
    if div_tag_with_panel_body_class is not None: 
        synopsis = str(div_tag_with_panel_body_class.text).strip()

    return synopsis

def save_synopsis_to_json(
        synopsis: str
) -> None:
    '''
    Saves the synopsis of the daily weather forecast to a
    JSON file in the data/raw/daily_weather_forecast/
    subdirectory on the local machine.

    :param synopsis: Synopsis of the daily weather forecast
    :type synopsis: str
    '''
    # Create a dictionary to store synopsis of the daily weather forecast
    data = {
        "synopsis": synopsis
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/daily_weather_forecast/synopsis.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_tc_information(
        soup: BeautifulSoup
) -> dict[str, str]:
    '''
    Extracts tropical cyclone information from the daily
    weather forecast on the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating and
        manipulating the page content
    :type soup: BeautifulSoup

    :return: Dictionary containing tropical cyclone
        information
    :rtype: dict[str, str]
    '''
    tc_information = {
        'current_update': '',
        'tropical_cyclone_name': '',
        'location': '',
        'maximum_sustained_winds': '',
        'gustiness': '',
        'movement': ''
    }

    # Extract HTML tags for tropical cyclone information from the daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_daily_weather_forecast_tags = div_tag_with_row_weather_page_class.find_all(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )

    # Verify TC info section exists: exactly 5 divs with class 'col-md-12 col-lg-12'
    if len(list_of_all_daily_weather_forecast_tags) == 5:
        tc_information_tag = list_of_all_daily_weather_forecast_tags[1]
    
    else:
        return tc_information

    tbody_tag = tc_information_tag.find('tbody')
    list_of_all_table_data_row_tags = tbody_tag.find_all('tr')

    # Loop through rows containing data of tropical cyclone information
    for row_number, table_row_tag in enumerate(list_of_all_table_data_row_tags):
        cell = str(table_row_tag.text)

        list_of_text_to_remove = [
            'LOCATION:',
            'GUSTINESS:',
            'MAXIMUM SUSTAINED WINDS:',
            'GUSTINESS:',
            'MOVEMENT:'
        ]

        # Loop through the list and remove each string from the tropical cyclone info text
        for text_to_remove in list_of_text_to_remove:
            cell = cell.replace(text_to_remove, '').strip()

        # Use the current row index to access the correct key in the tc_information dictionary
        tc_information_keys = list(tc_information.keys())
        key = tc_information_keys[row_number]
        value = cell
        tc_information[key] = value

    return tc_information

def save_tc_information_to_json(
        tc_information: dict[str, str]
) -> None:
    '''
    Saves the tropical cyclone information of the daily weather forecast to
    a JSON file in the data/raw/daily_weather_forecast/ subdirectory on the
    local machine.

    :param tc_information: Dictionary containing tropical cyclone information
    :type tc_information: dict[str, str]
    '''
    # Create a dictionary to store tropical cyclone information from the daily weather forecast
    data = {
        "current_update": tc_information['current_update'],
        "tropical_cyclone_name": tc_information['tropical_cyclone_name'],
        "location": tc_information['location'],
        "maximum_sustained_winds": tc_information['maximum_sustained_winds'],
        "gustiness": tc_information['gustiness'],
        "movement": tc_information['movement']
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/daily_weather_forecast/tropical_cyclone_information.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)
    
    json_file.close()

def extract_forecast_weather_conditions(
        soup: BeautifulSoup
) -> dict[str, list]:
    ''' 
    Extracts forecast weather conditions from the daily weather
    forecast on the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating and
        manipulating the page content
    :type soup: BeautifulSoup

    :return: Dictionary containing forecast weather conditions
    :rtype: dict[str, list]
    '''
    forecast_weather_conditions = {
        'place': [],
        'weather_condition': [],
        'caused_by': [],
        'impacts': []
    }

    # Extract HTML tags for forecast weather conditions from the daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_daily_weather_forecast_tags = div_tag_with_row_weather_page_class.find_all(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )

    # Verify TC info section exists: exactly 5 divs with class 'col-md-12 col-lg-12'
    if len(list_of_all_daily_weather_forecast_tags) == 5:
        forecast_weather_conditions_tag = list_of_all_daily_weather_forecast_tags[2]
    
    else:
        forecast_weather_conditions_tag = list_of_all_daily_weather_forecast_tags[1]

    tbody_tag = forecast_weather_conditions_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return forecast_weather_conditions

    list_of_all_table_row_tags = tbody_tag.find_all('tr')
    
    # Loop through rows containing HTML tags for forecast weather conditions
    for table_row_tag in list_of_all_table_row_tags:
        # Use find_all() to retrieve all forecast weather conditions data
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

def save_forecast_weather_conditions_to_json(
    forecast_weather_conditions: dict[str, list]
) -> None:
    '''
    Saves the forecast weather conditions of the daily
    weather forecast to a JSON file in the
    data/raw/daily_weather_forecast/ subdirectory on
    the local machine.

    :param forecast_weather_conditions: Dictionary
        containing forecast weather conditions
    :type forecast_weather_conditions: dict[str, list]
    '''
    # Create a dictionary to store forecast weather conditions from the daily weather forecast
    data = {
        "place": forecast_weather_conditions['place'],
        "weather_condition": forecast_weather_conditions['weather_condition'],
        "caused_by": forecast_weather_conditions['caused_by'],
        "impacts": forecast_weather_conditions['impacts']
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/daily_weather_forecast/forecast_weather_conditions.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_forecast_wind_and_coastal_water_conditions(
        soup: BeautifulSoup
) -> dict[str, list]:
    '''
    Extracts forecast wind and coastal water conditions
    from the daily weather forecast on the PAGASA-DOST
    website.

    :param soup: BeautifulSoup object for navigating and
        manipulating the page content
    :type soup: BeautifulSoup
    
    :return: Dictionary containing forecast wind and
        coastal water conditions
    :rtype: dict[str, list]
    '''
    forecast_wind_and_coastal_water_conditions = {
        'place': [],
        'speed': [],
        'direction': [],
        'coastal_water': []
    }

    # Extract HTML tags for forecast wind and coastal water conditions from the daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_daily_weather_forecast_tags = div_tag_with_row_weather_page_class.find_all(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )

    # Verify TC info section exists: exactly 5 divs with class 'col-md-12 col-lg-12'
    if len(list_of_all_daily_weather_forecast_tags) == 5:
        forecast_wind_and_coastal_water_conditions_tag = list_of_all_daily_weather_forecast_tags[3]
    
    else:
        forecast_wind_and_coastal_water_conditions_tag = list_of_all_daily_weather_forecast_tags[2]

    tbody_tag = forecast_wind_and_coastal_water_conditions_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return forecast_wind_and_coastal_water_conditions

    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    # Loop through rows containing HTML tags for forecast wind and coastal water conditions
    for table_row_tag in list_of_all_table_row_tags:
        # Use find_all() to retrieve all forecast wind and coastal water conditions data
        list_of_all_table_data_tags = table_row_tag.find_all('td')

        place = str(list_of_all_table_data_tags[0].text).strip()
        forecast_wind_and_coastal_water_conditions['place'].append(place)

        speed = str(list_of_all_table_data_tags[1].text).strip()
        forecast_wind_and_coastal_water_conditions['speed'].append(speed)

        direction = str(list_of_all_table_data_tags[2].text).strip()
        forecast_wind_and_coastal_water_conditions['direction'].append(direction)

        coastal_water = str(list_of_all_table_data_tags[3].text).strip()
        forecast_wind_and_coastal_water_conditions['coastal_water'].append(coastal_water)

    return forecast_wind_and_coastal_water_conditions

def save_forecast_wind_and_coastal_water_conditions_to_json(
    forecast_wind_and_coastal_water_conditions: dict[str, list]
) -> None:
    '''
    Saves the forecast wind and coastal water conditions of the
    daily weather forecast to a JSON file in the
    data/raw/daily_weather_forecast/ subdirectory on the local
    machine.

    :param forecast_wind_and_coastal_water_conditions: Dictionary
        containing forecast wind and coastal water conditions
    :type forecast_wind_and_coastal_water_conditions: dict[str, list]
    '''
    # Create a dictionary to store forecast wind and coastal water conditioons from the daily weather forecast
    data = {
        "place": forecast_wind_and_coastal_water_conditions['place'],
        "speed": forecast_wind_and_coastal_water_conditions['speed'],
        "direction": forecast_wind_and_coastal_water_conditions['direction'],
        "coastal_water": forecast_wind_and_coastal_water_conditions['coastal_water']
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/daily_weather_forecast/forecast_wind_and_coastal_water_conditions.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_temperature_and_relative_humidity(
        soup: BeautifulSoup
) -> dict[str, str]:
    '''
    Extracts temperature and relative humidity from
    the daily weather forecast on the PAGASA-DOST
    website.

    :param soup: BeautifulSoup object for navigating
        and manipulating the page content
    :type soup: BeautifulSoup

    :return: Dictionary containing temperature and
        relative humidity
    :rtype: dict[str, str]
    '''
    temperature_and_relative_humidity = {
        'temperature': {'max': [], 'min': []},
        'relative_humidity_percentage': {'max': [], 'min': []}
    }
    
    # Extract HTML tags for temperature and relative humidity from the daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_daily_weather_forecast_tags = div_tag_with_row_weather_page_class.find_all(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )

    # Verify TC info section exists: exactly 5 divs with class 'col-md-12 col-lg-12'
    if len(list_of_all_daily_weather_forecast_tags) == 5:
        temperature_and_relative_humidity_tag = list_of_all_daily_weather_forecast_tags[4]
    
    else:
        temperature_and_relative_humidity_tag = list_of_all_daily_weather_forecast_tags[3]

    tbody_tag = temperature_and_relative_humidity_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return temperature_and_relative_humidity

    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    # Loop through rows containing HTML tags for temperature and relative humidity
    for row_number, table_row_tag in enumerate(list_of_all_table_row_tags):
        row_number += 1
        # Use find_all() to retrieve all temperature and relative humidity data
        list_of_all_table_data_tags = table_row_tag.find_all('td')[1:]

        first_instance_of_table_data_tag = str(list_of_all_table_data_tags[0].text).strip()
        second_instance_of_table_data_tag = str(list_of_all_table_data_tags[1].text).strip()
        third_instance_of_table_data_tag = str(list_of_all_table_data_tags[2].text).strip()
        fourth_instance_of_table_data_tag = str(list_of_all_table_data_tags[3].text).strip()
        
        # Check if row_number is 1 (temperature) or 2 (relative humidity) instead of fetching manually
        if row_number == 1:
            temperature_and_relative_humidity['temperature']['max'].append(
                first_instance_of_table_data_tag
            )
            temperature_and_relative_humidity['temperature']['max'].append(
                second_instance_of_table_data_tag
            )
            temperature_and_relative_humidity['temperature']['min'].append(
                third_instance_of_table_data_tag
            )
            temperature_and_relative_humidity['temperature']['min'].append(
                fourth_instance_of_table_data_tag
            )

        else:
            temperature_and_relative_humidity['relative_humidity_percentage']['max'].append(
                first_instance_of_table_data_tag
            )
            temperature_and_relative_humidity['relative_humidity_percentage']['max'].append(
                second_instance_of_table_data_tag
            )
            temperature_and_relative_humidity['relative_humidity_percentage']['min'].append(
                third_instance_of_table_data_tag
            )
            temperature_and_relative_humidity['relative_humidity_percentage']['min'].append(
                fourth_instance_of_table_data_tag
            )

    return temperature_and_relative_humidity

def save_temperature_and_relative_humidity_to_json(
        temperature_and_relative_humidity: dict[str, dict]
) -> None:
    '''
    Saves the temperature and relative humidity of the daily
    weather forecast to a JSON file in the
    data/raw/daily_weather_forecast/ subdirectory on the local
    machine.

    :param temperature_and_relative_humidity: Dictionary
        containing temperature and relative humidity data
    :type temperature_and_relative_humidity: dict[str, dict]
    '''
    # Create a dictionary to store temperature and relative humidity from the daily weather forecast
    data = {
        "temperature": {
            "max": temperature_and_relative_humidity['temperature']['max'],
            "min": temperature_and_relative_humidity['temperature']['min']
        },
        "relative_humidity_percentage": {
            'max': temperature_and_relative_humidity['relative_humidity_percentage']['max'],
            'min': temperature_and_relative_humidity['relative_humidity_percentage']['min']
        }
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/daily_weather_forecast/temperature_and_relative_humidity.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()