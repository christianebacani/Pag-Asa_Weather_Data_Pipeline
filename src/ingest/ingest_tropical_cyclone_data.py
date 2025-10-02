'''
    Data Ingestion for Tropical Cyclone Data
'''
import requests
from bs4 import BeautifulSoup

def scrape_tropical_cyclone_bulletin(url: str) -> None | dict:
    '''
        Scrape function to perform web-scraping
        to ingest tropical cyclone bulletin data from
        the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/) 
    '''
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    tropical_cyclone_weather_bulletin_page = soup.find('div', attrs={'class': 'row tropical-cyclone-weather-bulletin-page'})
    print(tropical_cyclone_weather_bulletin_page)