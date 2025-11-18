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
        div_tag_with_panel_heading_class = selected_ph_city_tag.find('div', attrs={'class': 'panel-heading panel-pagasa-heading panel-pagasa-list panel-pagasa'})
        print(div_tag_with_panel_heading_class)
        print()