'''
    Module to ingest the data of daily weather forecast
    from the PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Function to create data/raw/daily_weather_forecast/
        subdirectory to store dedicated json files
        for the ingested data of daily weather forecast
        from the PAGASA-DOST website.
    '''
    # Create the data/raw/daily_weather_forecast/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/daily_weather_forecast'):
        os.makedirs('data/raw/daily_weather_forecast')

def extract_beautiful_soup_object(
        url: str
) -> BeautifulSoup | None:
    '''
    Function to extract the BeautifulSoup
    object of daily weather forecast from
    the PAGASA-DOST website.

    :param url: Url of the PAGASA-DOST website
    that consist of daily weather forecast
    :type url: str

    :return: BeautifulSoup object to navigate and
    manipulate the entire content of the web-page
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
    Function to extract the issued datetime of daily
    weather forecast from the PAGASA-DOST website.

    :param soup: BeautifulSoup object to navigate and
    manipulate the entire content of the web-page
    :type soup: BeautifulSoup

    :return: Issued datetime of daily weather forecast
    :rtype: str
    '''
    issued_datetime = ''

    # Extract the necessary HTML tags to get the issued datetime of daily weather forecast
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
    Function to save the issued datetime of daily weather 
    forecast to a dedicated json file of the
    data/raw/daily_weather_forecast/ subdirectory from your 
    local machine.

    :param issued_datetime: Issued datetime of daily weather forecast
    :type issued_datetime: str
    '''
    # Create a dictionary that stores the issued datetime of daily weather forecast
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
    Function to extract the synopsis of daily
    weather forecast from the PAGASA-DOST website.

    :param soup: BeautifulSoup object to navigate and
    manipulate the entire content of the web-page
    :type soup: BeautifulSoup

    :return: Synopsis of daily weather forecast
    :rtype: str
    '''
    synopsis = ''

    # Extract the necessary HTML tags to get the synopsis of daily weather forecast
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
    Function to save the synopsis of daily
    weather forecast to a dedicated json file
    of the data/raw/daily_weather_forecast/
    subdirectory from your local machine.

    :param synopsis: Synopsis of daily weather forecast
    :type synopsis: str
    '''
    # Create a dictionary that stores the synopsis of daily weather forecast
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
    Function to extract the tropical cyclone information
    of daily weather forecast from the PAGASA-DOST website.

    :param soup: BeautifulSoup object to navigate and
    manipulate the entire content of the web-page
    :type soup: BeautifulSoup

    :return: Tropical Cyclone information dictionary
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

    # Extract the necessary HTML tags to get the forecast weather conditions of daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_daily_weather_forecast_tags = div_tag_with_row_weather_page_class.find_all(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )

    # Verify that the TC info section exists by checking if there are exactly 5 divs 
    # with the 'col-md-12 col-lg-12' class
    if len(list_of_all_daily_weather_forecast_tags) == 5:
        tc_information_tag = list_of_all_daily_weather_forecast_tags[1]
    
    else:
        return tc_information

    tbody_tag = tc_information_tag.find('tbody')
    list_of_all_table_data_row_tags = tbody_tag.find_all('tr')

    # Using for-loop to access rows that contains the data of tropical cyclone information
    for row_number, table_row_tag in enumerate(list_of_all_table_data_row_tags):
        cell = str(table_row_tag.text)

        list_of_text_to_remove = [
            'LOCATION:',
            'GUSTINESS:',
            'MAXIMUM SUSTAINED WINDS:',
            'GUSTINESS:',
            'MOVEMENT:'
        ]

        # Loop through each string in the given list and remove it from the tropical cyclone
        # information text data
        for text_to_remove in list_of_text_to_remove:
            cell = cell.replace(text_to_remove, '').strip()

        # Use the current row index to access the correct key in the tc_information dictionary
        tc_information_keys = list(tc_information.keys())
        key = tc_information_keys[row_number]
        value = cell
        tc_information[key] = value

    return tc_information

def extract_forecast_weather_conditions(
        soup: BeautifulSoup
) -> dict[str, list]:
    '''
    Function to extract the forecast weather conditions
    of daily weather forecast from the PAGASA-DOST website.

    :param soup: BeautifulSoup object to navigate and
    manipulate the entire content of the web-page
    :type soup: BeautifulSoup

    :return: Forecast weather conditions dictionary
    :rtype: dict[str, list]
    '''
    forecast_weather_conditions = {
        'place': [],
        'weather_condition': [],
        'caused_by': [],
        'impacts': []
    }

    # Extract the necessary HTML tags to get the forecast weather conditions of daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_daily_weather_forecast_tags = div_tag_with_row_weather_page_class.find_all(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )

    # Verify that the TC info section exists by checking if there are exactly 5 divs 
    # with the 'col-md-12 col-lg-12' class
    if len(list_of_all_daily_weather_forecast_tags) == 5:
        forecast_weather_conditions_tag = list_of_all_daily_weather_forecast_tags[2]
    
    else:
        forecast_weather_conditions_tag = list_of_all_daily_weather_forecast_tags[1]

    tbody_tag = forecast_weather_conditions_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return forecast_weather_conditions

    list_of_all_table_row_tags = tbody_tag.find_all('tr')
    
    # Using for-loop to access rows that contains the necessary HTML tags to get forecast weather conditions
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

def save_forecast_weather_conditions_to_json(
    forecast_weather_conditions: dict[str, list]
) -> None:
    '''
    Function to save the forecast weather conditions
    of daily weather forecast to a dedicated
    json file of the data/raw/daily_weather_forecast/
    subdirectory from your local machine.

    :param forecast_weather_conditions: Forecast weather conditions dictionary
    :type forecast_weather_conditions: dict[str, list]
    '''
    # Create a dictionary that stores the forecast weather conditions of daily weather forecast
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
    Function to extract the forecast wind and coastal water
    conditions of daily weather forecast from the PAGASA-DOST
    website.

    :param soup: BeautifulSoup object to navigate and manipulate
    the entire content of the web-page
    :type soup: BeautifulSoup

    :return: Forecast wind and coastal water conditions dictionary
    :rtype: dict[str, list]
    '''
    forecast_wind_and_coastal_water_conditions = {
        'place': [],
        'speed': [],
        'direction': [],
        'coastal_water': []
    }

    # Extract the necessary HTML tags to get the forecast wind and coastal water conditions 
    # of daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_daily_weather_forecast_tags = div_tag_with_row_weather_page_class.find_all(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )

    # Verify that the TC info section exists by checking if there are exactly 5 divs 
    # with the 'col-md-12 col-lg-12' class
    if len(list_of_all_daily_weather_forecast_tags) == 5:
        forecast_wind_and_coastal_water_conditions_tag = list_of_all_daily_weather_forecast_tags[3]
    
    else:
        forecast_wind_and_coastal_water_conditions_tag = list_of_all_daily_weather_forecast_tags[2]

    tbody_tag = forecast_wind_and_coastal_water_conditions_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return forecast_wind_and_coastal_water_conditions

    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    # Using for-loop to access rows that contains the necessary HTML tags to 
    # get forecast wind and coastal water conditions
    for table_row_tag in list_of_all_table_row_tags:
        # Using find_all() method to retrieve all the necessary data of
        # forecast wind and coastal water conditions
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
    Function to save the forecast wind and coastal water conditions
    of daily weather forecast to a dedicated json file of the
    data/raw/daily_weather_forecast/ subdirectory from your local machine.

    :param forecast_wind_and_coastal_water_conditions: Forecast wind and
    coastal water conditions dictionary
    :type forecast_wind_and_coastal_water_conditions: dict[str, list]
    '''
    # Create a dictionary that stores the forecast wind and coastal water conditions of
    # daily weather forecast
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
    Function to extract temperature and relative humidity
    of daily weather forecast from the PAGASA-DOST website.

    :param soup: BeautifulSoup object to navigate and manipulate
    the entire content of the web-page
    :type soup: BeautifulSoup

    :return: Temperature and relative humidity dictionary
    :rtype: dict[str, str]
    '''
    temperature_and_relative_humidity = {
        'temperature': {'max': [], 'min': []},
        'relative_humidity_percentage': {'max': [], 'min': []}
    }
    
    # Extract the necessary HTML tags to get the temperature and relative humidity of daily weather forecast
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_daily_weather_forecast_tags = div_tag_with_row_weather_page_class.find_all(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )

    # Verify that the TC info section exists by checking if there are exactly 5 divs 
    # with the 'col-md-12 col-lg-12' class
    if len(list_of_all_daily_weather_forecast_tags) == 5:
        temperature_and_relative_humidity_tag = list_of_all_daily_weather_forecast_tags[4]
    
    else:
        temperature_and_relative_humidity_tag = list_of_all_daily_weather_forecast_tags[3]

    tbody_tag = temperature_and_relative_humidity_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return temperature_and_relative_humidity

    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    # Using for-loop to access rows that contains the necessary HTML tags to get
    # temperature and relative humidity of daily weather forecast
    for row_number, table_row_tag in enumerate(list_of_all_table_row_tags):
        row_number += 1
        list_of_all_table_data_tags = table_row_tag.find_all('td')[1:]

        first_instance_of_table_data_tag = str(list_of_all_table_data_tags[0].text).strip()
        second_instance_of_table_data_tag = str(list_of_all_table_data_tags[1].text).strip()
        third_instance_of_table_data_tag = str(list_of_all_table_data_tags[2].text).strip()
        fourth_instance_of_table_data_tag = str(list_of_all_table_data_tags[3].text).strip()
        
        # Check if the row_number is equal to 1 (temperature data) or
        # 2 (relative humidity percentage data) instead of manually fetching it
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
    Function to save the temperature and relative humidity of
    daily weather forecast to a dedicated json file of the
    data/raw/daily_weather_forecast/ subdirectory from your
    local machine.

    :param temperature_and_relative_humidity: Temperature and
    relative humidity dictionary
    :type temperature_and_relative_humidity: dict[str, dict]
    '''
    # Create a dictionary that stores the temperature and relative humidity of daily weather forecast
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