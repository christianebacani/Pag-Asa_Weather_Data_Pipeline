'''
    Data Ingestion for Tropical Cyclone Data
'''
import requests
from bs4 import BeautifulSoup

def scrape_tropical_cyclone_bulletin_data(url: str) -> dict:
    '''
        Scrape function to perform web-scraping
        to ingest tropical cyclone bulletin data from
        the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/) 
    '''
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    tropical_cyclone_weather_bulletin_page = soup.find('div', attrs={'class': 'row tropical-cyclone-weather-bulletin-page'})
    article_content = tropical_cyclone_weather_bulletin_page.find('div', attrs={'col-md-12 article-content'})

    if article_content is None:
        print(f'Currently there\'s no data for the tropical cyclone bulletin!')
        return {}

    result = {}

    list_of_all_row_tags = article_content.find_all('div', attrs={'class': 'row'})

    # Scrape tropical cyclone name    
    tropical_cyclone_name = str(list_of_all_row_tags[1].text)
    tropical_cyclone_name = ' '.join(tropical_cyclone_name.split())

    if tropical_cyclone_name == '':
        print(f'Currently there\'s no data for the tropical cyclone!')
        return {}
    
    result['tropical_cyclone_name'] = tropical_cyclone_name

    list_of_all_h5_tags = list_of_all_row_tags[2].find_all('h5')

    if len(list_of_all_h5_tags) != 2:
        print(f'Currently there\'s no data for the issued datetime and validity description of the tropical cyclone!')
        return {}

    # Scrape issued datetime
    issued_datetime = str(list_of_all_h5_tags[0].text)

    # Scrape validity description
    validity_description = str(list_of_all_h5_tags[1].text)

    result['issued_datetime'] = issued_datetime
    result['validity_description'] = validity_description

    tropical_cyclone_bulletin_descriptions = list_of_all_row_tags[3]
    
    # Scrape tropical cyclone current update header
    tropical_cyclone_current_update_header = (tropical_cyclone_bulletin_descriptions.find('h5').text)
    
    if tropical_cyclone_current_update_header == '':
        print(f'Currently there\'s no data for the current update header of the tropical cyclone!')
        return {}
    
    result['tropical_cyclone_current_update_header'] = tropical_cyclone_current_update_header

    # Scrape tropical cyclone descriptions
    unordered_list_tag = tropical_cyclone_bulletin_descriptions.find('ul')
    list_of_all_list_item_tags = unordered_list_tag.find_all('li')

    if list_of_all_list_item_tags == []:
        print(f'Currently there\'s no data for the current update descriptions of the tropical cyclone!')
        return {}
    
    tropical_cyclone_current_update_descriptions = []

    for list_item in list_of_all_list_item_tags:
        list_item = str(list_item.text)

        if list_item == '':
            continue

        tropical_cyclone_current_update_descriptions.append(list_item)

    result['tropical_cyclone_current_update_descriptions'] = tropical_cyclone_current_update_descriptions

    fifth_instance_of_row_tag = list_of_all_row_tags[4]
    list_of_all_div_tags = fifth_instance_of_row_tag.find_all('div', attrs={'class': 'col-md-6'})

    if len(list_of_all_div_tags) != 2:
        print(f'Currently there\'s no data for the location, movement, strength, and forecast position of the tropical cyclone!')
        return {}

    list_of_all_panel_tags = list_of_all_div_tags[0].find_all('div', attrs={'class': 'panel'})
    
    # Scrape the location of eye or center of the tropical cyclone
    location_of_eye_or_center = str(list_of_all_panel_tags[0].find('p').text)
    
    if location_of_eye_or_center == '':
        print(f'Currently there\'s no data for the location of eye or center of the tropical cyclone!')
        return {}

    result['location_of_eye_or_center'] = location_of_eye_or_center

    # Scrape the movement of the tropical cyclone
    movement = list_of_all_panel_tags[1].find('div', attrs={'class': 'panel-body'})
    movement = str(movement.text)
    movement = ' '.join(movement.split())

    if movement == '':
        print(f'Currently there\'s no data for the movement of the tropical cyclone!')
        return {}

    result['movement'] = movement

    # Scrape the strength of the tropical cyclone
    strength = list_of_all_panel_tags[2].find('div', attrs={'class': 'panel-body'})
    strength = str(strength.text)
    strength = ' '.join(strength.split())

    if strength == '':
        print(f'Currently there\'s no data for the strength of the tropical cyclone!')
        return {}

    result['strength'] = strength

    # Scrape the forecast positions of the tropical cyclone
    unordered_list_tag = list_of_all_div_tags[1].find('ul')
    list_of_all_list_item_tags = unordered_list_tag.find_all('li')

    if list_of_all_list_item_tags == []:
        print(f'Currently there\'s no data for the forecast position of the tropical cyclone!')
        return {}

    forecast_positions = []

    for list_item in list_of_all_list_item_tags:
        list_item = str(list_item.text)
        list_item = ' '.join(list_item.split())

        if list_item == '':
            continue

        forecast_positions.append(list_item)
    
    result['forecast_positions'] = forecast_positions

    sixth_instance_of_row_tag = list_of_all_row_tags[5]
    table = sixth_instance_of_row_tag.find('table', attrs={'class': 'table text-center table-header', 'style': 'margin-top:15px;'})
    
    if table is None:
        result['tropical_cyclone_wind_signal_data'] = {}
        print(f'Currently there\'s no data for the wind signal of the tropical cyclone!')
        return {}

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
        tropical_wind_signal_number = source_attribute_value.replace('tcws', '')
        
        tropical_cyclone_wind_signal = tropical_cyclone_wind_signal_header + ' ' + tropical_wind_signal_number
        tropical_cyclone_wind_signal_data[tropical_cyclone_wind_signal] = {}

    # TODO: To be implemented (because currently there's no data of wind signal of the tropical cyclone from the website)    
    list_of_all_table_body_tags = table.find_all('tbody')

    for table_body in list_of_all_table_body_tags:
        list_of_all_table_row_tags = table_body.find_all('tr')
        
        if list_of_all_table_row_tags == []:
            continue

def scrape_tropical_cyclone_warning_for_shipping_data(url: str) -> None | dict:
    '''
        Scrape function to perform web-scraping
        to ingest tropical cyclone warning from shipping 
        data in PDF Format from the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/) 
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    row_tropical_cycline_warning_for_shipping_page = soup.find('div', attrs={'class': 'row tropical-cyclone-warning-for-shipping'})
    article_content = row_tropical_cycline_warning_for_shipping_page.find('div', attrs={'class': 'col-md-12 article-content'})

    if article_content is None:
        print(f'Currently there\'s no data for the tropical cyclone warning for shipping data in PDF format!')
        return {}

    # Scrape the tropical cyclone warning for shipping in PDF Format
    iframe_tag = article_content.find('iframe')
    
    if iframe_tag is None:
        print(f'Currently there\'s no data for the tropical cyclone warning for shipping data in PDF format!')
        return {}

    document = str(iframe_tag['src']).strip()

    result = {}
    result['tropical_cyclone_warning_for_shipping_data_in_pdf_format'] = document

    return result

def scrape_forecast_storm_surge_data(url: str) -> None | dict:
    '''
        Scrape function to perform web-scraping
        to ingest forecast storm surge data in PDF
        format from the Website of Pag-Asa (https://www.pagasa.dost.gov.ph/)         
    '''