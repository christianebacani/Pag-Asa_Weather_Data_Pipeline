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
    article_content = tropical_cyclone_weather_bulletin_page.find('div', attrs={'col-md-12 article-content'})

    list_of_all_row_tags = article_content.find_all('div', attrs={'class': 'row'})

    # Scrape tropical cyclone name    
    tropical_cyclone_name = str(list_of_all_row_tags[1].text)
    tropical_cyclone_name = ' '.join(tropical_cyclone_name.split())

    if tropical_cyclone_name == '':
        print(f'Currently there\'s no tropical cyclone!')
        return None

    list_of_all_h5_tags = list_of_all_row_tags[2].find_all('h5')

    if len(list_of_all_h5_tags) != 2:
        issued_datetime = 'None'
        validity_description = 'None'

    else:
        # Scrape issued datetime
        issued_datetime = str(list_of_all_h5_tags[0].text)

        # Scrape validity description
        validity_description = str(list_of_all_h5_tags[1].text)