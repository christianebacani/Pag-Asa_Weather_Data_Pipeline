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

def get_ph_city_outlook_issued_datetime(soup: BeautifulSoup) -> str:
    '''
        Function to get the issued datetime of weather outlook for
        selected ph cities from pag-asa dost website.
    '''
    issued_datetime = ''

    issued_datetime_and_valid_period_tag = soup.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    if div_tag_with_validity_class is not None:
        issued_datetime = div_tag_with_validity_class.find_all('b')[0]
        issued_datetime = str(issued_datetime.text)
        issued_datetime = ' '.join(issued_datetime.split())

    return issued_datetime

def get_ph_city_outlook_valid_period(soup: BeautifulSoup) -> str:
    '''
        Function to get the valid period of weather outlook
        for selected ph cities from pag-asa dost website.
    '''
    valid_period = ''

    issued_datetime_and_valid_period_tag = soup.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    div_tag_with_validity_class = issued_datetime_and_valid_period_tag.find('div', attrs={'class': 'validity'})

    if div_tag_with_validity_class is not None:
        valid_period = div_tag_with_validity_class.find_all('b')[1]
        valid_period = str(valid_period.text).strip()
    
    return valid_period

def get_all_selected_ph_cities(soup: BeautifulSoup) -> dict[str, dict]:
    '''
        Function to get all the names of the selected ph cities
        for their respective weather outlook from pag-asa dost website.
    '''
    result = {}

    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    div_tag_with_row_class = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'row'})
    weather_outlook_for_selected_ph_cities_tag = div_tag_with_row_class.find('div', attrs={'class': 'col-md-12 col-lg-12'})
    div_tag_with_panel_class = weather_outlook_for_selected_ph_cities_tag.find('div', attrs={'class': 'panel'})
    div_tag_with_panel_body_class = div_tag_with_panel_class.find('div', attrs={'class': 'panel-body'})

    if div_tag_with_panel_body_class is None:
        return {}
    
    div_tag_with_panel_group_class = div_tag_with_panel_body_class.find('div', attrs={'class': 'panel-group'})
    list_of_all_selected_ph_cities_tags = div_tag_with_panel_group_class.find_all('div', attrs={'class': 'panel panel-default panel-pagasa'})

    for selected_ph_city_tag in list_of_all_selected_ph_cities_tags:
        anchor_tag = selected_ph_city_tag.find('a', attrs={'data-toggle': 'collapse', 'data-parent': '#outlook-phil-cities'})
        selected_ph_city_name = str(anchor_tag.text).strip()
        result[selected_ph_city_name] = {}

    return result

def map_the_weather_dates_for_ph_cities(soup: BeautifulSoup, selected_ph_cities: dict[str, dict]) -> dict[str, dict[str, list]] | dict[str, dict]:
    '''
        Function to map weather dates for selected ph cities
        to get the weather outlooks from pag-asa dost website.        
    '''
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    div_tag_with_row_class = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'row'})
    weather_outlook_for_selected_ph_cities_tag = div_tag_with_row_class.find('div', attrs={'class': 'col-md-12 col-lg-12'})
    div_tag_with_panel_class = weather_outlook_for_selected_ph_cities_tag.find('div', attrs={'class': 'panel'})
    div_tag_with_panel_body_class = div_tag_with_panel_class.find('div', attrs={'class': 'panel-body'})

    if div_tag_with_panel_body_class is None:
        return selected_ph_cities

    div_tag_with_panel_group_class = div_tag_with_panel_body_class.find('div', attrs={'class': 'panel-group'})
    list_of_all_selected_ph_cities_tags = div_tag_with_panel_group_class.find_all('div', attrs={'class': 'panel panel-default panel-pagasa'})

    for selected_ph_city_tag in list_of_all_selected_ph_cities_tags:
        anchor_tag = selected_ph_city_tag.find('a', attrs={'data-toggle': 'collapse', 'data-parent': '#outlook-phil-cities'})
        selected_ph_city_name = str(anchor_tag.text).strip()
        
        thead_tag = selected_ph_city_tag.find('thead', attrs={'class': 'desktop-view-thead'})
        table_row_tag = thead_tag.find('tr')
        list_of_all_table_head_tags = table_row_tag.find_all('th', attrs={'class': 'text-center'})
        
        weather_dates = []

        for table_head_tag in list_of_all_table_head_tags:
            weather_date = str(table_head_tag.text).strip()
            weather_date = ' '.join(weather_date.split())
            weather_dates.append(weather_date)            

        selected_ph_cities[selected_ph_city_name] = {'weather_dates': weather_dates}
    
    return selected_ph_cities