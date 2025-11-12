'''
    Data Ingestion Module to ingest
    Daily Weather Forecast.
'''
import requests
from bs4 import BeautifulSoup

def ingest_daily_weather_forecast_data(url: str) -> dict:
    '''
        Function to ingest daily weather forecast data.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print('The website does not allow to be scraped!')
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    div_tag_with_row_class = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'row'})

    # Get the issued datetime for the daily weather forecast    
    issued_datetime_tag = div_tag_with_row_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    bold_tag = issued_datetime_tag.find('b')

    if bold_tag is None:
        issued_datetime = ''
    
    else:
        issued_datetime = str(bold_tag.text).strip()

    list_of_all_div_tag_with_col_md_twelve_col_lg_twelve_classes = div_tag_with_row_class.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})

    if len(list_of_all_div_tag_with_col_md_twelve_col_lg_twelve_classes) == 4:
        synopsis_tag = list_of_all_div_tag_with_col_md_twelve_col_lg_twelve_classes[0]
        forecast_weather_conditions_tag = list_of_all_div_tag_with_col_md_twelve_col_lg_twelve_classes[1]
        forecast_wind_and_coastal_water_conditions_tag = list_of_all_div_tag_with_col_md_twelve_col_lg_twelve_classes[2]
        temperature_and_relative_humidity_tag = list_of_all_div_tag_with_col_md_twelve_col_lg_twelve_classes[3]
    
    # TODO: Implement functionality here to add else statement if the available div tags is not equals to 4 instances
    
    # Get the synopsis for the daily weather forecast
    div_tag_with_panel_class = synopsis_tag.find('div', attrs={'class': 'panel'})
    
    if div_tag_with_panel_class is None:
        synopsis = ''

    else:
        div_tag_with_panel_body_class = div_tag_with_panel_class.find('div', attrs={'class': 'panel-body'})
        paragraph_tag = div_tag_with_panel_body_class.find('p')
        synopsis = str(paragraph_tag.text).strip()