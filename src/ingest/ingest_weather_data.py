'''
    Data Ingestion for Weather Data
'''
import requests
from bs4 import BeautifulSoup

def scrape_daily_weather_forecast_data(url: str) -> dict:
    '''
        Scrape function to perform web-scraping
        to ingest daily weather forecast data from
        the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')        
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object

def scrape_weather_outlook_for_selected_ph_cities_data(url: str) -> dict:
    '''
        Scrape function to perform web-scraping
        to ingest weather oulook for selected ph
        cities data from the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_row_tags = div_tag_with_row_weather_page_class.find_all('div', attrs={'class': 'row'})

    # Scrape weather outlook for selected ph cities issued datetime and time of validity
    div_tag_with_validity_class = list_of_all_row_tags[0].find('div', attrs={'class': 'validity'})
    list_of_all_bold_tags = div_tag_with_validity_class.find_all('b')

    if len(list_of_all_bold_tags) != 2:
        issued_datetime = 'None'
        time_of_validity = 'None'

    else:
        issued_datetime = str(list_of_all_bold_tags[0].text)
        issued_datetime = ' '.join(issued_datetime.split())
        time_of_validity = str(list_of_all_bold_tags[1].text)
    
    # Scrape weather outlook for selected ph cities
    div_tag_with_panel_group_class = list_of_all_row_tags[0].find('div', attrs={'class': 'panel-group', 'id': 'outlook-phil-cities'})
    ph_cities = div_tag_with_panel_group_class.find_all('div', attrs={'class': 'panel panel-default panel-pagasa'})

    result = {}
    result['issued_datetime'] = issued_datetime
    result['time_of_validity'] = time_of_validity
 
    for ph_city in ph_cities:
        # Scrape city name
        city = str(ph_city.find('div', attrs={'class': 'panel-title'}).text)
        city = ' '.join(city.split())

        if city == '':
            continue

        table_tag = ph_city.find('table', attrs={'class': 'table'})

        # Scrape weather outlook dates
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
            # Scrape weather outlook temperatures
            temperatures = str(table_data_tag.find('div', attrs={'class': 'weather-values'}).text)
            temperatures = temperatures.split()

            if temperatures == []:
                continue

            weather_outlook_temperatures.append(temperatures)

            # Scrape weather outlook chances of rain
            chances_of_rain = str(table_data_tag.find('span', attrs={'style': 'font-weight:bold; color: rgb(9, 73, 156);'}).text)
            
            if chances_of_rain == '':
                continue

            weather_outlook_chances_of_rain.append(chances_of_rain)
        
        # Store all the scraped weather outlook for selected ph cities data to a dictionary for better readability instead of using separate arrays
        result[city] = {}
        result[city]['weather_outlook_dates'] = weather_outlook_dates
        result[city]['weather_outlook_temperatures'] = weather_outlook_temperatures
        result[city]['weather_outlook_chances_of_rain'] = weather_outlook_chances_of_rain

    return result

def scrape_asian_cities_weather_forecast_data(url: str) -> dict:
    '''
        Scrape function to perform web-scraping
        to ingest asian cities weather forecast data
        from the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')        
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_row_tags = div_tag_with_row_weather_page_class.find_all('div', attrs={'class': 'row'})

    # Scrape asian cities weather forecast issued datetime and time of validity
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
      
        # Scrape city name
        place = str(list_of_all_table_data_tags[0].text)

        if place == '':
            continue

        # Scrape weather description        
        description = str(list_of_all_table_data_tags[2].text)
        description = ' '.join(description.split())

        if description == '':
            description = 'None'

        # Scrape minimum temperature
        minimum_temperature = str(list_of_all_table_data_tags[3].text)
        
        if minimum_temperature == '':
            minimum_temperature = 'None'

        # Scrape maximum temperature
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
        Scrape function to perform web-scraping
        to ingest weather outlook for selected tourist
        areas data from the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_row_tags = div_tag_with_row_weather_page_class.find_all('div', attrs={'class': 'row'})

    # Scrape weather outlook for selected tourist areas issued datetime and time of validity
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

    # Scrape weather outlook dates
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

        # Scrape tourist destination name
        tourist_destination = str(list_of_all_table_data_tags[0].text)
        tourist_destination = ' '.join(tourist_destination.split())
        
        if tourist_destination == '':
            continue

        result[tourist_destination] = {}

        # Scrape minimum and maximum temperatures in different dates
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
        Scrape function to perform web-scraping
        to ingest weekly weather outlook data
        from the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
    '''
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_weather_page_class = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_all_row_tags = div_tag_with_row_weather_page_class.find_all('div', attrs={'class': 'row'})

    # Scrape weekly weather outlook issued datetime and datetime of validity
    div_tag_with_validity_class = list_of_all_row_tags[0].find('div', attrs={'class': 'validity'})
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

    table_tag = list_of_all_row_tags[0].find('table', attrs={'class': 'table'})
    tbody_tag = table_tag.find('tbody')
    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    for table_row_tag in list_of_all_table_row_tags:
        list_of_all_table_data_tags = table_row_tag.find_all('td')

        if len(list_of_all_table_data_tags) != 2:
            continue

        # Scrape weather outlook date
        weather_outlook_date = str(list_of_all_table_data_tags[0].text)
        weather_outlook_date = ' '.join(weather_outlook_date.split())
        
        if weather_outlook_date == '':
            continue

        # Scrape weather outlook description
        weather_outlook_description = str(list_of_all_table_data_tags[1].text)
        weather_outlook_description = ' '.join(weather_outlook_description.split())

        if weather_outlook_description == '':
            weather_outlook_description = 'None'

        result[weather_outlook_date] = weather_outlook_description
    
    return result

def scrape_weather_advisory_data(url: str) -> dict:
    '''
        Scrape function to perform web-scraping
        to ingest weather advisory data in PDF format
        from the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_marine_class = soup.find('div', attrs={'class': 'row marine'})
    div_tag_with_article_content_weather_advisory_class = div_tag_with_row_marine_class.find('div', attrs={'class': 'col-md-12 article-content weather-advisory'})

    # TODO: Implement the functionality here to ingest the PDF data of the weather advisory in PDF Format
    # NOTE: Curently we can't implement it because there's no currently no weather advisory data from the website
    return {}

def scrape_daily_temperature_data(url: str) -> dict:
    '''
        Scrape function to perform web-scraping
        to ingest daily temperature data from the 
        Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
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
    
    # Scrape top 10 lowest temperature heading
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

        # Scrape station name for top 10 lowest temperature
        station_name = str(list_of_all_table_data_tags[0].text)
        station_name = ' '.join(station_name.split())

        if station_name == '':
            continue

        # Scrape temperature for top 10 lowest temperature
        temperature = str(list_of_all_table_data_tags[1].text)
        temperature = ' '.join(temperature.split())

        if temperature == '':
            temperature = 'None'

        result[top_10_lowest_temperature_heading][station_name] = temperature
    
    div_tag_with_panel_class = list_of_all_column_tags[1].find('div', attrs={'class': 'panel'})

    # Scrape top 10 highest temperature heading
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

        # Scrape station name for top 10 highest temperature
        station_name = str(list_of_all_table_data_tags[0].text)
        station_name = ' '.join(station_name.split())
        
        if station_name == '':
            continue

        # Scrape temperature for top 10 highest temperature
        temperature = str(list_of_all_table_data_tags[1].text)
        temperature = ' '.join(temperature.split())

        if temperature == '':
            temperature = 'None'

        result[top_10_highest_temperature_heading][station_name] = temperature

    return result