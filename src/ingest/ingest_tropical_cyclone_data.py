'''
    Data Ingestion for Tropical Cyclone Data
'''
import requests
from bs4 import BeautifulSoup

def scrape_tropical_cyclone_bulletin_data(url: str) -> None | dict:
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
        print(f'Currently there\'s no data for the tropical cyclone!')
        return None

    list_of_all_h5_tags = list_of_all_row_tags[2].find_all('h5')

    if len(list_of_all_h5_tags) != 2:
        print(f'Currently there\'s no data for the issued datetime and validity description of the tropical cyclone!')
        return None

    # Scrape issued datetime
    issued_datetime = str(list_of_all_h5_tags[0].text)

    # Scrape validity description
    validity_description = str(list_of_all_h5_tags[1].text)
    
    tropical_cyclone_bulletin_descriptions = list_of_all_row_tags[3]
    
    # Scrape tropical cyclone current update header
    tropical_cyclone_current_update_header = (tropical_cyclone_bulletin_descriptions.find('h5').text)
    
    if tropical_cyclone_current_update_header == '':
        print(f'Currently there\'s no data for the current update header of the tropical cyclone!')
        return None
    
    # Scrape tropical cyclone descriptions
    unordered_list_tag = tropical_cyclone_bulletin_descriptions.find('ul')
    list_of_all_list_item_tags = unordered_list_tag.find_all('li')

    if list_of_all_list_item_tags == []:
        print(f'Currently there\'s no data for the current update descriptions of the tropical cyclone!')
        return None
    
    tropical_cyclone_current_update_descriptions = []

    for list_item in list_of_all_list_item_tags:
        list_item = str(list_item.text)

        if list_item == '':
            continue

        tropical_cyclone_current_update_descriptions.append(list_item)

    fifth_instance_of_row_tag = list_of_all_row_tags[4]
    list_of_all_div_tags = fifth_instance_of_row_tag.find_all('div', attrs={'class': 'col-md-6'})

    if len(list_of_all_div_tags) != 2:
        print(f'Currently there\'s no data for the location, movement, strength, and forecast position of the tropical cyclone!')
        return None
    
    list_of_all_panel_tags = list_of_all_div_tags[0].find_all('div', attrs={'class': 'panel'})
    
    # Scrape the location of eye or center of the tropical cyclone
    location_of_eye_or_center = str(list_of_all_panel_tags[0].find('p').text)
    
    if location_of_eye_or_center == '':
        print(f'Currently there\'s no data for the location of eye or center of the tropical cyclone!')
        return None

    # Scrape the movement of the tropical cyclone
    movement = list_of_all_panel_tags[1].find('div', attrs={'class': 'panel-body'})
    movement = str(movement.text)
    movement = ' '.join(movement.split())

    if movement == '':
        print(f'Currently there\'s no data for the movement of the tropical cyclone!')
        return None

    # Scrape the strength of the tropical cyclone
    strength = list_of_all_panel_tags[2].find('div', attrs={'class': 'panel-body'})
    strength = str(strength.text)
    strength = ' '.join(strength.split())

    if strength == '':
        print(f'Currently there\'s no data for the strength of the tropical cyclone!')
        return None

    # Scrape the forecast posotions of the tropical cyclone
    unordered_list_tag = list_of_all_div_tags[1].find('ul')
    list_of_all_list_item_tags = unordered_list_tag.find_all('li')

    if list_of_all_list_item_tags == []:
        print(f'Currently there\'s no data for the forecast position of the tropical cyclone!')
        return None

    forecast_positions = []

    for list_item in list_of_all_list_item_tags:
        list_item = str(list_item.text)
        list_item = ' '.join(list_item.split())

        if list_item == '':
            continue

        forecast_positions.append(list_item)
    
    sixth_instance_of_row_tag = list_of_all_row_tags[5]
    table = sixth_instance_of_row_tag.find('table', attrs={'class': 'table text-center table-header', 'style': 'margin-top:15px;'})

    tropical_cyclone_wind_signal_data = {}

    # Scrape the tropical cyclone wind signal numbers
    list_of_all_table_head_tags = table.find_all('thead')

    for table_head in list_of_all_table_head_tags:
        tropical_cyclone_wind_signal_header = str(table_head.text)
        tropical_cyclone_wind_signal_header = ' '.join(tropical_cyclone_wind_signal_header.split())

        if tropical_cyclone_wind_signal_header == '':
            continue

        image_tag = table_head.find('img')

        if image_tag is None:
            continue
        
        source_attribute_value = str(image_tag['src']).replace('https://pubfiles.pagasa.dost.gov.ph/pagasaweb/icons/hazard/tropical-cyclone/64/', '')
        source_attribute_value = source_attribute_value.replace('.png', '')
        source_attribute_value = source_attribute_value.replace('tcws', '')

        tropical_cyclone_wind_signal = tropical_cyclone_wind_signal_header + ' ' + source_attribute_value
        tropical_cyclone_wind_signal_data[tropical_cyclone_wind_signal] = {}
    
    list_of_all_table_body_tags = table.find_all('tbody')

    for table_body in list_of_all_table_body_tags:
        list_of_all_table_row_tags = table_body.find_all('tr')
        
        if list_of_all_table_row_tags == []:
            continue