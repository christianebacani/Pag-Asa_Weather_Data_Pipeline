'''
    Module to ingest weather outlook for selected
    Philippine tourist areas from the PAGASA-DOST
    website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Creates the data/raw/weather_outlook_for_ph_tourist_areas/
        subdirectory to store JSON files for daily weather
        forecast data ingested from the PAGASA-DOST website.
    '''
    # Create the data/raw/weather_outlook_for_ph_cities/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weather_outlook_for_ph_tourist_areas'):
        os.makedirs('data/raw/weather_outlook_for_ph_tourist_areas')

def extract_beautiful_soup_object(
        url: str
) -> BeautifulSoup | None:
    '''
    Extracts the BeautifulSoup object
    of the weather outlook for selected
    Philippine tourist areas from the
    PAGASA-DOST website.

    :param url: URL of the PAGASA-DOST
        page containing the weather outlook
        for selected Philippine tourist areas.
    :type url: str

    :return: BeautifulSoup object for navigating
        the page content, or None if extraction
        fails.
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
    outlook for selected Philippine tourist areas
    from the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating
        and manipulating the page content
    :type soup: BeautifulSoup

    :return: Issued datetime of the weather outlook for
        selected Philippine tourist areas
    :rtype: str
    '''
    issued_datetime = ''

    # Extract HTML tags for issued datetime of the weather outlook for selected Philippine tourist areas
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
    
    return issued_datetime

def save_issued_datetime_to_json(
        issued_datetime: str
) -> None:
    '''
    Saves the issued datetime of the
    weather outlook for selected Philippine
    tourist areas to a JSON file in the
    data/raw/weather_outlook_for_ph_tourist_areas/
    subdirectory on the local machine.

    :param issued_datetime: Issued datetime
        of the weather outlook for selected
        Philippine tourist areas
    :type issued_datetime: str
    '''
    # Create a dictionary to store issued datetime of the weather outlook for selected Philippine tourist areas
    data = {
        "issued_datetime": issued_datetime
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/weather_outlook_for_ph_tourist_areas/issued_datetime.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_valid_period(
        soup: BeautifulSoup
) -> str:
    '''
    Extracts the valid period of the weather
    outlook for selected Philippine tourist areas
    from the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating
        and manipulating the page content
    :type soup: BeautifulSoup

    :return: Valid period of the weather outlook for
        selected Philippine tourist areas
    :rtype: str
    '''
    valid_period = ''

    # Extract HTML tags for valid period of the weather outlook for selected Philippine tourist areas
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
    tourist areas to a JSON file in the
    data/raw/weather_outlook_for_ph_tourist_areas/
    subdirectory on the local machine.

    :param issued_datetime: Valid period of
        the weather outlook for selected Philippine
        tourist areas
    :type issued_datetime: str
    '''
    # Create a dictionary to store valid period of the weather outlook for selected Philippine tourist areas
    data = {
        "valid_period": valid_period
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/weather_outlook_for_ph_tourist_areas/valid_period.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_ph_tourist_area_tags(
        soup: BeautifulSoup
) -> list[BeautifulSoup | None]:
    '''
    Extracts selected Philippine tourist area tags to get
    their weather outlook from the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating and
        manipulating the page content
    :type soup: BeautifulSoup
    
    :return: List of selected Philippine tourist area HTML
        tags
    :rtype: list[BeautifulSoup | None]
    '''
    list_of_all_ph_tourist_area_tags = []

    # Extract HTML tags for all selected Philippine tourist areas to get their weather outlook
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    weather_outlook_for_ph_tourist_area_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )
    table_tag = weather_outlook_for_ph_tourist_area_tag.find('table', attrs={'class': 'table desktop'})

    # We need to check if the table_tag is missing
    if table_tag is None:
        return list_of_all_ph_tourist_area_tags

    tbody_tag = table_tag.find('tbody')
    # Use find_all() method to access all selected Philippine tourist area HTML tags
    list_of_all_ph_tourist_area_tags = tbody_tag.find_all('tr')

    return list_of_all_ph_tourist_area_tags

def extract_ph_tourist_area_names(
        list_of_all_ph_tourist_area_tags: list[BeautifulSoup]
) -> dict[str, dict]:
    '''
    Extracts the names of selected Philippine tourist areas
    to get their weather outlook from the PAGASA-DOST website.

    :param list_of_all_ph_city_tags: List of selected
        Philippine tourist area HTML tags
    :type list_of_all_ph_city_tags: list[BeautifulSoup]

    :return: Dictionary of selected Philippine tourist area
        names
    :rtype: dict[str, dict]
    '''
    result = {}

    # Loop through rows containing HTML tags to extract the names of the selected Philippine tourist areas
    for ph_tourist_area_tag in list_of_all_ph_tourist_area_tags:
        ph_tourist_area_name_tag = ph_tourist_area_tag.find('td')
        ph_tourist_area_name = str(ph_tourist_area_name_tag.text).strip()
        # Use replace() to remove extra whitespace after '(' in Philippine tourist area names
        ph_tourist_area_name = ph_tourist_area_name.replace('( ', '(')
        result[ph_tourist_area_name] = {}

    return result

def extract_weather_dates(
        soup: BeautifulSoup
) -> list[str]:
    '''
    Extracts all weather dates for the weather
    outlook of selected Philippine tourist areas.

    :param soup: BeautifulSoup object for navigating
        and manipulating the page content
    :type soup: BeautifulSoup

    :return: List of weather dates for the selected
        Philippine tourist areas
    :rtype: list[str]
    '''
    weather_dates = []

    # Extract HTML tags to get all weather dates of selected Philippine tourist areas
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    weather_outlook_for_ph_tourist_area_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-md-12 col-lg-12'
        }
    )
    table_tag = weather_outlook_for_ph_tourist_area_tag.find('table', attrs={'class': 'table desktop'})

    # We need to check if the table_tag is missing
    if table_tag is None:
        return weather_dates

    thead_tag = table_tag.find('thead')
    # Use find_all() method to access all weather dates
    list_of_all_table_header_tags = thead_tag.find_all('th')[1:]

    # Loop through rows containing HTML tags to extract the weather dates of selected Philippine tourist areas
    for table_header_tag in list_of_all_table_header_tags:
        weather_date = str(table_header_tag.text).strip()
        # Use split() method to remove extra whitespaces in between words
        weather_date = ' '.join(weather_date.split())
        weather_dates.append(weather_date)

    return weather_dates

def map_weather_dates_to_ph_tourist_areas(
        weather_dates: list[str],
        ph_tourist_area_names: dict[str, dict]
) -> dict[str, dict]:
    '''
    Maps extracted weather dates to selected Philippine
    tourist areas for their weather outlook from the
    PAGASA-DOST website.

    :param weather_dates: List of weather dates for the
        selected Philippine tourist areas
    :type weather_dates: list[str]

    :param ph_tourist_area_names: Dictionary of selected
        Philippine tourist area names
    :type ph_tourist_area_names: dict[str, dict]

    :return: Dictionary of tourist area names with
        corresponding weather dates
    :rtype: dict[str, dict]
    '''
    result = ph_tourist_area_names

    list_of_all_ph_tourist_area_names = list(result.keys())

    # Loop through the list of selected Philippine tourist areas to map it to the extracted weather dates
    for ph_tourist_area_name in list_of_all_ph_tourist_area_names:
        # Map weather dates to the selected Philippine tourist area
        result[ph_tourist_area_name]['weather_dates'] = weather_dates

    return result

def extract_temperature_ranges(
        list_of_all_ph_tourist_area_tags: list[BeautifulSoup]
) -> list[list]:
    '''
    Extracts all temperature ranges for the weather
    outlook of selected Philippine tourist areas.        

    :param list_of_all_ph_tourist_area_tags: List
        of selected Philippine tourist area HTML tags
    :type list_of_all_ph_tourist_area_tags: list[BeautifulSoup]

    :return: List of temperature ranges for the selected
        Philippine tourist areas
    :rtype: list[list]
    '''
    result = []

    # Loop through Philippine tourist area tags to extract temperature range tags
    for ph_tourist_area_tag in list_of_all_ph_tourist_area_tags:
        list_of_all_table_data_tags = ph_tourist_area_tag.find_all('td')[1:]
        
        temperature_ranges = []

        # Loop through tags to extract temperature ranges for selected tourist areas
        for table_data_tag in list_of_all_table_data_tags:
            minimum_temperature_tag = table_data_tag.find('span', attrs={'class': 'min'})
            minimum_temperature = str(minimum_temperature_tag.text).strip()

            maximum_temperature_tag = table_data_tag.find('span', attrs={'class': 'max'})
            maximum_temperature = str(maximum_temperature_tag.text).strip()

            temperature_ranges.append([minimum_temperature, maximum_temperature])
        
        result.append(temperature_ranges)
    
    return result

def map_temperature_ranges_to_ph_tourist_areas(
        temperature_ranges: list[list],
        ph_tourist_areas_with_weather_dates: dict[str, dict]
) -> dict[str, dict]:
    '''
    Maps extracted temperature ranges to selected Philippine
    tourist areas for their weather outlook from the
    PAGASA-DOST website.

    :param temperature_ranges: List of temperature ranges
        for the selected Philippine tourist areas
    :type temperature_ranges: list[list]
    
    :param ph_tourist_areas_with_weather_dates: Dictionary
        of tourist area names with corresponding weather dates
    :type ph_tourist_areas_with_weather_dates: dict[str, dict]

    :return: Dictionary of tourist area names with weather dates
        and temperature ranges
    :rtype: dict[str, dict]
    '''
    result = ph_tourist_areas_with_weather_dates

    list_of_all_temperature_ranges = temperature_ranges
    list_of_all_ph_tourist_area_names = list(result.keys())

    # Loop through the list of temperature ranges to map it to the selected Philippine tourist areas
    for index, temperature_ranges in enumerate(list_of_all_temperature_ranges):
        # Use the index of temperature range to get the name of the Philippine tourist area
        ph_tourist_area_name = list_of_all_ph_tourist_area_names[index]
        # Map temperature ranges to the selected Philippine tourist area
        result[ph_tourist_area_name]['temperature_ranges'] = temperature_ranges
    
    return result

def save_ph_tourist_areas_weather_outlook_to_json(
        ph_tourist_areas_weather_outlook: dict[str, dict]
) -> None:
    '''
    Saves the weather outlook for selected Philippine
    tourist areas to a JSON file in the
    data/raw/weather_outlook_for_ph_tourist_areas/
    subdirectory on the local machine.

    :param ph_tourist_areas_weather_outlook: Dictionary
        of tourist area names with weather dates and
        temperature ranges
    :type ph_tourust_areas_weather_outlook: dict[str, dict]
    '''
    # Create a dictionary to store weather outlook of selected Philippine tourist areas
    data = ph_tourist_areas_weather_outlook

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/weather_outlook_for_ph_tourist_areas/ph_tourist_areas_weather_outlook.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)
    
    json_file.close()