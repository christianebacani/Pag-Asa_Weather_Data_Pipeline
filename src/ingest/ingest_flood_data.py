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

        if len(table_datas) != 2:
            continue

        # Scrape major river basin name for basin hydrological forecast        
        major_river_basin = str(table_datas[0].text)

        if major_river_basin == '':
            continue

        # Scrape status for basin hydrological forecast
        status = str(table_datas[1].text)
        status = ' '.join(status.split())

        if status == '':
            status = 'None'

        result['basin_hydrological_forecast'][major_river_basin] = status

    sub_basins_table = list_of_tbody_tags[1]
    table_rows = sub_basins_table.find_all('tr')

    for table_row in table_rows:
        table_datas = table_row.find_all('td')

        if len(table_datas) != 2:
            continue

        # Scrape sub basin name for basin hydrological forecast
        sub_basin = str(table_datas[0].text)

        if sub_basin == '':
            continue

        # Scrape status for basin hydrological forecast
        status = str(table_datas[1].text)
        status = ' '.join(status.split())

        if status == '':
            status = 'None'

        result['basin_hydrological_forecast'][sub_basin] = status
    
    dam_water_level_update = list_of_all_article_content_tags[1]
    panel = dam_water_level_update.find('div', attrs={'class': 'panel'})
    
    # Scrape dam water level update datetime
    dam_weather_level_update_datetime = str(panel.find('h5', attrs={'class': 'pull-right'}).text)
    
    if dam_weather_level_update_datetime == '':
        dam_weather_level_update_datetime = 'None'
    
    result['dam_weather_level_update_datetime'] = dam_weather_level_update_datetime

    dam_table = panel.find('table', attrs={'class': 'table dam-table'})
    tbody = dam_table.find('tbody', attrs={'style': 'text-align: center;vertical-align: middle;'})
    table_rows = tbody.find_all('tr')

    # We iterate using 4 index because every row of dam water level update data contains 4 tr tags
    for index in range(0, len(table_rows), 4):
        dam_water_level_update_data = table_rows[index : index + 4]

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
        table_datas = dam_water_level_update_data[0].find_all('td')[1:]

        for table_data_index, table_data in enumerate(table_datas):
            table_data = str(table_data.text)
            table_data = ' '.join(table_data.split())

            if table_data == '':
                table_data = 'None'

            column = dam_water_level_update_columns[table_data_index]
            data[column].append(table_data)
        
        # Scrape the first instance of observation date
        observation_date = str(dam_water_level_update_data[1].find('td').text)
        
        if observation_date == '':
            pass

        else:
            data['observation_in_time_and_date'][0] = data['observation_in_time_and_date'][0] + ' ' + observation_date

        table_datas = dam_water_level_update_data[2].find_all('td')

        if table_datas == []:
            continue

        # Scrape the second instance of observation time
        observation_time = str(table_datas[0].text)

        if observation_time == '':
            observation_time == 'None'

        data['observation_in_time_and_date'].append(observation_time)

        # Scrape the second instance of reservoir water level
        reservoir_water_level = str(table_datas[1].text)

        if reservoir_water_level == '':
            reservoir_water_level = 'None'

        data['reservoir_water_level_in_meter'].append(reservoir_water_level)

        # Scrape the second instance of deviation from nhwl
        deviation_from_nhwl = str(table_datas[2].text)

        if deviation_from_nhwl == '':
            deviation_from_nhwl = 'None'

        data['deviation_from_nhwl_in_meter'].append(deviation_from_nhwl)

        # Scrape the second instance of rule curve elevation
        rule_curve_elevation = str(table_datas[3].text)
        
        if rule_curve_elevation == '':
            rule_curve_elevation = 'None'

        data['rule_curve_elevation_in_meter'].append(rule_curve_elevation)

        # Scrape the second instance of deviation from rule curve
        deviation_from_rule_curve = str(table_datas[4].text)

        if deviation_from_rule_curve == '':
            deviation_from_rule_curve = 'None'
        
        data['deviation_from_rule_curve_in_meter'].append(deviation_from_rule_curve)

        # Scrape the second instance of gate opening (in gate)
        gate_opening_in_gate = str(table_datas[5].text)

        if gate_opening_in_gate == '':
            gate_opening_in_gate = 'None'
        
        data['gate_opening_in_gate'].append(gate_opening_in_gate)

        # Scrape the second instance of gate opening (in meters)
        gate_opening_in_meter = str(table_datas[6].text)
        
        if gate_opening_in_meter == '':
            gate_opening_in_meter = 'None'
        
        data['gate_opening_in_meter'].append(gate_opening_in_meter)

        # Scrape the second instance of estimated centimeters (in inflow)
        estimated_centimeters_in_inflow = str(table_datas[7].text)

        if estimated_centimeters_in_inflow == '':
            estimated_centimeters_in_inflow = 'None'

        data['estimated_centimeters_in_inflow'].append(estimated_centimeters_in_inflow)

        # Scrape the second instance of estimated centimeters (in outflow)
        estimated_centimeters_in_outflow = str(table_datas[8].text)

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