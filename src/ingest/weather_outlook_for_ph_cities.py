'''
    Module to ingest weather outlook for selected
    Philippine cities from the PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Creates the data/raw/weather_outlook_for_ph_cities/
        subdirectory to store JSON files for daily
        weather forecast data ingested from the
        PAGASA-DOST website.
    '''
    # Create the data/raw/weather_outlook_for_ph_cities/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weather_outlook_for_ph_cities'):
        os.makedirs('data/raw/weather_outlook_for_ph_cities')

def extract_beautiful_soup_object(
        url: str
) -> BeautifulSoup | None:
    '''
    Extracts the BeautifulSoup object of the
    weather outlook for selected Philippine
    cities page from the PAGASA-DOST website.

    :param url: URL of the PAGASA-DOST page
    containing the weather outlook for selected
    Philippine cities
    :type url: str

    :return: BeautifulSoup object for navigating
    and manipulating the page content, or None if
    extraction fails
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
    Extracts the issued datetime of the weather
    outlook for selected Philippine cities from
    the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating
    and manipulating the page content
    :type soup: BeautifulSoup

    :return: Issued datetime of the weather outlook for
    selected Philippine cities
    :rtype: str
    '''
    issued_datetime = ''

    # Extract HTML tags for issued datetime of the weather outlook for selected Philippine cities
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_and_valid_period_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12 issue'
        }
    )
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find(
        'div',
        attrs={
            'class': 'validity'
        }
    )

    # We need to check if the div_tag_with_validity_class is not missing
    if div_tag_with_validity_class is not None:
        issued_datetime_tag = div_tag_with_validity_class.find('b')
        issued_datetime = str(issued_datetime_tag.text).strip()
        # Use split() method to remove extra whitespaces in between words
        issued_datetime = ' '.join(issued_datetime.split())

    return issued_datetime

def save_issued_datetime_to_json(
        issued_datetime: str
) -> None:
    '''
    Saves the issued datetime of the
    weather outlook for selected Philippine
    cities to a JSON file in the
    data/raw/weather_outlook_for_ph_cities/
    subdirectory on the local machine.

    :param issued_datetime: Issued datetime
    of the weather outlook for selected
    Philippine cities
    :type issued_datetime: str
    '''
    # Create a dictionary to store issued datetime of the weather outlook for selected Philippine cities
    data = {
        "issued_datetime": issued_datetime
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/weather_outlook_for_ph_cities/issued_datetime.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_valid_period(
        soup: BeautifulSoup
) -> str:
    '''
    Extracts the valid period of the weather
    outlook for selected Philippine cities from
    the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating
    and manipulating the page content
    :type soup: BeautifulSoup

    :return: Valid period of the weather outlook for
    selected Philippine cities
    :rtype: str
    '''
    valid_period = ''

    # Extract HTML tags for valid period of the weather outlook for selected Philippine cities
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    issued_datetime_and_valid_period_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12 issue'
        }
    )
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find(
        'div',
        attrs={
            'class': 'validity'
        }
    )

    # We need to check if the div_tag_with_validity_class is not missing
    if div_tag_with_validity_class is not None:
        valid_period_tag = div_tag_with_validity_class.find_all('b')[1]
        valid_period = str(valid_period_tag.text).strip()

    return valid_period

def save_valid_period_to_json(
        valid_period: str
) -> None:
    '''
    Saves the valid period of the
    weather outlook for selected Philippine
    cities to a JSON file in the
    data/raw/weather_outlook_for_ph_cities/
    subdirectory on the local machine.

    :param issued_datetime: Valid period of
    the weather outlook for selected Philippine
    cities
    :type issued_datetime: str
    '''
    # Create a dictionary to store valid period of the weather outlook for selected Philippine cities
    data = {
        "valid_period": valid_period
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/weather_outlook_for_ph_cities/valid_period.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_ph_city_tags(
    soup: BeautifulSoup
) -> list[BeautifulSoup | None]:
    '''
    Extracts selected Philippine city tags to get their
    weather outlook from the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating and
    manipulating the page content
    :type soup: BeautifulSoup
    
    :return: List of selected Philippine city HTML tags
    :rtype: list[BeautifulSoup | None]
    '''
    list_of_all_ph_city_tags = []

    # Extract HTML tags for all selected Philippine cities to get their weather outlook
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    weather_outlook_for_ph_city_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )
    div_tag_with_panel_group_class = weather_outlook_for_ph_city_tag.find(
        'div',
        attrs={
            'class': 'panel-group'
        }
    )

    # We need to check if the div_tag_with_panel_group_class is missing
    if div_tag_with_panel_group_class is None:
        return list_of_all_ph_city_tags

    # Use find_all() method to access all selected Philippine city HTML tags
    list_of_all_ph_city_tags = div_tag_with_panel_group_class.find_all(
        'div',
        attrs={
            'class': 'panel panel-default panel-pagasa'
        }
    )

    return list_of_all_ph_city_tags

def extract_ph_city_names(
        list_of_all_ph_city_tags: list[BeautifulSoup]
) -> dict[str, dict]:
    '''
    Extracts the names of selected Philippine cities to
    get their weather outlook from the PAGASA-DOST
    website.

    :param list_of_all_ph_city_tags: List of selected
    Philippine city HTML tags
    :type list_of_all_ph_city_tags: list[BeautifulSoup]

    :return: Dictionary of selected Philippine city names
    :rtype: dict[str, dict]
    '''
    result = {}

    # Loop through rows containing HTML tags to extract the names of the selected Philippine cities
    for ph_city_tag in list_of_all_ph_city_tags:
        ph_city_name_tag = ph_city_tag.find('a')
        ph_city_name = str(ph_city_name_tag.text).strip()
        result[ph_city_name] = {}

    return result

def extract_weather_dates(
        soup: BeautifulSoup
) -> list[str]:
    '''
    Extracts all weather dates for the weather
    outlook of selected Philippine cities.

    :param soup: BeautifulSoup object for navigating
    and manipulating the page content
    :type soup: BeautifulSoup

    :return: List of weather dates for the selected
    Philippine cities
    :rtype: list[str]
    '''
    weather_dates = []

    # Extract HTML tags to get all weather dates of selected Philippine cities
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    weather_outlook_for_ph_city_tag = div_tag_with_row_weather_page_class.find(
        'div', 
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )
    div_tag_with_panel_group_class = weather_outlook_for_ph_city_tag.find(
        'div',
        attrs={
            'class': 'panel-group'
        }
    )

    # We need to check if the div_tag_with_panel_group_class is missing
    if div_tag_with_panel_group_class is None:
        return weather_dates

    ph_city_tag = div_tag_with_panel_group_class.find('div', attrs={'class': 'panel panel-default panel-pagasa'})
    table_tag = ph_city_tag.find('table', attrs={'class': 'table'})
    list_of_all_table_header_tags = table_tag.find_all('th')

    # Loop through rows containing HTML tags to extract the weather dates of selected Philippine cities
    for table_header_tag in list_of_all_table_header_tags:
        weather_date = str(table_header_tag.text).strip()
        # Use split() method to remove extra whitespaces in between words
        weather_date = ' '.join(weather_date.split())
        weather_dates.append(weather_date)

    return weather_dates

def map_weather_dates_to_ph_cities(
        weather_dates: list[str],
        ph_city_names: dict[str, dict]
) -> dict[str, dict]:
    '''
    Maps extracted weather dates to selected Philippine
    cities for their weather outlook from the PAGASA-DOST
    website.

    :param weather_dates: List of weather dates for the
    selected Philippine cities
    :type weather_dates: list[str]

    :param ph_tourist_area_names: Dictionary of selected
    Philippine city names
    :type ph_tourist_area_names: dict[str, dict]

    :return: Dictionary of city names with corresponding
    weather dates
    :rtype: dict[str, dict]
    '''
    result = ph_city_names

    list_of_all_ph_city_names = list(result.keys())
    
    # Loop through the selected Philippine cities to map it to the extracted weather dates
    for ph_city_name in list_of_all_ph_city_names:
        # Map weather dates to the selected Philippine city
        result[ph_city_name]['weather_dates'] = weather_dates
    
    return result

def extract_temperature_ranges(
        list_of_all_ph_city_tags: list[BeautifulSoup]
) -> list[list]:
    '''
    Extracts all temperature ranges for the weather
    outlook of selected Philippine cities.
    
    :param list_of_all_ph_city_tags: List of selected
    Philippine city HTML tags
    :type list_of_all_ph_city_tags: list[BeautifulSoup]

    :return: List of temperature ranges for the selected
    Philippine cities
    :rtype: list[list]
    '''
    result = []
    
    # Loop through Philippine city tags to extract temperature range tags
    for ph_city_tag in list_of_all_ph_city_tags:
        table_tag = ph_city_tag.find('table', attrs={'class': 'table'})
        temperature_ranges_tag = table_tag.find('tr', attrs={'class': 'desktop-view-tr'})
        list_of_all_table_data_tags = temperature_ranges_tag.find_all('td')

        temperature_ranges = []

        # Loop through temperature range tags to extract temperature ranges of selected Philippine cities
        for table_data_tag in list_of_all_table_data_tags:
            minimum_temperature_tag = table_data_tag.find('span', attrs={'class': 'min'})
            minimum_temperature = str(minimum_temperature_tag.text).strip()

            maximum_temperature_tag = table_data_tag.find('span', attrs={'class': 'max'})
            maximum_temperature = str(maximum_temperature_tag.text).strip()
            
            temperature_ranges.append([minimum_temperature, maximum_temperature])
        
        result.append(temperature_ranges)
    
    return result

def map_temperature_ranges_to_ph_cities(
        temperature_ranges: list[list],
        ph_cities_with_weather_dates: dict[str, dict]
) -> dict[str, dict]:
    '''
    Maps extracted temperature ranges to selected Philippine
    cities for their weather outlook from the PAGASA-DOST
    website.

    :param temperature_ranges: List of temperature ranges for
    the selected Philippine cities
    :type temperature_ranges: list[list]

    :param ph_cities_with_weather_dates: Dictionary of city
    names with corresponding weather dates
    :type ph_cities_with_weather_dates: dict[str, dict]

    :return: Dictionary of city names with weather dates and
    temperature ranges
    :rtype: dict[str, dict]
    '''
    result = ph_cities_with_weather_dates

    list_of_all_temperature_ranges = temperature_ranges
    list_of_all_ph_city_names = list(result.keys())

    # Loop through temperature ranges to map it to the selected Philippine cities
    for index, temperature_ranges in enumerate(list_of_all_temperature_ranges):
        # Use the index of the temperature ranges to get the corresponding name of the Philippine city
        ph_city_name = list_of_all_ph_city_names[index]

        # Map temperature ranges to the selected Philippine city
        result[ph_city_name]['temperature_ranges'] = temperature_ranges

    return result