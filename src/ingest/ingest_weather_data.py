'''
    Data Ingestion for Weather Data
'''
import requests
from bs4 import BeautifulSoup

def scrape_daily_weather_forecast_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest daily weather forecast data. The function 
        retrieves the data containing the forecasted daily weather.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')        
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    div_tag_with_row_class = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'row'})

    # Scrape the issued datetime for the daily weather forecast
    div_tag_with_col_md_twelve_col_lg_twelve_issue_class = div_tag_with_row_class.find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    bold_tag =  div_tag_with_col_md_twelve_col_lg_twelve_issue_class.find('b')

    if bold_tag is None:
        issued_datetime = 'None'
    
    else:
        issued_datetime = str(bold_tag.text)

    list_of_div_tag_with_col_md_twelve_col_lg_twelve_classes = div_tag_with_row_class.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})

    if len(list_of_div_tag_with_col_md_twelve_col_lg_twelve_classes) == 4: # Without TC Information, only 4 matching <div> elements exist.
        synopsis = list_of_div_tag_with_col_md_twelve_col_lg_twelve_classes[0]
        forecast_weather_conditions = list_of_div_tag_with_col_md_twelve_col_lg_twelve_classes[1]
        forecast_wind_and_coastal_weather_conditions = list_of_div_tag_with_col_md_twelve_col_lg_twelve_classes[2]
        temperature_and_relative_humidity = list_of_div_tag_with_col_md_twelve_col_lg_twelve_classes[3]
    
    else:
        synopsis = list_of_div_tag_with_col_md_twelve_col_lg_twelve_classes[0]
        tc_information = list_of_div_tag_with_col_md_twelve_col_lg_twelve_classes[1]
        forecast_weather_conditions = list_of_div_tag_with_col_md_twelve_col_lg_twelve_classes[2]
        forecast_wind_and_coastal_weather_conditions = list_of_div_tag_with_col_md_twelve_col_lg_twelve_classes[3]
        temperature_and_relative_humidity = list_of_div_tag_with_col_md_twelve_col_lg_twelve_classes[4]

    # TODO: Add else statement here if the TC Information exist in the website so the matching <div> elements is 5 instead of 4

    # Scrape the synopsis of the daily weather forecast
    paragraph_tag = synopsis.find('p')

    if paragraph_tag is None:
        synopsis = 'None'
    
    else:
        synopsis = str(paragraph_tag.text)

    # Scrape the forecasted weather conditions
    tbody_tag = forecast_weather_conditions.find('tbody')

    if tbody_tag is None:
        forecast_weather_conditions = {
            'place': [],
            'weather_condition': [],
            'caused_by': [],
            'impacts': []
        }

    else:
        list_of_all_table_row_tags = tbody_tag.find_all('tr')

        forecast_weather_conditions = {
            'place': [],
            'weather_condition': [],
            'caused_by': [],
            'impacts': []
        }

        for table_row_tag in list_of_all_table_row_tags:
            list_of_all_table_data_tags = table_row_tag.find_all('td')
            
            # Scrape the place of forecasted weather conditions
            place = str(list_of_all_table_data_tags[0].text)
            forecast_weather_conditions['place'].append(place)

            # Scrape the forecasted weather condition
            weather_condition = str(list_of_all_table_data_tags[1].text)
            forecast_weather_conditions['weather_condition'].append(weather_condition)

            # Scraped the caused of forecasted weather condition
            caused_by = str(list_of_all_table_data_tags[2].text)
            forecast_weather_conditions['caused_by'].append(caused_by)

            # Scrape the impact of forecasted weather condition
            impacts = str(list_of_all_table_data_tags[3].text)
            forecast_weather_conditions['impacts'].append(impacts)

    # Scrape the forecasted wind and coastal water conditions
    tbody_tag = forecast_wind_and_coastal_weather_conditions.find('tbody')
    
    if tbody_tag is None:
        forecast_wind_and_coastal_weather_conditions = {
            'place': [],
            'speed': [],
            'direction': [],
            'coastal_water': []
        }

    else:
        list_of_all_table_row_tags = tbody_tag.find_all('tr')

        forecast_wind_and_coastal_weather_conditions = {
            'place': [],
            'speed': [],
            'direction': [],
            'coastal_water': []
        }
        
        for table_row_tag in list_of_all_table_row_tags:
            list_of_all_table_data_tags = table_row_tag.find_all('td')

            # Scrape the place of forecasted wind and coastal weather condition
            place = str(list_of_all_table_data_tags[0].text)
            forecast_wind_and_coastal_weather_conditions['place'].append(place)

            # Scrape the speed of forecasted wind and coastal weather condition
            speed = str(list_of_all_table_data_tags[1].text)
            forecast_wind_and_coastal_weather_conditions['speed'].append(speed)

            # Scrape the direction of forecasted wind and coastal weather condition
            direction = str(list_of_all_table_data_tags[2].text)
            forecast_wind_and_coastal_weather_conditions['direction'].append(direction)

            # Scrape the coastal water of forecasted wind and coastal weather condition
            coastal_water = str(list_of_all_table_data_tags[3].text)
            forecast_wind_and_coastal_weather_conditions['coastal_water'].append(coastal_water)
    
    # Scrape the forecasted temperature and relative humidity
    table_tag = temperature_and_relative_humidity.find('table', attrs={'class': 'table'})
    tbody_tag = table_tag.find('tbody')

    if tbody_tag is None:
        temperature_and_relative_humidity = {
            'maximum_temperature': 'None',
            'time_of_maximum_temperature': 'None',
            'minimum_temperature': 'None',
            'time_of_minimum_temperature': 'None',
            'maximum_relative_humidity_percentage': 'None',
            'time_of_maximum_relative_humidity_percentage': 'None',
            'minimum_relative_humidity_percentage': 'None',
            'time_of_minimum_relative_humidity_percentage': 'None'
        }
    
    else:
        list_of_all_table_row_tags = tbody_tag.find_all('tr')

        temperature_and_relative_humidity = {
            'maximum_temperature': 'None',
            'time_of_maximum_temperature': 'None',
            'minimum_temperature': 'None',
            'time_of_minimum_temperature': 'None',
            'maximum_relative_humidity_percentage': 'None',
            'time_of_maximum_relative_humidity_percentage': 'None',
            'minimum_relative_humidity_percentage': 'None',
            'time_of_minimum_relative_humidity_percentage': 'None'
        }
        
        list_of_all_table_data_tags = list_of_all_table_row_tags[0].find_all('td')
        list_of_all_table_data_tags = list_of_all_table_data_tags[1:]

        # Scrape the forecasted maximum temperature
        maximum_temperature = str(list_of_all_table_data_tags[0].text)
        temperature_and_relative_humidity['maximum_temperature'] = maximum_temperature

        # Scrape the forecasted time of maximum temperature
        time_of_maximum_temperature = str(list_of_all_table_data_tags[1].text)
        temperature_and_relative_humidity['time_of_maximum_temperature'] = time_of_maximum_temperature

        # Scrape the forecasted minimum temperature
        minimum_temperature = str(list_of_all_table_data_tags[2].text)
        temperature_and_relative_humidity['minimum_temperature'] = minimum_temperature

        # Scrape the forecasted time of minimum temperature
        time_of_minimum_temperature = str(list_of_all_table_data_tags[3].text)
        temperature_and_relative_humidity['time_of_minimum_temperature'] = time_of_minimum_temperature

        list_of_all_table_data_tags = list_of_all_table_row_tags[1].find_all('td')
        list_of_all_table_data_tags = list_of_all_table_data_tags[1:]

        # Scrape the forecasted maximum relative humidity percentage
        maximum_relative_humidity_percentage = str(list_of_all_table_data_tags[0].text)
        temperature_and_relative_humidity['maximum_relative_humidity_percentage'] = maximum_relative_humidity_percentage

        # Scrape the forecasted time of maximum relative humidity percentage
        time_of_maximum_relative_humidity_percentage = str(list_of_all_table_data_tags[1].text)
        temperature_and_relative_humidity['time_of_maximum_relative_humidity_percentage'] = time_of_maximum_relative_humidity_percentage

        # Scrape the forecasted minimum relative humidity percentage
        minimum_relative_humidity_percentage = str(list_of_all_table_data_tags[2].text)
        temperature_and_relative_humidity['minimum_relative_humidity_percentage'] = minimum_relative_humidity_percentage

        # Scrape the forecasted time of minimum relative humidity percentage
        time_of_minimum_relative_humidity_percentage = str(list_of_all_table_data_tags[3].text)
        temperature_and_relative_humidity['time_of_minimum_relative_humidity_percentage'] = time_of_minimum_relative_humidity_percentage
    
    # TODO: Added new data to initialize inside the dictionary 'result' if the TC Information div is present
    result = {}
    result['issued_datetime'] = issued_datetime
    result['synopsis'] = synopsis
    result['forecast_weather_conditions'] = forecast_weather_conditions
    result['forecast_wind_and_coastal_water_conditions'] = forecast_wind_and_coastal_weather_conditions
    result['temperature_and_relative_humidity'] = temperature_and_relative_humidity
    
    return result

def scrape_weather_outlook_for_selected_ph_cities_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest weather outlook for selected philippine cities data. 
        The function retrieves the data containing the weather outlook
        for selected philippine cities.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_row_tags = div_tag_with_row_weather_page_class.find_all('div', attrs={'class': 'row'})

    # Scrape the issued datetime and time of validity for the weather outlook for selected ph cities    
    div_tag_with_validity_class = list_of_all_row_tags[0].find('div', attrs={'class': 'validity'})
    list_of_all_bold_tags = div_tag_with_validity_class.find_all('b')

    if len(list_of_all_bold_tags) != 2:
        issued_datetime = 'None'
        time_of_validity = 'None'

    else:
        issued_datetime = str(list_of_all_bold_tags[0].text)
        issued_datetime = ' '.join(issued_datetime.split())
        time_of_validity = str(list_of_all_bold_tags[1].text)

    # Scrape all the div elements of the selected ph cities
    div_tag_with_panel_group_class = list_of_all_row_tags[0].find('div', attrs={'class': 'panel-group', 'id': 'outlook-phil-cities'})
    ph_cities = div_tag_with_panel_group_class.find_all('div', attrs={'class': 'panel panel-default panel-pagasa'})

    result = {}
    result['issued_datetime'] = issued_datetime
    result['time_of_validity'] = time_of_validity
 
    for ph_city in ph_cities:
        # Scrape the name of the city
        city = str(ph_city.find('div', attrs={'class': 'panel-title'}).text)
        city = ' '.join(city.split())

        if city == '':
            continue

        table_tag = ph_city.find('table', attrs={'class': 'table'})

        # Scrape all of the weather outlook dates
        thead_tag = table_tag.find('thead', attrs={'class': 'desktop-view-thead'})
        list_of_all_table_header_tags = thead_tag.find_all('th', attrs={'class': 'text-center'})

        weather_outlook_dates = []

        for table_header_tag in list_of_all_table_header_tags:
            table_header_tag = str(table_header_tag.text)
            table_header_tag = ' '.join(table_header_tag.split())

            if table_header_tag == '':
                continue

            weather_outlook_dates.append(table_header_tag)

        tbody_tag = table_tag.find('tbody')
        table_row_tag_with_desktop_view_class = tbody_tag.find('tr', attrs={'class': 'desktop-view-tr'})
        list_of_all_table_data_tags = table_row_tag_with_desktop_view_class.find_all('td')

        weather_outlook_temperatures = []
        weather_outlook_chances_of_rain = []

        for table_data_tag in list_of_all_table_data_tags:
            # Scrape the weather outlook temperatures
            temperatures = str(table_data_tag.find('div', attrs={'class': 'weather-values'}).text)
            temperatures = temperatures.split()

            if temperatures == []:
                continue

            weather_outlook_temperatures.append(temperatures)

            # Scrape the chances of rain percentage
            chances_of_rain = str(table_data_tag.find('span', attrs={'style': 'font-weight:bold; color: rgb(9, 73, 156);'}).text)
            
            if chances_of_rain == '':
                continue

            weather_outlook_chances_of_rain.append(chances_of_rain)
        
        # Store all of the data of the weather outlook for selected ph cities to a dictionary for better readability instead of using separate arrays
        result[city] = {}
        result[city]['weather_outlook_dates'] = weather_outlook_dates
        result[city]['weather_outlook_temperatures'] = weather_outlook_temperatures
        result[city]['weather_outlook_chances_of_rain'] = weather_outlook_chances_of_rain

    return result

def scrape_asian_cities_weather_forecast_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest asian cities weather forecast data. The function 
        retrieves the data containing the forecasted asian cities weather.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')        
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_row_tags = div_tag_with_row_weather_page_class.find_all('div', attrs={'class': 'row'})

    # Scrape the issued datetime and time of validity for the forecasted weather of asian cities 
    div_tag_with_validity_class = list_of_all_row_tags[0].find('div', attrs={'class': 'validity'})
    list_of_all_bold_tags = div_tag_with_validity_class.find_all('b')

    if len(list_of_all_bold_tags) != 2:
        issued_datetime = 'None'
        time_of_validity = 'None'
    
    else:
        issued_datetime = str(list_of_all_bold_tags[0].text)
        time_of_validity = str(list_of_all_bold_tags[1].text)
    
    result = {}
    result['issued_datetime'] = issued_datetime
    result['time_of_validity'] = time_of_validity

    table_tag = list_of_all_row_tags[0].find('table', attrs={'class': 'table', 'id': 'asian-table'})
    tbody_tag = table_tag.find('tbody')
    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    for table_row_tag in list_of_all_table_row_tags:
        list_of_all_table_data_tags = table_row_tag.find_all('td')

        if list_of_all_table_data_tags == []:
            continue
      
        # Scrape the name of the city
        place = str(list_of_all_table_data_tags[0].text)

        if place == '':
            continue

        # Scrape the weather description        
        description = str(list_of_all_table_data_tags[2].text)
        description = ' '.join(description.split())

        if description == '':
            description = 'None'

        # Scrape the forecasted minimum temperature
        minimum_temperature = str(list_of_all_table_data_tags[3].text)
        
        if minimum_temperature == '':
            minimum_temperature = 'None'

        # Scrape the forecasted maximum temperature
        maximum_temperature = str(list_of_all_table_data_tags[4].text)

        if maximum_temperature == '':
            maximum_temperature = 'None'

        result[place] = {}
        result[place]['description'] = description
        result[place]['minimum_temperature'] = minimum_temperature
        result[place]['maximum_temperature'] = maximum_temperature

    return result

def scrape_weather_outlook_for_selected_tourist_areas_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest weather outlook for selected tourist areas data. 
        The function retrieves the data containing the weather 
        outlook for selected tourist areas.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_row_tags = div_tag_with_row_weather_page_class.find_all('div', attrs={'class': 'row'})

    # Scrape the issued datetime and time of validity for the forecasted weather outlook for the selected tourist areas
    div_tag_with_validity_class = list_of_all_row_tags[0].find('div', attrs={'class': 'validity'})
    list_of_all_bold_tags = div_tag_with_validity_class.find_all('b')

    if len(list_of_all_bold_tags) != 2:
        issued_datetime = 'None'
        time_of_validity = 'None'
    
    else:
        issued_datetime = str(list_of_all_bold_tags[0].text)
        time_of_validity = str(list_of_all_bold_tags[1].text)
    
    result = {}
    result['issued_datetime'] = issued_datetime
    result['time_of_validity'] = time_of_validity

    table_tag_with_table_desktop_class = list_of_all_row_tags[0].find('table', attrs={'class': 'table desktop'})

    # Scrape all of the weather outlook dates
    thead_tag = table_tag_with_table_desktop_class.find('thead')
    list_of_all_table_header_tags = thead_tag.find_all('th')
    list_of_all_table_header_tags = list_of_all_table_header_tags[1:]

    weather_outlook_dates = []

    for table_header_tag in list_of_all_table_header_tags:
        table_header_tag = str(table_header_tag.text)
        table_header_tag = ' '.join(table_header_tag.split())

        if table_header_tag == '':
            continue

        weather_outlook_dates.append(table_header_tag)

    tbody_tag = table_tag_with_table_desktop_class.find('tbody')
    list_of_all_table_row_tags = tbody_tag.find_all('tr')
    
    for table_row_tag in list_of_all_table_row_tags:
        list_of_all_table_data_tags = table_row_tag.find_all('td')
        
        if list_of_all_table_data_tags == []:
            continue

        # Scrape the name of the tourist destination
        tourist_destination = str(list_of_all_table_data_tags[0].text)
        tourist_destination = ' '.join(tourist_destination.split())
        
        if tourist_destination == '':
            continue

        result[tourist_destination] = {}

        # Scrape all of the different dates of minimum and maximum temperatures
        minimum_and_maximum_temperatures = list_of_all_table_data_tags[1:]

        for index, minimum_and_maximum_temperature in enumerate(minimum_and_maximum_temperatures):
            minimum_and_maximum_temperature = str(minimum_and_maximum_temperature.text)
            temperatures = minimum_and_maximum_temperature.split()

            if weather_outlook_dates == []:
                continue

            date = weather_outlook_dates[index]
            result[tourist_destination][date] = temperatures

    return result

def scrape_weekly_weather_outlook_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest weekly weather outlook data. The function 
        retrieves the data containing the weekly weather outlook.
    '''
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_div_tag_with_row_classes = div_tag_with_row_weather_page_class.find_all('div', attrs={'class': 'row'})

    # Scrape the issued datetime and datetime of validity for weekly weather outlook
    div_tag_with_validity_class = list_of_all_div_tag_with_row_classes[0].find('div', attrs={'class': 'validity'})
    list_of_all_bold_tags = div_tag_with_validity_class.find_all('b')

    if len(list_of_all_bold_tags) != 2:
        issued_datetime = 'None'
        datetime_of_validity = 'None'
    
    else:
        issued_datetime = str(list_of_all_bold_tags[0].text)
        datetime_of_validity = str(list_of_all_bold_tags[1].text)

    result = {}
    result['issued_datetime'] = issued_datetime
    result['datetime_of_validity'] = datetime_of_validity

    table_tag = list_of_all_div_tag_with_row_classes[0].find('table', attrs={'class': 'table'})
    
    if table_tag is None:
        print(f'Currently there\'s no data for the weekly weather outlook!')
        return {}

    tbody_tag = table_tag.find('tbody')
    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    for table_row_tag in list_of_all_table_row_tags:
        list_of_all_table_data_tags = table_row_tag.find_all('td')

        if len(list_of_all_table_data_tags) != 2:
            continue

        # Scrape the weather outlook date
        weather_outlook_date = str(list_of_all_table_data_tags[0].text)
        weather_outlook_date = ' '.join(weather_outlook_date.split())
        
        if weather_outlook_date == '':
            continue
        
        # Scrape the description of weather outlook
        weather_outlook_description = str(list_of_all_table_data_tags[1].text)
        weather_outlook_description = ' '.join(weather_outlook_description.split())

        if weather_outlook_description == '':
            weather_outlook_description = 'None'

        result[weather_outlook_date] = weather_outlook_description
    
    return result

def scrape_weather_advisory_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest weather advisory data. The function 
        retrieves the data containing the weather advisory.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_marine_class = soup.find('div', attrs={'class': 'row marine'})
    div_tag_with_col_md_twelve_article_content_weather_advisory_class = div_tag_with_row_marine_class.find('div', attrs={'class': 'col-md-12 article-content weather-advisory'})
    
    result = {}

    # Scrape the URL of the weather advisory data
    div_tag_with_weekly_content_adv_class = div_tag_with_col_md_twelve_article_content_weather_advisory_class.find('div', attrs={'class': 'weekly-content-adv'})
    iframe_tag = div_tag_with_weekly_content_adv_class.find('iframe')
    
    if iframe_tag is None:
        result['url_of_weather_advisory_data'] = 'None'

    else:
        url = str(iframe_tag['src']).strip()
        result['url_of_weather_advisory_data'] = url

    return result

def scrape_daily_temperature_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest daily temperature data. The function 
        retrieves the data containing the daily temperature.
    '''
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    div_tag_with_article_content_class = div_tag_with_row_weather_page_class.find('div', attrs={'class': 'col-md-12 article-content'})

    list_of_all_column_tags = div_tag_with_article_content_class.find_all('div', attrs={'class': 'col-md-6'})

    div_tag_with_panel_class = list_of_all_column_tags[0].find('div', attrs={'class': 'panel'})

    result = {}
    
    # Scrape the heading of the table that consist of top 10 lowest temperature
    div_tag_with_panel_heading_class = div_tag_with_panel_class.find('div', attrs={'class': 'panel-heading'})
    div_tag_with_panel_heading_class = str(div_tag_with_panel_heading_class.text)

    top_10_lowest_temperature_heading = ' '.join(div_tag_with_panel_heading_class.split())

    if top_10_lowest_temperature_heading == '':    
        print(f'Currently there\'s no data for top 10 lowest temperature')
        return {}

    result[top_10_lowest_temperature_heading] = {}

    div_tag_with_panel_body_class = div_tag_with_panel_class.find('div', attrs={'class': 'panel-body'})
    table_tag = div_tag_with_panel_body_class.find('table', attrs={'class': 'table'})
    tbody_tag = table_tag.find('tbody')
    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    for table_row_tag in list_of_all_table_row_tags:
        list_of_all_table_data_tags = table_row_tag.find_all('td')

        if len(list_of_all_table_data_tags) != 2:
            continue

        # Scrape the station name in the table of top 10 lowest temperature
        station_name = str(list_of_all_table_data_tags[0].text)
        station_name = ' '.join(station_name.split())

        if station_name == '':
            continue
        
        # Scrape the temperature in the table of the top 10 lowest temperature
        temperature = str(list_of_all_table_data_tags[1].text)
        temperature = ' '.join(temperature.split())

        if temperature == '':
            temperature = 'None'

        result[top_10_lowest_temperature_heading][station_name] = temperature
    
    div_tag_with_panel_class = list_of_all_column_tags[1].find('div', attrs={'class': 'panel'})

    # Scrape the heading of the table that consist of the top 10 highest temperature
    div_tag_with_panel_heading_class = div_tag_with_panel_class.find('div', attrs={'class': 'panel-heading'})
    div_tag_with_panel_heading_class = str(div_tag_with_panel_heading_class.text)
    top_10_highest_temperature_heading = ' '.join(div_tag_with_panel_heading_class.split())

    if top_10_highest_temperature_heading == '':
        print(f'Currently there\'s no data for top 10 highest temperature')
        return {}

    result[top_10_highest_temperature_heading] = {}

    div_tag_with_panel_body_class = div_tag_with_panel_class.find('div', attrs={'class': 'panel-body'})
    table_tag = div_tag_with_panel_body_class.find('table', attrs={'class': 'table'})
    tbody_tag = table_tag.find('tbody')
    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    for table_row_tag in list_of_all_table_row_tags:
        list_of_all_table_data_tags = table_row_tag.find_all('td')

        if len(list_of_all_table_data_tags) != 2:
            continue
        
        # Scrape the station name in the table of top 10 highest temperature
        station_name = str(list_of_all_table_data_tags[0].text)
        station_name = ' '.join(station_name.split())
        
        if station_name == '':
            continue
            
        # Scrape the temperature in the table of top 10 highest temperature
        temperature = str(list_of_all_table_data_tags[1].text)
        temperature = ' '.join(temperature.split())

        if temperature == '':
            temperature = 'None'

        result[top_10_highest_temperature_heading][station_name] = temperature

    return result