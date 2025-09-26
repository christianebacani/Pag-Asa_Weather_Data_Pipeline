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
    
    # Scrape weather outlook for selected ph cities issued datetime
    validity = list_of_row_tags[0].find('div', attrs={'class': 'validity'})
    list_of_bold_tags = validity.find_all('b')

    if list_of_bold_tags == []:
        issued_datetime = ''
        time_of_validity = ''

    else:
        issued_datetime = str(list_of_bold_tags[0].text)
        issued_datetime = ' '.join(issued_datetime.split())