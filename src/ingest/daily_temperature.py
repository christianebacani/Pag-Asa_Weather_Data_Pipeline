'''
    Module to ingest daily temperature
    including top 10 lowest and top 10
    highest temperatures recorded across
    different weather stations from the
    PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Creates the data/raw/daily_temperature/
        subdirectory to store JSON files for top
        10 lowest and top 10 highest temperature
        data ingested from the daily temperature
        page of the PAGASA-DOST website.
    '''
    # Create the data/raw/daily_temperature/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/daily_temperature'):
        os.makedirs('data/raw/daily_temperature')

def extract_beautiful_soup_object(
        url: str
) -> BeautifulSoup | None:
    '''
    Extracts the BeautifulSoup object of
    the daily temperature page from the
    PAGASA-DOST website.

    :param url: URL of the PAGASA-DOST page
        containing the daily temperature
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

def extract_top_10_lowest_temps_table_tag(
        soup: BeautifulSoup | None
) -> BeautifulSoup | None:
    '''
    Extracts top 10 lowest temperatures table
    tag to get it's corresponding data from the
    daily temperature page of the PAGASA-DOST
    website.

    :param soup: BeautifulSoup object for
        navigating and manipulating the page
        content, or None if extraction fails
    :type soup: BeautifulSoup | None

    :return: Top 10 lowest temperatures table
        HTML tag, or None if extraction fails
    :rtype: BeautifulSoup | None
    '''
    # We need to check if the BeautifulSoup object is missing
    if soup is None:
        return None

    # Extract HTML tags to get the data for the top 10 lowest temperatures table
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    top_10_lowest_temps_table_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-md-6'
        }
    )
    div_tag_with_panel_class = top_10_lowest_temps_table_tag.find('div', attrs={'class': 'panel'})
    top_10_lowest_temps_table_tag = div_tag_with_panel_class

    return top_10_lowest_temps_table_tag

def extract_recorded_date_of_lowest_temp(
        top_10_lowest_temps_table_tag: BeautifulSoup | None
) -> str:
    '''
    Extracts the recorded date of lowest temperature
    from daily temperature page of PAGASA-DOST website.

    :param lowest_temperature_table_tag: Top 10 lowest
        temperatures table HTML tag, or None if extration
        fails
    :type lowest_temperature_table_tag: BeautifulSoup | None

    :return: Recorded date of lowest temperature
    :rtype: str
    '''
    recorded_date_of_lowest_temp = ''

    # We need to check if the top 10 lowest temperatures table HTML tag is missing
    if top_10_lowest_temps_table_tag is None:
        return recorded_date_of_lowest_temp

    top_10_lowest_temps_header_tag = top_10_lowest_temps_table_tag.find(
        'div',
        attrs={
            'class': 'panel-heading'
        }
    )
    top_10_lowest_temps_header = str(top_10_lowest_temps_header_tag.text)
    recorded_date_of_lowest_temp = top_10_lowest_temps_header.replace(
        'Top 10 Lowest Temperature as of',
        ''
    ).strip()

    return recorded_date_of_lowest_temp

def save_recorded_date_of_lowest_temp_to_json(
        recorded_date_of_lowest_temp: str
) -> None:
    '''
    Saves the recorded date of lowest temperature
    to a JSON file in the data/raw/daily_temperature/
    subdirectory on the local machine.

    :param recorded_date_of_lowest_temp: Recorded
        date of lowest temperature
    :type recorded_date_of_lowest_temp: str
    '''
    # Create a dictionary to store the recorded date of lowest temperature
    data = {
        "recorded_date_of_lowest_temp": recorded_date_of_lowest_temp
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/daily_temperature/recorded_date_of_lowest_temp.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_station_names_from_top_10_lowest_temps(
        top_10_lowest_temps_table_tag: BeautifulSoup | None
) -> list[str]:
    '''
    Extracts the list of station names from the top 10
    lowest temperatures table of daily temperature page
    from the PAGASA-DOST website.

    :param top_10_lowest_temps_table_tag: Top 10 lowest
        temperatures table HTML tag, or None if extraction
        fails
    :type top_10_lowest_temps_table_tag: BeautifulSoup | None

    :return: List of station names from the top 10 lowest
        temperatures table
    :rtype: list[str]
    '''
    station_names_from_top_10_lowest_temps = []

    # We need to check if the top 10 lowest temperatures table HTML tag is missing
    if top_10_lowest_temps_table_tag is None:
        return station_names_from_top_10_lowest_temps

    tbody_tag = top_10_lowest_temps_table_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return station_names_from_top_10_lowest_temps

    # Use find_all() method to access all station names
    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    # Loop through rows containing HTML tags to extract all station names from top 10 lowest temps table
    for table_row_tag in list_of_all_table_row_tags:
        station_name_tag = table_row_tag.find('td')
        station_name = str(station_name_tag.text).strip()
        station_names_from_top_10_lowest_temps.append(station_name)

    return station_names_from_top_10_lowest_temps

def extract_temperatures_from_top_10_lowest_temps(
        top_10_lowest_temps_table_tag: BeautifulSoup | None
) -> list[str]:
    '''
    Extracts the list of temperatures from the the top 10
    lowest temperatures table of the daily temperature page
    from the PAGASA-DOST website.

    :param top_10_lowest_temps_table_tag: Top 10 lowest
        temperatures table HTML tag, or None if extraction fails
    :type top_10_lowest_temps_table_tag: BeautifulSoup | None

    :return: List of temperatures from the top 10 lowest
        temperatures table
    :rtype: list[str]
    '''
    temperatures_from_top_10_lowest_temps = []

    # We need to check if the top 10 lowest temperatures table HTML tag is missing
    if top_10_lowest_temps_table_tag is None:
        return top_10_lowest_temps_table_tag

    tbody_tag = top_10_lowest_temps_table_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return temperatures_from_top_10_lowest_temps

    # Use find_all() method to access all temperatures
    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    # Loop through rows containing HTML tags to extract all temperatures from top 10 lowest temps table
    for table_row_tag in list_of_all_table_row_tags:
        temperature_tag = table_row_tag.find_all('td')[1]
        temperature = str(temperature_tag.text).strip()
        temperatures_from_top_10_lowest_temps.append(temperature)
    
    return temperatures_from_top_10_lowest_temps

def map_station_names_to_lowest_temps(
        station_names_from_top_10_lowest_temps: list[str],
        temperatures_from_top_10_lowest_temps: list[str]
) -> dict[str, str]:
    '''
    Maps extracted list of station names to 
    the list of extracted temperatures from
    the top 10 lowest temperatures table of
    daily temperature page from PAGASA-DOST
    website.

    :param station_names_from_top_10_lowest_temps:
        List of station names from the top 10
        lowest temperatures table
    :type station_names_from_top_10_lowest_temps:
        list[str]

    :param temperatures_from_top_10_lowest_temps:
        List of temperatures from the top 10
        lowest temperatures table
    :type temperatures_from_top_10_lowest_temps:
        list[str]

    :return: Dictionary of top 10 lowest
        temperatures table
    :rtype: dict[str, str]
    '''
    result = {}

    # We need to check if station names list or temperatures list for top 10 lowest temp table is missing
    if station_names_from_top_10_lowest_temps == [] or temperatures_from_top_10_lowest_temps == []:
        return {}

    list_of_all_station_names = station_names_from_top_10_lowest_temps
    list_of_all_temperatures = temperatures_from_top_10_lowest_temps

    # Loop through the station names list to map it to the temperatures list
    for index, station_name in enumerate(list_of_all_station_names):
        # Use the index of station names list to get the temperature
        temperature = list_of_all_temperatures[index]
        # Map station name to the selected temperature
        result[station_name] = temperature

    return result

def save_top_10_lowest_temps_to_json(
        top_10_lowest_temperatures: dict[str, str]
) -> None:
    '''
    Saves the top 10 lowest temperatures table
    to a JSON file in the data/raw/daily_temperature/
    subdirectory on the local machine.

    :param top_10_lowest_temperatures: Dictionary of
        top 10 lowest temperatures table
    :type top_10_lowest_temperatures: dict[str, str]
    '''
    # Create a dictionary to store the top 10 lowest temperatures table
    data = top_10_lowest_temperatures

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/daily_temperature/top_10_lowest_temperatures.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_top_10_highest_temps_table_tag(
        soup: BeautifulSoup | None
) -> BeautifulSoup | None:
    '''
    Extracts top 10 highest temperatures table
    tag to get it's corresponding data from the
    daily temperature page of the PAGASA-DOST
    website.

    :param soup: BeautifulSoup object for
        navigating and manipulating the page
        content, or None if extraction fails
    :type soup: BeautifulSoup | None

    :return: Top 10 highest temperatures table
        HTML tag, or None if extraction fails
    :rtype: BeautifulSoup | None
    '''
    # We need to check if the BeautifulSoup object is missing
    if soup is None:
        return None

    # Extract HTML tags to get the data for the top 10 highest temperatures table
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    top_10_highest_temps_table_tag = div_tag_with_row_weather_page_class.find_all(
        'div',
        attrs={
            'class': 'col-md-6'
        }
    )[1]
    div_tag_with_panel_class = top_10_highest_temps_table_tag.find('div', attrs={'class': 'panel'})    
    top_10_highest_temps_table_tag = div_tag_with_panel_class

    return top_10_highest_temps_table_tag

def extract_recorded_date_of_highest_temp(
        top_10_highest_temps_table_tag: BeautifulSoup | None
) -> str:
    '''
    Extracts the recorded date of highest temperature
    from daily temperature page of PAGASA-DOST website.

    :param top_10_highest_temps_table_tag: Top 10 highest
        temperatures table HTML tag, or None if extration
        fails
    :type top_10_highest_temps_table_tag: BeautifulSoup | None

    :return: Recorded date of highest temperature 
    :rtype: str
    '''
    recorded_date_of_highest_temp = ''

    # We need to check if the top 10 highest temperatures table HTML tag is missing
    if top_10_highest_temps_table_tag is None:
        return recorded_date_of_highest_temp

    top_10_highest_temps_header_tag = top_10_highest_temps_table_tag.find(
        'div',
        attrs={
            'class': 'panel-heading'
        }
    )
    top_10_highest_temps_header = str(top_10_highest_temps_header_tag.text)
    recorded_date_of_highest_temp = top_10_highest_temps_header.replace(
        'Top 10 Highest Temperature as of',
        ''
    ).strip()

    return recorded_date_of_highest_temp

def save_recorded_date_of_highest_temp_to_json(
        recorded_date_of_highest_temp: str    
) -> None:
    '''
    Saves the recorded date of highest temperature
    to a JSON file in the data/raw/daily_temperature/
    subdirectory on the local machine.

    :param recorded_date_of_highest_temp: Recorded
        date of highest temperature
    :type recorded_date_of_highest_temp: str
    '''
    # Create a dictionary to store the recorded date of highest temperature
    data = {
        "recorded_date_of_highest_temperature": recorded_date_of_highest_temp
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/daily_temperature/recorded_date_of_highest_temp.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_station_names_from_top_10_highest_temps(
        top_10_hightest_temps_table_tag: BeautifulSoup | None        
) -> list[str]:
    '''    
    Extracts the list of station names from the top 10
    highest temperatures table of daily temperature page
    from the PAGASA-DOST website.

    :param top_10_hightest_temps_table_tag: Top 10 highest
        temperatures table HTML tag, or None if extraction
        fails
    :type top_10_hightest_temps_table_tag: BeautifulSoup | None

    :return: List of station names from the top 10 lowest
        temperatures table
    :rtype: list[str]
    '''
    station_names_from_top_10_highest_temps = []

    # We need to check if the top 10 highest temperatures table HTML tag is missing
    if top_10_hightest_temps_table_tag is None:
        return station_names_from_top_10_highest_temps

    tbody_tag = top_10_hightest_temps_table_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return station_names_from_top_10_highest_temps

    # Use find_all() method to access all station names
    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    # Loop through rows containing HTML tags to extract all station names from top 10 highest temps table
    for table_row_tag in list_of_all_table_row_tags:
        station_name_tag = table_row_tag.find('td')
        station_name = str(station_name_tag.text).strip()
        station_names_from_top_10_highest_temps.append(station_name)

    return station_names_from_top_10_highest_temps

def extract_temperatures_from_top_10_highest_temps(
        top_10_highest_temps_table_tag: BeautifulSoup | None
) -> list[str]:
    '''
    Extracts the list of temperatures from the the top 10
    highest temperatures table of the daily temperature page
    from the PAGASA-DOST website.

    :param top_10_highest_temps_table_tag: Top 10 highest
        temperatures table HTML tag, or None if extraction fails
    :type top_10_highest_temps_table_tag: BeautifulSoup | None

    :return: List of temperatures from the top 10 highest
        temperatures table
    :rtype: list[str]
    '''
    temperatures_from_top_10_highest_temps = []

    # We need to check if the top 10 highest temperatures table HTML tag is missing
    if top_10_highest_temps_table_tag is None:
        return top_10_highest_temps_table_tag

    tbody_tag = top_10_highest_temps_table_tag.find('tbody')

    # We need to check if the tbody_tag is missing
    if tbody_tag is None:
        return temperatures_from_top_10_highest_temps

    # Use find_all() method to access all temperatures
    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    # Loop through rows containing HTML tags to extract all temperatures from top 10 highest temps table
    for table_row_tag in list_of_all_table_row_tags:
        temperature_tag = table_row_tag.find_all('td')[1]
        temperature = str(temperature_tag.text).strip()
        temperatures_from_top_10_highest_temps.append(temperature)
    
    return temperatures_from_top_10_highest_temps