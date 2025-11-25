'''
    Module to ingest the data of the weather outlook for
    selected Philippine cities from the PAGASA-DOST website.
'''
import requests
import os
import json
from bs4 import BeautifulSoup

def create_subdir() -> None:
    '''
        Function to create data/raw/weather_outlook_for_ph_cities/
        subdirectory to store dedicated json files
        for the ingested data of weather outlook for selected
        Philippine cities from the PAGASA-DOST website.
    '''
    # Create the data/raw/weather_outlook_for_ph_cities/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weather_outlook_for_ph_cities'):
        os.makedirs('data/raw/weather_outlook_for_ph_cities')

def extract_beautiful_soup_object(url: str) -> BeautifulSoup | None:
    '''
    Function to extract the BeautifulSoup object of weather 
    outlook for selected Philippine cities from the PAGASA-DOST 
    website.

    :param url: Url of the PAGASA-DOST website that consist of weather outlook for selected Philippine cities
    :type url: str
    :return: BeautifulSoup object to navigate and manipulate the entire content of the web-page
    :rtype: BeautifulSoup | None
    '''
    response = requests.get(url)

    # We need to check if the status code of the response for the request is unsuccessful
    if response.status_code != 200:
        return None
    
    # Parse as a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_issued_datetime(soup: BeautifulSoup) -> str:
    '''
    Function to extract the issued datetime of
    weather outlook for selected Philippine cities 
    from the PAGASA-DOST website.

    :param soup: BeautifulSoup object to navigate and manipulate the entire content of the web-page
    :type soup: BeautifulSoup
    :return: Issued datetime of weather outlook for selected Philippine cities
    :rtype: str
    '''
    issued_datetime = ''

    # Extract the necessary html tags to get the issued datetime of weather outlook for selected Philippine cities
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_and_valid_period_tag = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    # We need to check if the div_tag_with_validity_class is not missing
    if div_tag_with_validity_class is not None:
        issued_datetime_tag = div_tag_with_validity_class.find('b')
        issued_datetime = str(issued_datetime_tag.text).strip()
        issued_datetime = ' '.join(issued_datetime.split()) # Using split() method to remove extra whitespaces in between words

    return issued_datetime

def save_issued_datetime_to_json(issued_datetime: str) -> None:
    '''
    Function to save the issued datetime of weather outlook for
    selected Philippine cities to a dedicated json file of the 
    data/raw/weather_outlook_for_ph_cities/ subdirectory from your local machine.

    :param issued_datetime: Issued datetime of weather outlook for selected Philippine cities
    :type issued_datetime: str
    '''
    # Create a dictionary that stores the issued datetime of weather outlook for selected Philippine cities
    data = {
        "issued_datetime": issued_datetime
    }

    # Save the dictionary to a json file using open() method and json module
    with open('data/raw/weather_outlook_for_ph_cities/issued_datetime.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_valid_period(soup: BeautifulSoup) -> str:
    '''
    Function to extract the valid period of weather
    outlook for selected Philippine cities from the
    PAGASA-DOST website.

    :param soup: BeautifulSoup object to navigate and manipulate the entire content of the web-page
    :type soup: BeautifulSoup
    :return: Valid period of weather outlook for selected Philippine cities
    :rtype: str
    '''
    valid_period = ''

    # Extract the necessary html tags to get the valid period of weather outlook for selected Philippine cities
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_and_valid_period_tag = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    # We need to check if the div_tag_with_validity_class is not missing
    if div_tag_with_validity_class is not None:
        valid_period_tag = div_tag_with_validity_class.find_all('b')[1]
        valid_period = str(valid_period_tag.text).strip()

    return valid_period

def save_valid_period_to_json(valid_period: str) -> None:
    '''
    Function to save the valid period of weather outlook for
    selected Philippine cities to a dedicated json file of the 
    data/raw/weather_outlook_for_ph_cities/ subdirectory from your local machine.
        
    :param valid_period: Valid period of weather outlook for selected Philippine cities
    :type valid_period: str
    '''

    # Create a dictionary that stores the valid period of weather outlook for selected Philippine cities
    data = {
        "valid_period": valid_period
    }

    # Save the dictionary to a json file using open() method and json module
    with open('data/raw/weather_outlook_for_ph_cities/valid_period.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    json_file.close()

def extract_ph_city_tags(soup: BeautifulSoup) -> list[BeautifulSoup | None]:
    '''
    Function to extract selected Philippine city
    tags to get their weather outlook from the
    PAGASA-DOST website.
            
    :param soup: BeautifulSoup object to navigate and manipulate the entire content of the web-page
    :type soup: BeautifulSoup
    :return: List of all selected Philippine city HTML tags
    :rtype: list[BeautifulSoup | None]
    '''
    list_of_all_ph_city_tags = []

    # Extract the necessary html tags to get all selected Philippine city tags for their weather outlook
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    weather_outlook_for_ph_city_tag = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 col-lg-12'})
    div_tag_with_panel_group_class = weather_outlook_for_ph_city_tag.find('div', attrs={'class': 'panel-group'})

    # We need to check if the div_tag_with_panel_group_class is missing
    if div_tag_with_panel_group_class is None:
        return list_of_all_ph_city_tags

    # Using for-loop to access all selected Philippine city tags
    list_of_all_ph_city_tags = div_tag_with_panel_group_class.find_all('div', attrs={'class': 'panel panel-default panel-pagasa'})
    return list_of_all_ph_city_tags

def extract_ph_city_names(list_of_all_ph_city_tags: list[BeautifulSoup]) -> dict[str, dict]:
    '''
    Function to extract all the name of selected Philippine cities to get their weather
    outlook from the PAGASA-DOST website.

    :param list_of_all_ph_city_tags: List of all selected Philippine city HTML tags
    :type list_of_all_ph_city_tags: list[BeautifulSoup]
    :return: Selected Philippine city names dictionary
    :rtype: dict[str, dict]
    '''
    result = {}

    # Using for-loop to access rows that contains the necessary html tags to get the name of all selected Philippine city
    for ph_city_tag in list_of_all_ph_city_tags:
        ph_city_name_tag = ph_city_tag.find('a')
        ph_city_name = str(ph_city_name_tag.text).strip()
        result[ph_city_name] = {}

    return result

def map_weather_dates_to_ph_cities(list_of_all_ph_city_tags: list[BeautifulSoup], ph_city_names: dict[str, dict]) -> dict[str, dict]:
    '''
    Function to map extracted weather dates for selected Philippine cities to get their weather outlook
    from the PAGASA-DOST website.

    :param list_of_all_ph_city_tags: List of all selected Philippine city HTML tags
    :type list_of_all_ph_city_tags: list[BeautifulSoup]
    :param ph_city_names: Selected Philippine city names dictionary
    :type ph_city_names: dict[str, dict]
    :rtype: dict[str, dict]
    :return: Selected Philippine city names with weather dates dictionary
    '''
    result = ph_city_names

    # Using for-loop to access rows that contains the necessary html tags to get weather dates for selected Philippine cities
    for ph_city_tag in list_of_all_ph_city_tags:
        ph_city_name_tag = ph_city_tag.find('a')
        ph_city_name = str(ph_city_name_tag.text).strip()

        table_tag = ph_city_tag.find('table', attrs={'class': 'table'})
        # Using find_all() method to retrieve all weather dates for selected Philippine cities
        list_of_all_table_header_tags = table_tag.find_all('th')

        weather_dates = []

        for table_header_tag in list_of_all_table_header_tags:
            weather_date = str(table_header_tag.text).strip()
            weather_dates.append(weather_date)

        # Map weather dates to selected Philippine cities
        result[ph_city_name]['weather_dates'] = weather_dates

    return result

def map_temperature_ranges_to_ph_cities(list_of_all_ph_city_tags: list[BeautifulSoup], ph_cities_with_weather_dates: dict[str, dict]) -> dict[str, dict]:
    '''
    Function to map extracted temperature ranges per weather dates for selected Philippine cities to get their weather outlook
    from the PAGASA-DOST website.

    :param list_of_all_ph_city_tags: List of all selected Philippine city HTML tags
    :type list_of_all_ph_city_tags: list[BeautifulSoup]
    :param ph_cities_with_weather_dates: Selected Philippine city names with weather dates dictionary
    :type ph_cities_with_weather_dates: dict[str, dict]
    :return: Selected Philippine city names with temperature ranges per weather dates dictionary
    :rtype: dict[str, dict]
    '''
    result = ph_cities_with_weather_dates

    # Using for-loop to access rows that contains the necessary html tags to get temperature ranges for selected Philippine cities
    for ph_city_tag in list_of_all_ph_city_tags:
        ph_city_name_tag = ph_city_tag.find('a')
        ph_city_name = str(ph_city_name_tag.text).strip()

        table_tag = ph_city_tag.find('table', attrs={'class': 'table'})
        temperature_ranges_and_chances_of_rain_pct_tag = table_tag.find('tr', attrs={'class': 'desktop-view-tr'})
        # Using find_all() method to retrieve all temperature ranges for selected Philippine cities
        list_of_all_table_data_tags = temperature_ranges_and_chances_of_rain_pct_tag.find_all('td')

        temperature_ranges = []

        for table_data_tag in list_of_all_table_data_tags:
            minimum_temperature_tag = table_data_tag.find('span', attrs={'class': 'min'})
            minimum_temperature = str(minimum_temperature_tag.text).strip()

            maximum_temperature_tag = table_data_tag.find('span', attrs={'class': 'max'})
            maximum_temperature = str(maximum_temperature_tag.text).strip()

            temperature_ranges.append([minimum_temperature, maximum_temperature])

        # Map temperature ranges per weather dates to selected Philippine cities
        result[ph_city_name]['temperature_ranges'] = temperature_ranges
    
    return result

def map_chances_of_rain_pct_to_ph_cities(list_of_all_ph_city_tags: list[BeautifulSoup], ph_cities_weather_outlook: dict[str, dict]) -> dict[str, dict]:
    '''
    Function to map extracted percentage of chances of rain per weather dates for selected Philippine cities to get their weather outlook
    from the PAGASA-DOST website.

    :param list_of_all_ph_city_tags: List of all selected Philippine city HTML tags
    :type list_of_all_ph_city_tags: list[BeautifulSoup]
    :param ph_cities_weather_outlook: Description
    :type ph_cities_weather_outlook: Selected Philippine city names with temperature ranges per weather dates dictionary
    :return: Selected Philippine city names with temperature ranges and percentage of chances of rain per weather dates dictionary
    :rtype: dict[str, dict]
    '''
    result = ph_cities_weather_outlook

    for ph_city_tag in list_of_all_ph_city_tags:
        ph_city_name_tag = ph_city_tag.find('a')
        ph_city_name = str(ph_city_name_tag.text).strip()

        table_tag = ph_city_tag.find('table', attrs={'class': 'table'})
        temperature_ranges_and_chances_of_rain_pct_tag = table_tag.find('tr', attrs={'class': 'desktop-view-tr'})
        list_of_all_table_data_tags = temperature_ranges_and_chances_of_rain_pct_tag.find_all('td')