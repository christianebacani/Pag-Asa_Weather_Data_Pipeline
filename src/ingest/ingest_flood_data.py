'''
    Data Ingestion for Flood Data
'''
import requests
from bs4 import BeautifulSoup

def scrape_flood_information_data(url: str) -> dict:
    '''
        Performs web scraping on the Pag-asa website to
        ingest flood information data. The function 
        retrieves the data containing the flood information.
    '''
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        print(f'The website didn\'t accept the request!')
        return {}

    soup = BeautifulSoup(response.text, 'html.parser') # Parse response to a Beautiful Soup object
    div_tag_with_row_flood_page_class = soup.find('div', attrs={'class': 'row flood-page'})
    list_of_all_div_tag_with_article_content_classes = div_tag_with_row_flood_page_class.find_all('div', attrs={'class': 'col-md-12 article-content'})

    basin_hydrological_forecast = list_of_all_div_tag_with_article_content_classes[0]
    table_tag = basin_hydrological_forecast.find('table', attrs={'class': 'table'})
    list_of_all_tbody_tags = table_tag.find_all('tbody')

    result = {}
    result['basin_hydrological_forecast'] = {}

    major_river_basins_table = list_of_all_tbody_tags[0]
    list_of_all_table_row_tags = major_river_basins_table.find_all('tr')

    for table_row_tag in list_of_all_table_row_tags:
        list_of_all_table_data_tags = table_row_tag.find_all('td')

        if len(list_of_all_table_data_tags) != 2:
            continue

        # Scrape the major river basin name for basin hydrological forecast        
        major_river_basin = str(list_of_all_table_data_tags[0].text)

        if major_river_basin == '':
            continue

        # Scrape the status of the major river basin for basin hyrdological forecast
        status = str(list_of_all_table_data_tags[1].text)
        status = ' '.join(status.split())

        if status == '':
            status = 'None'

        result['basin_hydrological_forecast'][major_river_basin] = status

    sub_basins_table = list_of_all_tbody_tags[1]
    list_of_all_table_row_tags = sub_basins_table.find_all('tr')

    for table_row_tag in list_of_all_table_row_tags:
        list_of_all_table_data_tags = table_row_tag.find_all('td')

        if len(list_of_all_table_data_tags) != 2:
            continue

        # Scrape the sub basin name for basin hydrological forecast
        sub_basin = str(list_of_all_table_data_tags[0].text)

        if sub_basin == '':
            continue

        # Scrape status of the sub basin for basin hydrological forecast
        status = str(list_of_all_table_data_tags[1].text)
        status = ' '.join(status.split())

        if status == '':
            status = 'None'

        result['basin_hydrological_forecast'][sub_basin] = status
    
    dam_water_level_update = list_of_all_div_tag_with_article_content_classes[1]
    div_tag_with_panel_class = dam_water_level_update.find('div', attrs={'class': 'panel'})
    
    # Scrape the datetime of the water level update of dam
    dam_weather_level_update_datetime = str(div_tag_with_panel_class.find('h5', attrs={'class': 'pull-right'}).text)
    
    if dam_weather_level_update_datetime == '':
        dam_weather_level_update_datetime = 'None'
    
    result['dam_weather_level_update_datetime'] = dam_weather_level_update_datetime

    table_tag_with_dam_table_class = div_tag_with_panel_class.find('table', attrs={'class': 'table dam-table'})
    tbody_tag = table_tag_with_dam_table_class.find('tbody', attrs={'style': 'text-align: center;vertical-align: middle;'})
    list_of_all_table_row_tags = tbody_tag.find_all('tr')

    # We iterate using 4 index because every row of the table from dam water level update consist of 4 tr tags
    for index in range(0, len(list_of_all_table_row_tags), 4):
        dam_water_level_update_data = list_of_all_table_row_tags[index : index + 4]

        if len(dam_water_level_update_data) != 4:
            continue

        data = {
            'observation_in_time_and_date': [],
            'reservoir_water_level_in_meter': [],
            'water_level_deviation_in_hour': [],
            'water_level_deviation_in_amount': [],
            'normal_high_water_level_in_meter': [],
            'deviation_from_nhwl_in_meter': [],
            'rule_curve_elevation_in_meter': [],
            'deviation_from_rule_curve_in_meter': [],
            'gate_opening_in_gate': [],
            'gate_opening_in_meter': [],
            'estimated_centimeters_in_inflow': [],
            'estimated_centimeters_in_outflow': []
        }
        dam_water_level_update_columns = list(data.keys())

        # Scrape dam name for dam water level update
        dam_name = dam_water_level_update_data[0].find('td')
        dam_name = str(dam_name.text)
        
        if dam_name == '':
            continue

        '''
        Scrape the first instance of observation time, first instance of reservoir water level, 
        water level deviation (both hour and amount), normal water level, first instance of deviation from NHWL, 
        first instance of rule curve elevation, first instance of deviation from rule, first instance of gate opening (both gate and meters), 
        and lastly first instances of estimated in centimeters (both inflow and outflow)
        '''
        list_of_all_table_data_tags = dam_water_level_update_data[0].find_all('td')[1:]

        for table_data_tag_index, table_data_tag in enumerate(list_of_all_table_data_tags):
            table_data_tag = str(table_data_tag.text)
            table_data_tag = ' '.join(table_data_tag.split())

            if table_data_tag == '':
                table_data_tag = 'None'

            column = dam_water_level_update_columns[table_data_tag_index]
            data[column].append(table_data_tag)
        
        # Scrape the first instance of observation date
        observation_date = str(dam_water_level_update_data[1].find('td').text)
        
        if observation_date == '':
            pass

        else:
            data['observation_in_time_and_date'][0] = data['observation_in_time_and_date'][0] + ' ' + observation_date

        list_of_all_table_data_tags = dam_water_level_update_data[2].find_all('td')

        if list_of_all_table_data_tags == []:
            continue

        # Scrape the second instance of observation time
        observation_time = str(list_of_all_table_data_tags[0].text)

        if observation_time == '':
            observation_time == 'None'

        data['observation_in_time_and_date'].append(observation_time)

        # Scrape the second instance of reservoir water level in meters
        reservoir_water_level = str(list_of_all_table_data_tags[1].text)

        if reservoir_water_level == '':
            reservoir_water_level = 'None'

        data['reservoir_water_level_in_meter'].append(reservoir_water_level)

        # Scrape the second instance of deviation from nhwl in meters
        deviation_from_nhwl = str(list_of_all_table_data_tags[2].text)

        if deviation_from_nhwl == '':
            deviation_from_nhwl = 'None'

        data['deviation_from_nhwl_in_meter'].append(deviation_from_nhwl)

        # Scrape the second instance of rule curve elevation in meters
        rule_curve_elevation = str(list_of_all_table_data_tags[3].text)
        
        if rule_curve_elevation == '':
            rule_curve_elevation = 'None'

        data['rule_curve_elevation_in_meter'].append(rule_curve_elevation)

        # Scrape the second instance of deviation from rule curve in meters
        deviation_from_rule_curve = str(list_of_all_table_data_tags[4].text)

        if deviation_from_rule_curve == '':
            deviation_from_rule_curve = 'None'
        
        data['deviation_from_rule_curve_in_meter'].append(deviation_from_rule_curve)

        # Scrape the second instance of gate opening (gates)
        gate_opening_in_gate = str(list_of_all_table_data_tags[5].text)

        if gate_opening_in_gate == '':
            gate_opening_in_gate = 'None'
        
        data['gate_opening_in_gate'].append(gate_opening_in_gate)

        # Scrape the second instance of gate opening (meters)
        gate_opening_in_meter = str(list_of_all_table_data_tags[6].text)
        
        if gate_opening_in_meter == '':
            gate_opening_in_meter = 'None'
        
        data['gate_opening_in_meter'].append(gate_opening_in_meter)

        # Scrape the second instance of estimated centimeters (inflow)
        estimated_centimeters_in_inflow = str(list_of_all_table_data_tags[7].text)

        if estimated_centimeters_in_inflow == '':
            estimated_centimeters_in_inflow = 'None'

        data['estimated_centimeters_in_inflow'].append(estimated_centimeters_in_inflow)

        # Scrape the second instance of estimated centimeters (outflow)
        estimated_centimeters_in_outflow = str(list_of_all_table_data_tags[8].text)

        if estimated_centimeters_in_outflow == '':
            estimated_centimeters_in_outflow = 'None'
        
        data['estimated_centimeters_in_outflow'].append(estimated_centimeters_in_outflow)

        # Scrape the second instance of observation date
        observation_date = str(dam_water_level_update_data[3].find('td').text)
        
        if observation_date == '':
            pass

        else:
            data['observation_in_time_and_date'][1] = data['observation_in_time_and_date'][1] + ' ' + observation_date
        
        result[dam_name] = data

    return result