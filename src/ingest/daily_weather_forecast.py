'''
    Daily Weather Forecast Module
'''
import requests
from bs4 import BeautifulSoup

def init_soup_object(url: str) -> BeautifulSoup | None:
    '''
        Function to initialize Beautiful 
        Soup Object from the requested data
        from the website 
        (https://www.pagasa.dost.gov.ph/weather#daily-weather-forecast).
    '''
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_issued_datetime(soup: BeautifulSoup) -> str:
    '''
        Function to get issued datetime
        from the daily weather forecast.
    '''
    issued_datetime = ''

    issued_datetime_tag = soup.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    bold_tag = issued_datetime_tag.find('b')

    if bold_tag is not None:
        issued_datetime = str(bold_tag.text).strip()
    
    return issued_datetime

def get_synopsis(soup: BeautifulSoup) -> str:
    '''
        Function to get the synopsis from
        the daily weather forecast.
    '''
    synopsis = ''

    synopsis_tag = soup.find('div', attrs={'class': 'col-md-12 col-lg-12'})
    div_tag_with_panel_class = synopsis_tag.find('div', attrs={'class': 'panel'})
    div_tag_with_panel_body_class = div_tag_with_panel_class.find('div', attrs={'class': 'panel-body'})

    if div_tag_with_panel_body_class is not None:
        paragraph_tag = div_tag_with_panel_body_class.find('p')
        synopsis = str(paragraph_tag.text).strip()
    
    return synopsis

def get_forecast_weather_conditions(soup: BeautifulSoup) -> dict:
    '''
        Function to get the forecast weather conditions
        from the daily weather forecast.
    '''
    forecast_weather_conditions = {
        'place': [],
        'weather_condition': [],
        'caused_by': [],
        'impacts': []
    }

    forecast_weather_conditions_tag = soup.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[1]
    table_tag = forecast_weather_conditions_tag.find('table', attrs={'class': 'table table-striped'})

    if table_tag is not None:
        tbody_tag = table_tag.find('tbody')
        list_of_all_table_row_tags = tbody_tag.find_all('tr')

        for table_row_tag in list_of_all_table_row_tags:
            list_of_all_table_data_tags = table_row_tag.find_all('td', attrs={'class': 'text-center'})
            
            place = str(list_of_all_table_data_tags[0].text).strip()
            forecast_weather_conditions['place'].append(place)

            weather_condition = str(list_of_all_table_data_tags[1].text).strip()
            forecast_weather_conditions['weather_condition'].append(weather_condition)

            caused_by = str(list_of_all_table_data_tags[2].text).strip()
            forecast_weather_conditions['caused_by'].append(caused_by)

            impacts = str(list_of_all_table_data_tags[3].text).strip()
            forecast_weather_conditions['impacts'].append(impacts)
    
    return forecast_weather_conditions

def get_forecast_wind_and_coastal_water_conditions(soup: BeautifulSoup) -> dict:
    '''
        Function to get the forecast wind and coastal water conditions
        from the daily weather forecast.
    '''
    forecast_wind_and_coastal_water_conditions = {
        'place': [],
        'speed': [],
        'direction': [],
        'coastal_water': []
    }

    forecast_wind_and_coastal_water_conditions_tag = soup.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[2]
    table_tag = forecast_wind_and_coastal_water_conditions_tag.find('table', attrs={'class': 'table table-striped'})

    if table_tag is not None:
        tbody_tag = table_tag.find('tbody')
        list_of_all_table_row_tags = tbody_tag.find_all('tr')

        for table_row_tag in list_of_all_table_row_tags:
            list_of_all_table_data_tags = table_row_tag.find_all('td', attrs={'class': 'text-center'})

            place = str(list_of_all_table_data_tags[0].text).strip()
            forecast_wind_and_coastal_water_conditions['place'].append(place)

            speed = str(list_of_all_table_data_tags[1].text).strip()
            forecast_wind_and_coastal_water_conditions['speed'].append(speed)

            direction = str(list_of_all_table_data_tags[2].text).strip()
            forecast_wind_and_coastal_water_conditions['direction'].append(direction)

            coastal_water = str(list_of_all_table_data_tags[3].text).strip()
            forecast_wind_and_coastal_water_conditions['coastal_water'].append(coastal_water)
    
    return forecast_wind_and_coastal_water_conditions

def get_temperature_and_relative_humidity(soup: BeautifulSoup) -> dict:
    '''
        Function to get the temperature and relative humidity from
        the daily weather forecast.
    '''