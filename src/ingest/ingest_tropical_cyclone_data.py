'''
    Data Ingestion for Tropical Cyclone Data
'''
import requests
from bs4 import BeautifulSoup

def scrape_tropical_cyclone_bulletin_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest tropical cyclone bulletin data. The function
        retrieves the data containing tropical cyclone bulletin.
    '''
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_tropical_cyclone_weather_bulletin_page_class = soup.find('div', attrs={'class': 'row tropical-cyclone-weather-bulletin-page'})
    div_tag_with_article_content_class = div_tag_with_tropical_cyclone_weather_bulletin_page_class.find('div', attrs={'col-md-12 article-content'})
    
    if div_tag_with_article_content_class is None:
        print(f'Currently there\'s no data for the tropical cyclone bulletin!')
        return {}

    result = {}

    list_of_all_div_tag_with_row_classes = div_tag_with_article_content_class.find_all('div', attrs={'class': 'row'})

    # Scrape the name of the tropical cyclone
    tropical_cyclone_name = str(list_of_all_div_tag_with_row_classes[1].text)
    tropical_cyclone_name = ' '.join(tropical_cyclone_name.split())

    if tropical_cyclone_name == '':
        print(f'Currently there\'s no data for the tropical cyclone!')
        return {}
    
    result['tropical_cyclone_name'] = tropical_cyclone_name

    list_of_all_h5_tags = list_of_all_div_tag_with_row_classes[2].find_all('h5')

    if len(list_of_all_h5_tags) != 2:
        print(f'Currently there\'s no data for the issued datetime and validity description of the tropical cyclone!')
        return {}

    # Scrape the issued datetime for the tropical cyclone bulletin
    issued_datetime = str(list_of_all_h5_tags[0].text)

    # Scrape the description of validity for the tropical cyclone bulletin
    validity_description = str(list_of_all_h5_tags[1].text)

    result['issued_datetime'] = issued_datetime
    result['validity_description'] = validity_description

    tropical_cyclone_bulletin_descriptions = list_of_all_div_tag_with_row_classes[3]

    # Scrape the header of the current update from tropical cyclone
    tropical_cyclone_current_update_header = (tropical_cyclone_bulletin_descriptions.find('h5').text)
    
    if tropical_cyclone_current_update_header == '':
        print(f'Currently there\'s no data for the current update header of the tropical cyclone!')
        return {}
    
    result['tropical_cyclone_current_update_header'] = tropical_cyclone_current_update_header

    # Scrape the descriptions of the tropical cyclone
    unordered_list_tag = tropical_cyclone_bulletin_descriptions.find('ul')
    list_of_all_list_item_tags = unordered_list_tag.find_all('li')

    if list_of_all_list_item_tags == []:
        print(f'Currently there\'s no data for the current update descriptions of the tropical cyclone!')
        return {}
    
    tropical_cyclone_current_update_descriptions = []

    for list_item_tag in list_of_all_list_item_tags:
        list_item_tag = str(list_item_tag.text)

        if list_item_tag == '':
            continue

        tropical_cyclone_current_update_descriptions.append(list_item_tag)

    result['tropical_cyclone_current_update_descriptions'] = tropical_cyclone_current_update_descriptions

    fifth_instance_of_div_tag_with_row_classes = list_of_all_div_tag_with_row_classes[4]
    list_of_all_div_tag_with_col_md_six_classes = fifth_instance_of_div_tag_with_row_classes.find_all('div', attrs={'class': 'col-md-6'})

    if len(list_of_all_div_tag_with_col_md_six_classes) != 2:
        print(f'Currently there\'s no data for the location, movement, strength, and forecast position of the tropical cyclone!')
        return {}

    list_of_all_div_tag_with_panel_class = list_of_all_div_tag_with_col_md_six_classes[0].find_all('div', attrs={'class': 'panel'})
    
    # Scrape the location of eye or center of the tropical cyclone
    location_of_eye_or_center = str(list_of_all_div_tag_with_panel_class[0].find('p').text)
    
    if location_of_eye_or_center == '':
        print(f'Currently there\'s no data for the location of eye or center of the tropical cyclone!')
        return {}

    result['location_of_eye_or_center'] = location_of_eye_or_center

    # Scrape the movement of the tropical cyclone
    movement = list_of_all_div_tag_with_panel_class[1].find('div', attrs={'class': 'panel-body'})
    movement = str(movement.text)
    movement = ' '.join(movement.split())

    if movement == '':
        print(f'Currently there\'s no data for the movement of the tropical cyclone!')
        return {}

    result['movement'] = movement

    # Scrape the strength of the tropical cyclone
    strength = list_of_all_div_tag_with_panel_class[2].find('div', attrs={'class': 'panel-body'})
    strength = str(strength.text)
    strength = ' '.join(strength.split())

    if strength == '':
        print(f'Currently there\'s no data for the strength of the tropical cyclone!')
        return {}

    result['strength'] = strength

    # Scrape the forecasted positions of the tropical cyclone
    unordered_list_tag = list_of_all_div_tag_with_col_md_six_classes[1].find('ul')
    list_of_all_list_item_tags = unordered_list_tag.find_all('li')

    if list_of_all_list_item_tags == []:
        print(f'Currently there\'s no data for the forecast position of the tropical cyclone!')
        return {}

    forecast_positions = []

    for list_item_tag in list_of_all_list_item_tags:
        list_item_tag = str(list_item_tag.text)
        list_item_tag = ' '.join(list_item_tag.split())

        if list_item_tag == '':
            continue

        forecast_positions.append(list_item_tag)
    
    result['forecast_positions'] = forecast_positions

    # Scrape the data for every tropical cyclone wind signal numbers
    sixth_instance_of_div_tag_with_row_classes = list_of_all_div_tag_with_row_classes[5]
    table_tag = sixth_instance_of_div_tag_with_row_classes.find('table', attrs={'class': 'table text-center table-header', 'style': 'margin-top:15px;'})
    
    if table_tag is None:
        result['tropical_cyclone_wind_signal_data'] = {}
        return result

    tropical_cyclone_wind_signal_data = {}

    # Scrape the tropical cyclone wind signal numbers
    list_of_all_table_head_tags = table_tag.find_all('thead')

    for table_head_tag in list_of_all_table_head_tags:
        tropical_cyclone_wind_signal_header = str(table_head_tag.text)
        tropical_cyclone_wind_signal_header = ' '.join(tropical_cyclone_wind_signal_header.split())

        if tropical_cyclone_wind_signal_header == '':
            continue

        image_tag = table_head_tag.find('img')

        if image_tag is None:
            continue
        
        source_class_value = str(image_tag['src']).replace('https://pubfiles.pagasa.dost.gov.ph/pagasaweb/icons/hazard/tropical-cyclone/64/', '')
        source_class_value = source_class_value.replace('.png', '')
        tropical_wind_signal_number = source_class_value.replace('tcws', '')
        
        tropical_cyclone_wind_signal = tropical_cyclone_wind_signal_header + ' ' + tropical_wind_signal_number
        tropical_cyclone_wind_signal_data[tropical_cyclone_wind_signal] = {}

    # Scrape the data of affected areas, meteorological condition, impact of the wind, precautionary measures, 
    # and list of what to do for every tropical cyclone wind signal number
    list_of_all_table_body_tags = table_tag.find_all('tbody')
    
    for table_body_tag in list_of_all_table_body_tags:
        list_of_all_table_row_tags = table_body_tag.find_all('tr')
        
        if list_of_all_table_row_tags == []:
            continue
        
        data = {
            'affected_areas': [],
            'meteorological_condition': [],
            'impact_of_the_wind': [],
            'precautionary_measures': [],
            'what_to_do': []
        }

        # Scrape the affected areas for a specific tropical cyclone wind signal number
        list_of_all_table_data_tags = list_of_all_table_row_tags[0].find_all('td')        
        affected_areas = str(list_of_all_table_data_tags[1].text)
        affected_areas = ' '.join(affected_areas.split())
        affected_areas = affected_areas.replace('Luzon ', 'Luzon: ')
        affected_areas = affected_areas.replace('Visayas ', '\nVisayas: ')
        affected_areas = affected_areas.replace('Mindanao ', '\nMindanao: ')
        data['affected_areas'].append(affected_areas)

        # Scrape the meteorological condition for a specific tropical cyclone wind signal number
        list_of_all_table_data_tags = list_of_all_table_row_tags[1].find_all('td')
        meteorological_condition = str(list_of_all_table_data_tags[1].text)
        meteorological_condition = ' '.join(meteorological_condition.split())
        data['meteorological_condition'].append(meteorological_condition)

        # Scrape the impact of the wind for a specific tropical cyclone wind signal number
        list_of_all_table_data_tags = list_of_all_table_row_tags[2].find_all('td')
        impact_of_the_wind = str(list_of_all_table_data_tags[1].text)
        impact_of_the_wind = ' '.join(impact_of_the_wind.split())
        data['impact_of_the_wind'].append(impact_of_the_wind)

        # Scrape the precautionary measures for a specific tropical cyclone wind signal number
        list_of_all_table_data_tags = list_of_all_table_row_tags[3].find_all('td')
        precautionary_measures = str(list_of_all_table_data_tags[1].text)
        precautionary_measures = ' '.join(precautionary_measures.split())
        data['precautionary_measures'].append(precautionary_measures)

        # Scrape the list of what to do for a specific tropical cyclone wind signal number
        list_of_all_table_data_tags = list_of_all_table_row_tags[4].find_all('td')
        what_to_do = str(list_of_all_table_data_tags[1].text)
        what_to_do = ' '.join(what_to_do.split())
        data['what_to_do'].append(what_to_do)
        
        tropical_cyclone_wind_signal_numbers = list(tropical_cyclone_wind_signal_data.keys())
        
        # Store the data to the corresponding tropical cyclone wind signal number
        for tropical_cyclone_wind_signal_number in tropical_cyclone_wind_signal_numbers:
            if tropical_cyclone_wind_signal_data[tropical_cyclone_wind_signal_number] != {}:
                continue

            tropical_cyclone_wind_signal_data[tropical_cyclone_wind_signal_number] = data
            break
    
    result['tropical_cyclone_wind_signal_data'] = tropical_cyclone_wind_signal_data

    return result

def scrape_tropical_cyclone_warning_for_shipping_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest tropical cyclone warning for shipping data. The function
        retrieves the data containing tropical cyclone warning for shipping.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_tropical_cyclone_warning_for_shipping_class = soup.find('div', attrs={'class': 'row tropical-cyclone-warning-for-shipping'})
    div_tag_with_article_content_class = div_tag_with_tropical_cyclone_warning_for_shipping_class.find('div', attrs={'class': 'col-md-12 article-content'})

    if div_tag_with_article_content_class is None:
        print(f'Currently there\'s no data for the tropical cyclone warning for shipping data!')
        return {}

    # Scrape the URL of the tropical cyclone warning for shipping
    iframe_tag = div_tag_with_article_content_class.find('iframe')

    if iframe_tag is None:
        print(f'Currently there\'s no data for the tropical cyclone warning for shipping data!')
        return {}

    result = {}

    url = str(iframe_tag['src']).strip()
    result['url_of_the_tropical_cyclone_warning_for_shipping'] = url

    return result

def scrape_forecast_storm_surge_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest forecast storm surge data. The function 
        retrieves the URL containing the forecasted storm 
        surge data in PDF Format.
    '''
    # TODO: To be implemented
    return {}

def scrape_tropical_cyclone_warning_for_agriculture_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest tropical cyclone warning for agriculture
        data. The function retrieves the data containing
        tropical cyclone warning for agriculture.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_agriculture_page_class = soup.find('div', attrs={'class': 'row agriculture-page'})
    div_tag_with_col_md_twelve_article_content_class = div_tag_with_row_agriculture_page_class.find('div', attrs={'class': 'col-md-12 article-content'})
    div_tag_with_row_class = div_tag_with_col_md_twelve_article_content_class.find('div', attrs={'class': 'row'})
    div_tag_with_col_md_twelve_class = div_tag_with_row_class.find('div', attrs={'class': 'col-md-12'})

    list_of_all_div_tag_with_row_classes = div_tag_with_col_md_twelve_class.find_all('div', attrs={'class': 'row'})

    first_instance_of_div_tag_with_row_class = list_of_all_div_tag_with_row_classes[0]

    # Scrape the header of the tropical cyclone warning for agriculture
    div_tag_with_col_md_eight_col_sm_five_col_xs_four_text_center_class = first_instance_of_div_tag_with_row_class.find('div', attrs={'class': 'col-md-8 col-sm-5 col-xs-4 text-center'})
    
    if div_tag_with_col_md_eight_col_sm_five_col_xs_four_text_center_class is None:
        return {}
    
    # TODO: Add more content here...