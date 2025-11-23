'''
    Weather Outlook for Selected Philippine Cities Module
'''
import os

def create_weather_outlook_for_selected_ph_cities_subdir() -> None:
    '''
        Function to create data/raw/weather_outlook_for_selected_ph_cities/
        subdirectory to store dedicated json files
        for the ingested data of weather outlook for selected philippine cities
        from the website of pag-asa dost website.
    '''
    # Create the data/raw/weather_outlook_for_selected_ph_cities/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/weather_outlook_for_selected_ph_cities'):
        os.makedirs('data/raw/weather_outlook_for_selected_ph_cities')