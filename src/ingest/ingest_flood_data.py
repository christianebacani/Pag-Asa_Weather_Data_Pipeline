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
    list_of_all_article_content_tags = row_flood_page.find_all('div', attrs={'class': 'col-md-12 article-content'})

    basin_hydrological_forecast = list_of_all_article_content_tags[0]
    table = basin_hydrological_forecast.find('table', attrs={'class': 'table'})
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
    
    dam_water_level_update = list_of_all_article_content_tags[1]
    panel = dam_water_level_update.find('div', attrs={'class': 'panel'})
    
    # Scrape dam water level update datetime
    dam_weather_level_update_datetime = str(panel.find('h5', attrs={'class': 'pull-right'}).text)

    dam_table = panel.find('table', attrs={'class': 'table dam-table'})
    tbody = dam_table.find('tbody', attrs={'style': 'text-align: center;vertical-align: middle;'})
    table_rows = tbody.find_all('tr')

    # We iterate using 4 index because every row of dam water level update data contains 4 tr tags
    for index in range(0, len(table_rows), 4):
        dam_water_level_update_data = table_rows[index : index + 4]

        if len(dam_water_level_update_data) != 4:
            continue
        
        # TODO: Add more keys here for the column of dam water level update data containing 4 tr tags per iteration
        data = {
            'observation_time_date': [],
            'reservoir_water_level_meter': [],
            'water_level_deviation_hour': [],
            'water_level_deviation_amount': [],
            'normal_high_water_level_meter': []
        }

        table_datas = dam_water_level_update_data[0].find_all('td')

        for table_data in table_datas:
            table_data = str(table_data.text)