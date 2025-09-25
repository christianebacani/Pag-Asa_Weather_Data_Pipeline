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
        return

    # Parse response to a Beautiful Soup object
    soup = BeautifulSoup(response.text, 'html.parser')
    row_weather_page = soup.find('div', attrs={'class': 'row weather-page'})
    list_of_row_tags = row_weather_page.find_all('div', attrs={'class': 'row'})

    # Scrape daily weather forececast issued datetime
    issue_tag = list_of_row_tags[0].find('div', attrs={'class': 'col-md-12 col-lg-12 issue'})
    issued_datetime = str(issue_tag.find('b').text)

    if issued_datetime is None:
        issued_datetime = []

    # Scrape synopsis
    synopsis = list_of_row_tags[0].find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[0]
    synopsis = str(synopsis.find('p').text)
    
    if synopsis is None:
        synopsis = ''