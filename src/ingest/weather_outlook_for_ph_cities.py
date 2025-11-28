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

def map_weather_dates_to_ph_cities(
        list_of_all_ph_city_tags: list[BeautifulSoup],
        ph_city_names: dict[str, dict]
) -> dict[str, dict]:
    '''
    Maps extracted weather dates to selected Philippine cities
    for their weather outlook from the PAGASA-DOST website.

    :param list_of_all_ph_city_tags: List of selected Philippine
    city HTML tags
    :type list_of_all_ph_city_tags: list[BeautifulSoup]

    :param ph_city_names: Dictionary of selected Philippine city names
    :type ph_city_names: dict[str, dict]
    
    :return: Dictionary of city names with corresponding weather dates
    :rtype: dict[str, dict]
    '''
    result = ph_city_names

    # Loop through rows with HTML tags to extract selected Philippine city names and their weather dates
    for ph_city_tag in list_of_all_ph_city_tags:
        ph_city_name_tag = ph_city_tag.find('a')
        ph_city_name = str(ph_city_name_tag.text).strip()

        table_tag = ph_city_tag.find('table', attrs={'class': 'table'})
        # Use find_all() to retrieve all weather dates
        list_of_all_table_header_tags = table_tag.find_all('th')

        weather_dates = []

        for table_header_tag in list_of_all_table_header_tags:
            weather_date = str(table_header_tag.text).strip()
            weather_date = ' '.join(weather_date.split())
            weather_dates.append(weather_date)

        # Map weather dates to each selected Philippine city
        result[ph_city_name]['weather_dates'] = weather_dates

    return result

def map_temperature_ranges_to_ph_cities(
        list_of_all_ph_city_tags: list[BeautifulSoup],
        ph_cities_with_weather_dates: dict[str, dict]
) -> dict[str, dict]:
    '''
    Maps extracted temperature ranges per weather date
    to selected Philippine cities for their weather
    outlook from the PAGASA-DOST website.

    :param list_of_all_ph_city_tags: List of selected
    Philippine city HTML tags
    :type list_of_all_ph_city_tags: list[BeautifulSoup]
    
    :param ph_cities_with_weather_dates: Dictionary of
    selected city names with weather dates
    :type ph_cities_with_weather_dates: dict[str, dict]
    
    :return: Dictionary of city names with temperature ranges per weather date
    :rtype: dict[str, dict]
    '''
    result = ph_cities_with_weather_dates

    # Loop through rows with HTML tags to extract city names, weather dates, and temperature ranges
    for ph_city_tag in list_of_all_ph_city_tags:
        ph_city_name_tag = ph_city_tag.find('a')
        ph_city_name = str(ph_city_name_tag.text).strip()

        table_tag = ph_city_tag.find('table', attrs={'class': 'table'})
        temperature_ranges_and_chances_of_rain_pct_tag = table_tag.find(
            'tr',
            attrs={
                'class': 'desktop-view-tr'
            }
        )
        # Use find_all() to retrieve all temperature ranges data
        list_of_all_table_data_tags = temperature_ranges_and_chances_of_rain_pct_tag.find_all('td')

        temperature_ranges = []

        for table_data_tag in list_of_all_table_data_tags:
            minimum_temperature_tag = table_data_tag.find('span', attrs={'class': 'min'})
            minimum_temperature = str(minimum_temperature_tag.text).strip()

            maximum_temperature_tag = table_data_tag.find('span', attrs={'class': 'max'})
            maximum_temperature = str(maximum_temperature_tag.text).strip()

            temperature_ranges.append([minimum_temperature, maximum_temperature])

        # Map temperature ranges to each selected Philippine city by weather date
        result[ph_city_name]['temperature_ranges'] = temperature_ranges

    return result

def map_chances_of_rain_pct_to_ph_cities(
        list_of_all_ph_city_tags: list[BeautifulSoup],
        ph_cities_weather_outlook: dict[str, dict]
) -> None:
    '''
    Maps extracted percentages of chance of rain per weather
    date to selected Philippine cities for their weather
    outlook from the PAGASA-DOST website.

    :param list_of_all_ph_city_tags: List of selected
    Philippine city HTML tags
    :type list_of_all_ph_city_tags: list[BeautifulSoup]
    
    :param ph_cities_weather_outlook: Dictionary of selected
    city names with temperature ranges per weather date
    :type ph_cities_weather_outlook: dict[str, dict]
    
    :return: Dictionary of city names with temperature ranges
    and chance of rain per weather date
    :rtype: dict[str, dict]
    '''
    result = ph_cities_weather_outlook

    # Loop through rows with HTML tags to extract city names, weather dates, temperature ranges, and rain chance percentages  
    for ph_city_tag in list_of_all_ph_city_tags:
        ph_city_name_tag = ph_city_tag.find('a')
        ph_city_name = str(ph_city_name_tag.text).strip()

        table_tag = ph_city_tag.find('table', attrs={'class': 'table'})
        temperature_ranges_and_chances_of_rain_pct_tag = table_tag.find(
            'tr',
            attrs={
                'class': 'desktop-view-tr'
            }
        )
        # Use find_all() to retrieve all rain chance percentages data
        list_of_all_table_data_tags = temperature_ranges_and_chances_of_rain_pct_tag.find_all('td')

        chances_of_rain_percentages = []

        for table_data_tag in list_of_all_table_data_tags:
            chances_of_rain_pct_tag = table_data_tag.find(
                'span',
                attrs={
                    'style': 'font-weight:bold; color: rgb(9, 73, 156);'
                }
            )
            chances_of_rain_pct = str(chances_of_rain_pct_tag.text).strip()
            chances_of_rain_percentages.append(chances_of_rain_pct)

        # Map chances of rain percentage to each selected Philippine city by weather date
        result[ph_city_name]['chances_of_rain_percentages'] = chances_of_rain_percentages

    return result

def save_ph_cities_weather_outlook_to_json(
        ph_cities_weather_outlook: dict[str, dict]
) -> None:
    '''
    Saves the weather outlook of selected Philippine
    cities to a JSON file in the
    data/raw/weather_outlook_for_ph_cities/ subdirectory
    on the local machine.

    :param ph_cities_weather_outlook: Dictionary of city
    names with temperature ranges and rain chances per
    weather date
    :type ph_cities_weather_outlook: dict[str, dict]
    '''
    # Create a dictionary to store weather outlook of the selected Philippine cities
    data = {}

    for ph_city_name, weather_outlook in ph_cities_weather_outlook.items():
        data[ph_city_name] = {
            "weather_dates": weather_outlook['weather_dates'],
            "temperature_ranges": weather_outlook['temperature_ranges'],
            "chances_of_rain_percentages": weather_outlook['chances_of_rain_percentages']
        }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/weather_outlook_for_ph_cities/ph_cities_weather_outlook.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()