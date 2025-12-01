'''
    Module to ingest weekly weather outlook
    from the PAGASA-DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir(
) -> None:
    '''
        Creates the data/raw/weekly_weather_outlook/
        subdirectory to store JSON files for weekly
        weather outlook data ingested from the PAGASA-
        DOST website.
    '''
    # Create the data/raw/weekly_weather_outlook/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weekly_weather_outlook'):
        os.makedirs('data/raw/weekly_weather_outlook')
    
def extract_beautiful_soup_object(
        url: str
) -> BeautifulSoup | None:
    '''
    Extracts the BeautifulSoup object of the
    weekly weather outlook page from the
    PAGASA-DOST website.

    :param url: URL of the PAGASA-DOST page
        containing the weekly weather outlook
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
    Extracts the issued datetime of weekly
    weather outlook from the PAGASA-DOST
    website.

    :param soup: BeautifulSoup object for navigating
        and manipulating the page content
    :type soup: BeautifulSoup

    :return: Issued datetime of the weekly weather
        outlook
    :rtype: str
    '''
    issued_datetime = ''

    # Extract HTML tags for issued datetime of the weekly weather outlook
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
    weekly weather outlook to a JSON
    file in the data/raw/weeekly_weather_outlook/
    subdirectory on the local machine.

    :param issued_datetime: Issued datetime
        of the weekly weather outlook
    :type issued_datetime: str
    '''
    # Create a dictionary to store issued datetime of the weekly weather outlook
    data = {
        "issued_datetime": issued_datetime
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/weekly_weather_outlook/issued_datetime.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)
    
    json_file.close()

def extract_valid_period(
        soup: BeautifulSoup
) -> str:    
    '''
    Extracts the valid period of the weekly
    weather outlook from the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating
        and manipulating the page content
    :type soup: BeautifulSoup

    :return: Valid period of the weekly weather outlook
    :rtype: str
    '''
    valid_period = ''

    # Extract HTML tags for valid period of the weekly weather outlook
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
    weekly weather outlook to a
    JSON file in the
    data/raw/weekly_weather_outlook/
    subdirectory on the local machine.

    :param issued_datetime: Valid period of
        weekly weather outlook
    :type issued_datetime: str
    '''
    # Create a dictionary to store valid period of the weekly weather outlook
    data = {
        "valid_period": valid_period
    }

    # Save the dictionary to a json file using open() method and json module
    with open(
        'data/raw/weekly_weather_outlook/valid_period.json',
        'w'
    ) as json_file:
        json.dump(data, json_file, indent=4)

    json_file.close()

def extract_date_ranges(
        soup: BeautifulSoup
) -> dict[str, str]:
    '''
    Extracts the date ranges of the weekly
    weather outlook from the PAGASA-DOST website.

    :param soup: BeautifulSoup object for navigating
        and manipulating the page content
    :type soup: BeautifulSoup

    :return: Dictionary of date ranges for weekly
        weather outlook
    :rtype: dict[str, str]
    '''
    date_ranges = {}

    # Extract HTML tags to get all date ranges for weekly weather outlook
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    weekly_weather_outlook_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-lg-12 col-md-12'
        }
    )
    table_tag = weekly_weather_outlook_tag.find('table', attrs={'class': 'table'})

    # We need to check if the table_tag is missing
    if table_tag is None:
        return date_ranges
    
    # Use find_all() method to access all date ranges
    list_of_all_table_row_tags = table_tag.find_all('tr')

    # Loop through rows containing HTML tags to extract the date ranges of weekly weather outlook
    for table_row_tag in list_of_all_table_row_tags:
        date_range_tag = table_row_tag.find('td')
        date_range = str(date_range_tag.text).strip()

        # We need to check if the date_range is not empty string
        if date_range != '':
            date_ranges[date_range] = ''

    return date_ranges

def extract_weather_outlooks(
        soup: BeautifulSoup
) -> list[str]:
    '''
    Extracts the weather outlooks
    for every date ranges from the
    PAGASA-DOST website.

    :param soup: BeautifulSoup
        object for navigating and
        manipulating the page
        content
    :type soup: BeautifulSoup

    :return: List of weather outlooks
        for every date ranges
    :rtype: list[str]
    '''
    weather_outlooks = []

    # Extract HTML tags to get all weather outlooks
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    weekly_weather_outlook_tag = div_tag_with_row_weather_page_class.find(
        'div',
        attrs={
            'class': 'col-lg-12 col-md-12'
        }
    )
    table_tag = weekly_weather_outlook_tag.find('table', attrs={'class': 'table'})

    # We need to check if the table_tag is missing
    if table_tag is None:
        return weather_outlooks

    # Use find_all() method to access all date ranges    
    list_of_all_table_row_tags = table_tag.find_all('tr')

    # Loop through rows containing HTML tags to extract the date ranges and weather outlooks
    for table_row_tag in list_of_all_table_row_tags:
        # Use find_all() method to access all date ranges and weather outlooks
        list_of_all_table_data_tags = table_row_tag.find_all('td')

        date_range_tag = list_of_all_table_data_tags[0]
        date_range = str(date_range_tag.text).strip()

        # We need to check if date_range is not empty string
        if date_range == '':
            continue

        # Get the weather outlook if the date_range is not empty string
        weather_outlook_tag = list_of_all_table_data_tags[1]
        weather_outlook = str(weather_outlook_tag.text).strip()
        weather_outlooks.append(weather_outlook)

    return weather_outlooks

def map_date_ranges_to_weather_outlooks(
        date_ranges: dict[str, str],
        weather_outlooks: list[str]
) -> dict[str, str]:
    '''
    Maps extracted date ranges for their
    corresponding weekly weather outlook
    from the PAGASA-DOST website.

    :param date_ranges: Dictionary of date
        ranges for weekly weather outlook
    :type date_ranges: dict[str, str]

    :param weather_outlooks: List of weather
        outlooks for every date ranges
    :type weather_outlooks:

    :return: Dictionary of weekly weather outlook
        for every date ranges
    :rtype: dict[str, str]
    '''
    result = date_ranges

    list_of_all_date_ranges = list(date_ranges.keys())

    # Loop through the list of date ranges to map it to the extracted date ranges
    for index, date_range in enumerate(list_of_all_date_ranges):
        # Use the index of date range to get the corresponding weather outlook
        weather_outlook = weather_outlooks[index]
        # Map date range to the selected weather outlook
        result[date_range] = weather_outlook

    return result