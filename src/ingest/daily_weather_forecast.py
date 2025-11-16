'''
    Daily Weather Forecast Module
'''
import requests
from bs4 import BeautifulSoup

def get_daily_weather_forecast_soup(url: str) -> BeautifulSoup | None:
    '''
        Function to get the parsed beautiful soup object
        from the web-page that contains daily weather forecast
        of pag-asa dost website.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser') # Parse to a Beautiful Soup Object
    return soup

def get_daily_forecast_issued_datetime(soup: BeautifulSoup) -> str:
    '''
        Function to get issued datetime from web-page that contains
        daily weather forecast of pag-asa dost website.
    '''
    issued_datetime = ''

    # Fetch the necessary HTML tags using find() method
    issued_datetime_tag = soup.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    bold_tag = issued_datetime_tag.find('b')

    if bold_tag is not None: # Validate the bold_tag if it's existing
        issued_datetime = str(bold_tag.text).strip()
    
    return issued_datetime

def get_synopsis(soup: BeautifulSoup) -> str:
    '''
        Function to get synopsis from web-page
        that contains daily weather forecast of
        pag-asa dost website.
    '''
    synopsis = ''

    # Fetch the necessary HTML tags using find() method
    synopsis_tag = soup.find('div', attrs={'class': 'col-md-12 col-lg-12'})
    div_tag_with_panel_class = synopsis_tag.find('div', attrs={'class': 'panel'})
    div_tag_with_panel_body_class = div_tag_with_panel_class.find('div', attrs={'class': 'panel-body'})

    if div_tag_with_panel_body_class is not None: # Validate the div_tag_with_panel_body_class if it's existing
        paragraph_tag = div_tag_with_panel_body_class.find('p')
        synopsis = str(paragraph_tag.text).strip()
    
    return synopsis

def get_forecast_weather_conditions(soup: BeautifulSoup) -> dict:
    '''
        Function to get forecast weather conditions from web-page
        that contains daily weather forecast of pag-asa dost website.
    '''
    forecast_weather_conditions = {
        'place': [],
        'weather_condition': [],
        'caused_by': [],
        'impacts': []
    }

    # Fetch the necessary HTML tags using find() method
    forecast_weather_conditions_tag = soup.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[1]
    table_tag = forecast_weather_conditions_tag.find('table', attrs={'class': 'table table-striped'})

    if table_tag is not None: # Validate the table_tag if it's existing
        tbody_tag = table_tag.find('tbody')
        list_of_all_table_row_tags = tbody_tag.find_all('tr')

        # Using for-loop to iterate for every table_row_tag to fetch the necessary data
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
        Function to get forecast wind and coastal water conditions from web-page
        that contains daily weather forecast of pag-asa dost website.
    '''
    forecast_wind_and_coastal_water_conditions = {
        'place': [],
        'speed': [],
        'direction': [],
        'coastal_water': []
    }

    # Fetch the necessary HTML tags using find() method
    forecast_wind_and_coastal_water_conditions_tag = soup.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[2]
    table_tag = forecast_wind_and_coastal_water_conditions_tag.find('table', attrs={'class': 'table table-striped'})

    if table_tag is not None: # Validate the table_tag if it's existing
        tbody_tag = table_tag.find('tbody')
        list_of_all_table_row_tags = tbody_tag.find_all('tr')

        # Using for-loop to iterate for every table_row_tag to fetch the necessary data
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
        Function to get temperature and relative humidity from the
        web-page that contains daily weather forecast of pag-asa
        dost website.
    '''
    temperature_and_relative_humidity = {
        'maximum_temperature': [],
        'time_of_maximum_temperature': [],
        'minimum_temperature': [],
        'time_of_minimum_temperature': [],
        'maximum_relative_humidity_percentage': [],
        'time_of_maximum_relative_humidity_percentage': [],
        'minimum_relative_humidity_percentage': [],
        'time_of_minimum_relative_humidity_percentage': []
    }

    # Fetch the necessary HTML tags using find() method
    temperature_and_relative_humidity_tag = soup.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[3]
    table_tag = temperature_and_relative_humidity_tag.find('table', attrs={'class': 'table'})

    if table_tag is not None: # Validate the table_tag if it's existing
        tbody_tag = table_tag.find('tbody')
        list_of_all_table_row_tags = tbody_tag.find_all('tr')

        # Using index to fetch all the necessary table_row_tag to get all the instances of it's table_data_tag
        temperature_tag = list_of_all_table_row_tags[0]
        relative_humidity_percentage_tag = list_of_all_table_row_tags[1]

        list_of_all_table_data_tags_for_temperature = temperature_tag.find_all('td', attrs={'class', 'text-center'})[1:]
        list_of_all_table_data_tags_for_relative_humidity_percentage = relative_humidity_percentage_tag.find_all('td', attrs={'class': 'text-center'})[1:]

        maximum_temperature = str(list_of_all_table_data_tags_for_temperature[0].text).strip()
        maximum_relative_humidity_percentage = str(list_of_all_table_data_tags_for_relative_humidity_percentage[0].text).strip()
        temperature_and_relative_humidity['maximum_temperature'].append(maximum_temperature)
        temperature_and_relative_humidity['maximum_relative_humidity_percentage'].append(maximum_relative_humidity_percentage)

        time_of_maximum_temperature = str(list_of_all_table_data_tags_for_temperature[1].text).strip()
        time_of_maximum_relative_humidity_percentage = str(list_of_all_table_data_tags_for_relative_humidity_percentage[1].text).strip()
        temperature_and_relative_humidity['time_of_maximum_temperature'].append(time_of_maximum_temperature)
        temperature_and_relative_humidity['time_of_maximum_relative_humidity_percentage'].append(time_of_maximum_relative_humidity_percentage)

        minimum_temperature = str(list_of_all_table_data_tags_for_temperature[2].text).strip()
        minimum_relative_humidity_percentage = str(list_of_all_table_data_tags_for_relative_humidity_percentage[2].text).strip()
        temperature_and_relative_humidity['minimum_temperature'].append(minimum_temperature)
        temperature_and_relative_humidity['minimum_relative_humidity_percentage'].append(minimum_relative_humidity_percentage)

        time_of_minimum_temperature = str(list_of_all_table_data_tags_for_temperature[3].text).strip()
        time_of_minimum_relative_humidity_percentage = str(list_of_all_table_data_tags_for_relative_humidity_percentage[3].text).strip()
        temperature_and_relative_humidity['time_of_minimum_temperature'].append(time_of_minimum_temperature)
        temperature_and_relative_humidity['time_of_minimum_relative_humidity_percentage'].append(time_of_minimum_relative_humidity_percentage)
    
    return temperature_and_relative_humidity