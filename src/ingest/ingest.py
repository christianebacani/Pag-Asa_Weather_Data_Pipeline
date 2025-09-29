'''
    Data Ingestion
'''
import requests
from bs4 import BeautifulSoup

def scrape_daily_weather_forecast_data(url: str) -> None | dict:
    '''
        Scrape function to perform web-scraping
        to ingest daily weather forecast data from
        the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return None

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    row_weather_page = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_row_tags = row_weather_page.find_all('div', attrs={'class': 'row'})

    # Scrape daily weather forececast issued datetime
    issue_tag = list_of_row_tags[0].find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    issued_datetime = str(issue_tag.find('b').text)

    if issued_datetime is None:
        issued_datetime = ''

    # Scrape synopsis
    synopsis = list_of_row_tags[0].find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[0]
    synopsis = str(synopsis.find('p').text)

    if synopsis is None:
        synopsis = ''

    # Scrape forecast weather conditions    
    forecast_weather_conditions = list_of_row_tags[0].find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[1]
    table = forecast_weather_conditions.find('table', attrs={'class': 'table table-striped'})
    tbody = table.find('tbody')
    table_row = tbody.find_all('tr')

    forecast_weather_conditions_data = []
    
    for tr in table_row:
        table_data = tr.find_all('td')
        data = []

        for td in table_data:
            data.append(str(td.text))
        
        forecast_weather_conditions_data.append(data)

    # Scrape forecast wind and coastal weather conditions    
    forecast_wind_and_coastal_weather_conditions = list_of_row_tags[0].find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[2]
    table = forecast_wind_and_coastal_weather_conditions.find('table', attrs={'class': 'table table-striped'})
    tbody = table.find('tbody')
    table_row = tbody.find_all('tr')
    
    forecast_wind_and_coastal_weather_conditions_data = []

    for tr in table_row:
        table_data = tr.find_all('td')
        data = []

        for td in table_data:
            data.append(str(td.text))
        
        forecast_wind_and_coastal_weather_conditions_data.append(data)
    
    # Scrape temperature and relative humidity
    inner_row_tag = list_of_row_tags[0].find('div', attrs={'class': 'row', 'style': 'margin-left: 0; margin-right: 0;'})
    temperature_and_relative_humidity = inner_row_tag.find('div', attrs={'class': 'col-md-12 col-lg-12'})

    span_tags = temperature_and_relative_humidity.find_all('span')
    
    temperature_and_relative_humidity_description = []

    for span_tag in span_tags:
        temperature_and_relative_humidity_description.append(str(span_tag.text))

    temperature_and_relative_humidity_description = ' '.join(temperature_and_relative_humidity_description)

    table = temperature_and_relative_humidity.find('table', attrs={'class': 'table'})
    tbody = table.find('tbody')
    table_row = tbody.find_all('tr')

    temperature_and_relative_humidity_data = []

    for tr in table_row:
        table_data = tr.find_all('td')
        data = []

        for td in table_data:
            data.append(str(td.text))
        
        temperature_and_relative_humidity_data.append(data)

    # Store all the scraped daily weather forecast data to a dictionary for better readability instead of using separate arrays    
    result = {}
    result['issued_datetime'] = issued_datetime
    result['synopsis'] = synopsis
    result['forecast_weather_conditions'] = forecast_weather_conditions_data
    result['forecast_wind_and_coastal_water_conditions'] = forecast_wind_and_coastal_weather_conditions_data
    result['temperature_and_relative_humidity_description'] = temperature_and_relative_humidity_description
    result['temperature_and_relative_humidity'] = temperature_and_relative_humidity_data

    return result

def scrape_weather_outlook_for_selected_ph_cities_data(url: str) -> None | dict:
    '''
        Scrape function to perform web-scraping
        to ingest weather oulook for selected ph
        cities from the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return None

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    row_weather_page = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_row_tags = row_weather_page.find_all('div', attrs={'class': 'row'})
    
    # Scrape weather outlook for selected ph cities issued datetime and time of validity
    validity = list_of_row_tags[0].find('div', attrs={'class': 'validity'})
    list_of_bold_tags = validity.find_all('b')

    if list_of_bold_tags == []:
        issued_datetime = ''
        time_of_validity = ''

    else:
        issued_datetime = str(list_of_bold_tags[0].text)
        issued_datetime = ' '.join(issued_datetime.split())
        time_of_validity = str(list_of_bold_tags[1].text)
    
    # Scrape weather outlook for selected ph cities
    outlook_ph_cities = list_of_row_tags[0].find('div', attrs={'class': 'panel-group', 'id': 'outlook-phil-cities'})
    ph_cities = outlook_ph_cities.find_all('div', attrs={'class': 'panel panel-default panel-pagasa'})

    result = {}
    result['issued_datetime'] = issued_datetime
    result['time_of_validity'] = time_of_validity
 
    for ph_city in ph_cities:
        # Scrape city name
        city = str(ph_city.find('div', attrs={'class': 'panel-title'}).text)
        city = ' '.join(city.split())

        table = ph_city.find('table', attrs={'class': 'table'})

        # Scrape weather outlook dates
        thead = table.find('thead', attrs={'class': 'desktop-view-thead'})
        table_headers = thead.find_all('th', attrs={'class': 'text-center'})

        weather_outlook_dates = []

        for table_header in table_headers:
            table_header = str(table_header.text)
            table_header = ' '.join(table_header.split())
            weather_outlook_dates.append(table_header)

        tbody = table.find('tbody')
        desktop_view_table_row = tbody.find('tr', attrs={'class': 'desktop-view-tr'})
        table_datas = desktop_view_table_row.find_all('td')

        weather_outlook_temperatures = []
        weather_outlook_chances_of_rain = []

        for table_data in table_datas:
            # Scrape weather outlook temperatures
            temperatures = str(table_data.find('div', attrs={'class': 'weather-values'}).text)
            temperatures = temperatures.split()
            weather_outlook_temperatures.append(temperatures)

            # Scrape weather outlook chances of rain
            chances_of_rain = str(table_data.find('span', attrs={'style': 'font-weight:bold; color: rgb(9, 73, 156);'}).text)
            weather_outlook_chances_of_rain.append(chances_of_rain)
        
        # Store all the scraped weather outlook for selected ph cities data to a dictionary for better readability instead of using separate arrays
        result[city] = {}
        result[city]['weather_outlook_dates'] = weather_outlook_dates
        result[city]['weather_outlook_temperatures'] = weather_outlook_temperatures
        result[city]['weather_outlook_chances_of_rain'] = weather_outlook_chances_of_rain

    return result

def scrape_asian_cities_weather_forecast_data(url: str) -> None | dict:
    '''
        Scrape function to perform web-scraping
        to ingest asian cities weather forecast
        from the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return None

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    row_weather_page = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_row_tags = row_weather_page.find_all('div', attrs={'class': 'row'})

    # Scrape asian cities weather forecast issued datetime and time of validity
    validity = list_of_row_tags[0].find('div', attrs={'class': 'validity'})
    list_of_bold_tags = validity.find_all('b')

    if list_of_bold_tags == []:
        issued_datetime = ''
        time_of_validity = ''
    
    else:
        issued_datetime = str(list_of_bold_tags[0].text)
        time_of_validity = str(list_of_bold_tags[1].text)
    
    table = list_of_row_tags[0].find('table', attrs={'class': 'table', 'id': 'asian-table'})
    tbody = table.find('tbody')
    table_rows = tbody.find_all('tr')

    result = {}
    result['issued_datetime'] = issued_datetime
    result['time_of_validity'] = time_of_validity

    for table_row in table_rows:
        table_datas = table_row.find_all('td')
        
        # Scrape city name
        place = str(table_datas[0].text)

        if place is None:
            place = ''

        # Scrape weather description        
        description = str(table_datas[2].text)
        description = ' '.join(description.split())

        # Scrape minimum temperature
        minimum_temperature = str(table_datas[3].text)
        
        if minimum_temperature is None:
            minimum_temperature = ''

        # Scrape maximum temperature
        maximum_temperature = str(table_datas[4].text)

        if maximum_temperature is None:
            maximum_temperature = ''

        result[place] = {}
        result[place]['description'] = description
        result[place]['minimum_temperature'] = minimum_temperature
        result[place]['maximum_temperature'] = maximum_temperature

    return result

def scrape_weather_outlook_for_selected_tourist_areas_data(url: str) -> None | dict:
    '''
        Scrape function to perform web-scraping
        to ingest weather outlook for selected tourist
        areas from the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return None

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    row_weather_page = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_row_tags = row_weather_page.find_all('div', attrs={'class': 'row'})

    # Scrape weather outlook for selected tourist areas issued datetime and time of validity
    validity = list_of_row_tags[0].find('div', attrs={'class': 'validity'})
    list_of_bold_tags = validity.find_all('b')

    if list_of_bold_tags == []:
        issued_datetime = ''
        time_of_validity = ''
    
    else:
        issued_datetime = str(list_of_bold_tags[0].text)
        time_of_validity = str(list_of_bold_tags[1].text)
    
    table_desktop = list_of_row_tags[0].find('table', attrs={'class': 'table desktop'})

    # Scrape weather outlook dates
    thead = table_desktop.find('thead')
    table_headers = thead.find_all('th')

    weather_outlook_dates = []

    for table_header in table_headers:
        table_header = str(table_header.text)
        table_header = ' '.join(table_header.split())
        weather_outlook_dates.append(table_header)

    tbody = table_desktop.find('tbody')
    table_rows = tbody.find_all('tr')
    
    result = {}
    result['issued_datetime'] = issued_datetime
    result['time_of_validity'] = time_of_validity

    for table_row in table_rows:
        table_datas = table_row.find_all('td')
        
        # Scrape tourist destination name
        tourist_destination = str(table_datas[0].text)
        tourist_destination = ' '.join(tourist_destination.split())

        # Scrape minimum and maximum temperatures in different dates
        minimum_and_maximum_temperatures = table_datas[1:]