'''
    Data Ingestion for Flood Data
'''
import requests
from bs4 import BeautifulSoup

def scrape_flood_information_data(url: str) -> None | dict:
    '''
        Scrape function to perform web-scraping
        to ingest flood information data from
        the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)
    '''
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    row_flood_page = soup.find('div', attrs={'class': 'row flood-page'})

    article_content = row_flood_page.find('div', attrs={'class': 'col-md-12 article-content'})
    table = article_content.find('table', attrs={'class': 'table'})
    list_of_tbody_tags = table.find_all('tbody')

    result = {}
    result['basin_hydrological_forecast'] = {}

    major_river_basins_table = list_of_tbody_tags[0]
    table_rows = major_river_basins_table.find_all('tr')

    for table_row in table_rows:
        table_datas = table_row.find_all('td')

        if (table_datas == []) or (len(table_datas) != 2):
            continue

        # Scrape major river basin name for basin hydrological forecast        
        major_river_basin = str(table_datas[0].text)

        # Scrape status for basin hydrological forecast
        status = str(table_datas[1].text)
        status = ' '.join(status.split())

        result['basin_hydrological_forecast'][major_river_basin] = status

    sub_basins_table = list_of_tbody_tags[1]
    table_rows = sub_basins_table.find_all('tr')

    for table_row in table_rows:
        table_datas = table_row.find_all('td')

        if (table_datas == []) or (len(table_datas) != 2):
            continue

        # Scrape sub basin name for basin hydrological forecast
        sub_basin = str(table_datas[0].text)
        
        # Scrape status for basin hydrological forecast
        status = str(table_datas[1].text)
        status = ' '.join(status.split())

        result['basin_hydrological_forecast'][sub_basin] = status