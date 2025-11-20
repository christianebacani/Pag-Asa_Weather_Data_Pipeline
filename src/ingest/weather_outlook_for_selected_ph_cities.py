'''
    Weather Outlook for Selected PH Cities Module
'''
import requests
from bs4 import BeautifulSoup

def get_ph_city_weather_outlook_soup(url: str) -> BeautifulSoup | None:
    '''
        Function to get the parsed beautiful soup object to extract
        weather outlook for selected ph cities from pag-asa dost website.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser') # Parse to a Beautiful Soup Object
    return soup

def get_ph_city_weather_outlook_issued_datetime(soup: BeautifulSoup) -> str:
    '''
        Function to get the the issued datetime of weather outlook for
        selected ph cities from pag-asa dost website.
    '''
    issued_datetime = ''

    # Fetch the necessary HTML tags using find() method
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    div_tag_with_row_class = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'row'})

    issued_datetime_and_valid_period_tag = div_tag_with_row_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    if div_tag_with_validity_class is not None: # Validate the div_tag_with_validity_class if it's existing
        bold_tag = div_tag_with_validity_class.find_all('b')[0]
        issued_datetime = str(bold_tag.text).strip()
        issued_datetime = ' '.join(issued_datetime.split())

    return issued_datetime

def get_ph_city_weather_outlook_valid_period(soup: BeautifulSoup) -> str:
    '''
        Function to get the the valid period of weather outlook for
        selected ph cities from pag-asa dost website.
    '''
    valid_period = ''
    
    # Fetch the necessary HTML tags using find() method
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    div_tag_with_row_class = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'row'})

    issued_datetime_and_valid_period_tag = div_tag_with_row_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    if div_tag_with_validity_class is not None: # Validate the div_tag_with_validity_class if it's existing
        bold_tag = div_tag_with_validity_class.find_all('b')[1]
        valid_period = str(bold_tag.text).strip()

    return valid_period

def get_selected_ph_cities(soup: BeautifulSoup) -> dict[str, dict]:
    '''
        Function to get the name of the selected ph cities for their 
        weather outlook from pag-asa dost website.
    '''
    result = {}
    
    # Fetch the necessary HTML tags using find() method
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    div_tag_with_row_class = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'row'})

    selected_ph_cities_weather_outlook_tag = div_tag_with_row_class.find('div', attrs={'class': 'col-md-12 col-lg-12'})
    div_tag_with_panel_group_class = selected_ph_cities_weather_outlook_tag.find('div', attrs={'class': 'panel-group'})

    if div_tag_with_panel_group_class is None: # Validate the div_tag_with_panel_group_class if it's missing
        return result

    list_of_div_tag_with_panel_default_classes = div_tag_with_panel_group_class.find_all('div', attrs={'class': 'panel panel-default panel-pagasa'})

    # Using for-loop to iterate for every div_tag_with_panel_default_classes to fetch the name of the selected ph cities
    for div_tag_with_panel_default_class in list_of_div_tag_with_panel_default_classes:
        anchor_tag = div_tag_with_panel_default_class.find('a', attrs={'data-toggle': 'collapse'})
        ph_city = str(anchor_tag.text).strip()
        result[ph_city] = {}

    return result

def map_weather_dates_to_ph_cities(soup: BeautifulSoup, selected_ph_cities: dict[str, dict]) -> dict[str, dict]:
    '''
        Function to map weather dates to the selected ph cities for their weather outlook
        from pag-asa dost website.
    '''
    result = selected_ph_cities

    # Fetch the necessary HTML tags using find() method
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    div_tag_with_row_class = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'row'})

    selected_ph_cities_weather_outlook_tag = div_tag_with_row_class.find('div', attrs={'class': 'col-md-12 col-lg-12'})
    div_tag_with_panel_group_class = selected_ph_cities_weather_outlook_tag.find('div', attrs={'class': 'panel-group'})
    
    if div_tag_with_panel_group_class is None: # Validate the div_tag_with_panel_group_class if it's missing
        return result

    list_of_div_tag_with_panel_default_classes = div_tag_with_panel_group_class.find_all('div', attrs={'class': 'panel panel-default panel-pagasa'})

    # Using for-loop to iterate for every div_tag_with_panel_default_classes to fetch the necessary data
    for div_tag_with_panel_default_class in list_of_div_tag_with_panel_default_classes:
        anchor_tag = div_tag_with_panel_default_class.find('a', attrs={'data-toggle': 'collapse'})
        ph_city = str(anchor_tag.text).strip()

        table_tag = div_tag_with_panel_default_class.find('table', attrs={'class': 'table'})
        thead_tag = table_tag.find('thead', attrs={'class': 'desktop-view-thead'})
        list_of_all_table_head_tags = thead_tag.find_all('th', attrs={'class': 'text-center'})
        
        weather_dates = []

        # Using for-loop to iterate for every table_head_tags to fetch the weather dates
        for table_head_tag in list_of_all_table_head_tags:
            weather_date = str(table_head_tag.text).strip()
            weather_date = ' '.join(weather_date.split())
            weather_dates.append(weather_date)
        
        result[ph_city]['weather_dates'] = weather_dates
    
    return result

def map_temperature_ranges_to_ph_cities(soup: BeautifulSoup, ph_cities_with_weather_dates: dict[str, dict]) -> dict[str, dict]:
    '''
        Function to map temperature ranges to the selected ph cities for their weather outlook
        from pag-asa dost website.
    '''
    result = ph_cities_with_weather_dates

    # Fetch the necessary HTML tags using find() method
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    div_tag_with_row_class = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'row'})

    selected_ph_cities_weather_outlook_tag = div_tag_with_row_class.find('div', attrs={'class': 'col-md-12 col-lg-12'})
    div_tag_with_panel_group_class = selected_ph_cities_weather_outlook_tag.find('div', attrs={'class': 'panel-group'})
    
    if div_tag_with_panel_group_class is None: # Validate the div_tag_with_panel_group_class if it's missing
        return result

    list_of_div_tag_with_panel_default_classes = div_tag_with_panel_group_class.find_all('div', attrs={'class': 'panel panel-default panel-pagasa'})

    # Using for-loop to iterate for every div_tag_with_panel_default_classes to fetch the necessary data
    for div_tag_with_panel_default_class in list_of_div_tag_with_panel_default_classes:
        anchor_tag = div_tag_with_panel_default_class.find('a', attrs={'data-toggle': 'collapse'})
        ph_city = str(anchor_tag.text).strip()
        
        table_tag = div_tag_with_panel_default_class.find('table', attrs={'class': 'table'})
        tbody_tag = table_tag.find('tbody')
        table_row_tag_with_desktop_view_class = tbody_tag.find('tr', attrs={'class': 'desktop-view-tr'})
        list_of_all_table_data_tags = table_row_tag_with_desktop_view_class.find_all('td')
        
        temperature_ranges = []

        # Using for-loop to iterate for every div_tag_with_panel_default_classes to fetch the temperature ranges for every weather date
        for table_data_tag in list_of_all_table_data_tags:
            minimum_temperature_tag = table_data_tag.find('span', attrs={'class': 'min'})
            minimum_temperature = str(minimum_temperature_tag.text).strip()

            maximum_temperature_tag = table_data_tag.find('span', attrs={'class': 'max'})
            maximum_temperature = str(maximum_temperature_tag.text).strip()

            temperature_ranges.append([minimum_temperature, maximum_temperature])
        
        result[ph_city]['temperature_ranges'][temperature_ranges]
    
    return result