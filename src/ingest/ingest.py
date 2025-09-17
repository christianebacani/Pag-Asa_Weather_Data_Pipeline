'''
    Data Ingestion
'''
import requests

def scrape_daily_weather_forecast(url: str) -> None:
    '''
        Scrape function to perform web
        scraping to ingest the data for
        daily weather forecast of Pag-Asa
    '''
    try:
        response = requests.get(url)
    
    except Exception as error_message:
        print(f'Error: {error_message}')