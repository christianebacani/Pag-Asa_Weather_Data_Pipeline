'''
    Data Ingestion
'''
import requests
from bs4 import BeautifulSoup

def scrape_daily_weather_forecast(url: str) -> dict:
    '''
        Scrape function to perform web
        scraping to ingest the data for
        daily weather forecast using Pag-Asa
        Website (https://www.pagasa.dost.gov.ph/)
    '''
    try:
        result = {}

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser') # Parse to BeautifulSoup Object

        row_weather_page = soup.find_all('div', attrs={'class': 'row weather-page'})[0]
        content = row_weather_page.find_all('div', attrs={'class': 'row'})[0]

        # Scrape daily weather issued datetime
        daily_weather_issued_datetime = str(content.find_all('div', attrs={'class': 'col-md-12 col-lg-12 issue'})[0].find('b').text)

        # Scrape synopsis
        synopsis = content.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[0]
        synopsis = str(synopsis.find('p').text)  

        # Scrape tropical cyclone information
        tc_information = content.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[1]
        table = tc_information.find('table', attrs={'style': 'width: 100%; border: 1px solid black; border-collapse: collapse;'})
        tbody = table.find('tbody')
        tr = tbody.find_all('tr')

        tc_information_data = []

        for row in tr:
            data = str(row.text)
            data = ' '.join(data.split())
            tc_information_data.append(data)

        # Scrape forecasted weather conditions
        forecast_weather_cond = content.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[2]
        table = forecast_weather_cond.find('table', attrs={'class': 'table table-striped'})
        tbody = table.find('tbody')
        tr = tbody.find_all('tr')

        forecast_weather_cond_data = []

        for row in tr:
            td = row.find_all('td', attrs={'class': 'text-center'})
            data = []

            for cell in td:
                cell = str(cell.text)
                data.append(cell)            
            
            forecast_weather_cond_data.append(data)
        
        # Scrape forecasted wind and coastal water conditions
        forecast_wind_and_coast_water_cond = content.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[3]
        table = forecast_wind_and_coast_water_cond.find('table', attrs={'class': 'table table-striped'})
        tbody = table.find('tbody')
        tr = tbody.find_all('tr')

        forecast_wind_and_coast_water_cond_data = []

        for row in tr:
            td = row.find_all('td', attrs={'class': 'text-center'})
            data = []

            for cell in td:
                cell = str(cell.text)
                data.append(cell)
                        
            forecast_wind_and_coast_water_cond_data.append(data)

        # Scrape temperature and relative humidity
        temp_and_relative_humidity = content.find_all('div', attrs={'class': 'row', 'style': 'margin-left: 0; margin-right: 0;'})[0]
        temp_and_relative_humidity = temp_and_relative_humidity.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[0]
        temp_and_relative_humidity_desc = str(temp_and_relative_humidity.find('div', attrs={'style': 'display: flex; flex-direction: column;'}).text)
        temp_and_relative_humidity_desc = ' '.join(temp_and_relative_humidity_desc.split())
        
        table = temp_and_relative_humidity.find('table')
        tbody = table.find('tbody')
        tr = tbody.find_all('tr')

        temp_and_relative_humidity_data = []

        for row in tr:
            td = row.find_all('td', attrs={'class': 'text-center'})
            data = []

            for cell in td:
                cell = str(cell.text)
                data.append(cell)

            temp_and_relative_humidity_data.append(data)
        
        # Stores the scraped data to a dictionary
        result['daily_weather_issued_datetime'] = daily_weather_issued_datetime
        result['synopsis'] = synopsis
        result['tc_information'] = tc_information_data
        result['forecast_weather_cond'] = forecast_weather_cond_data
        result['forecast_wind_and_coast_water_cond'] = forecast_wind_and_coast_water_cond_data
        result['temp_and_relative_humidity_desc'] = temp_and_relative_humidity_desc
        result['temp_and_relative_humidity'] = temp_and_relative_humidity_data

        return result

    except Exception as error_message:
        print(f'Error: {error_message}')
        print(f'Status Code: {response.status_code}')
    
def scrape_weather_outlook_selected_ph_cities(url: str) -> dict:
    '''
        Scrape function to perform web
        scraping to ingest the data for
        weather outlook of selected philippine
        cities using Pag-Asa Website (https://www.pagasa.dost.gov.ph/)
    '''
    try:
        result = {}

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser') # Parse to BeautifulSoup Object
        
        row_weather_page = soup.find_all('div', attrs={'class': 'row weather-page'})[0]

        # Scrape weather outlook issued datetime
        validity = row_weather_page.find_all('div', attrs={'class': 'col-md-12 col-lg-12 issue'})[0]
        weather_outlook_issued_datetime = str(validity.find('b').text)
        weather_outlook_issued_datetime = ' '.join(weather_outlook_issued_datetime.split())

        # Scrape cities
        panel = row_weather_page.find_all('div', attrs={'class': 'col-md-12 col-lg-12'})[0]
        panel_body = panel.find_all('div', attrs={'class': 'panel-body'})[0]
        cities = panel_body.find_all('div', attrs={'class': 'panel panel-default panel-pagasa'})

        result['weather_outlook_issued_datetime'] = weather_outlook_issued_datetime

        for city in cities:
            # Scrape city name
            panel_title = city.find('div', attrs={'class': 'panel-title'})
            city_name = str(panel_title.find('a').text)
            city_name = ' '.join(city_name.split())

            row = city.find('div', attrs={'class': 'row'})
            table = row.find('table', attrs={'class': 'table'})

            # Scrape weather outlook dates per city 
            thead = table.find('thead', attrs={'class': 'desktop-view-thead'})
            tr = thead.find('tr')
            th = tr.find_all('th')

            dates = []

            for table_header in th:
                table_header = str(table_header.text)
                table_header = ' '.join(table_header.split())
                dates.append(table_header)

            # Scrape minimum and maximum temperature and chances of rain per cities
            tbody = table.find('tbody')
            desktop_view_tr = tbody.find('tr', attrs={'class': 'desktop-view-tr'})
            td = desktop_view_tr.find_all('td')

            minimum_and_maximum_temp_data = []
            chances_of_rain_data = []

            for table_data in td:
                weather_values = table_data.find('div', attrs={'class': 'weather-values'})

                temperatures = weather_values.find('div', attrs={'class': 'ol-temperature'})
                temperatures = temperatures.find_all('span')
                temperature_data = []

                for temperature in temperatures:
                    temperature = str(temperature.text)
                    temperature_data.append(temperature)
                    
                minimum_and_maximum_temp_data.append(temperature_data)
                
                ol_forecast = table_data.find('div', attrs={'class': 'ol-forecast'})
                chance_of_rain = str(ol_forecast.find('span', attrs={'style': 'font-weight:bold; color: rgb(9, 73, 156);'}).text)
                chances_of_rain_data.append(chance_of_rain)

            result[city_name] = {}
            result[city_name]['dates'] = dates
            result[city_name]['minimum_and_maximum_temp_data'] = minimum_and_maximum_temp_data
            result[city_name]['chances_of_rain_data'] = chances_of_rain_data
        
        return result

    except Exception as error_message:
        print(f'Error: {error_message}')
        print(f'Status Code: {response.status_code}')
    
def scrape_asian_cities_weather_forecast(url: str) -> None:
    '''
        Scrape function to perform web
        scraping to ingest the data for
        weather forecast of asian cities
        using Pag-Asa Website (https://www.pagasa.dost.gov.ph/)
    '''
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser') # Parse to BeautifulSoup Object

        row_weather_page = soup.find_all('div', attrs={'class': 'row weather-page'})[0]
        article_content = row_weather_page.find_all('div', attrs={'class': 'col-md-10 col-md-offset-1 col-xs-10 col-xs-offset-1 article-content'})[0]
        
        # Scrape issued datetime and valid time
        validity = article_content.find_all('div', attrs={'class': 'validity'})[0]
        asian_cities_weather_forecast_issued_datetime = str(validity.find_all('b')[0].text)
        print(asian_cities_weather_forecast_issued_datetime)

    except Exception as error_message:
        print(f'Error: {error_message}')
        print(f'Status Code: {response.status_code}')