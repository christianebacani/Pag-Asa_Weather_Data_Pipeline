'''
    Module to ingest tropical cyclone
    associated rainfall from the PAGASA-
    DOST website.
'''
import os
import requests
import json
from bs4 import BeautifulSoup

def create_subdir():
    '''
        Creates the
        data/raw/tropical_cyclone_associated_rainfall/
        subdirectory to store JSON files for
        tropical cyclone associated rainfall from the
        PAGASA-DOST website.
    '''
    # Create the data/raw/tropical_cyclone_associated_rainfall/ subdirectory if it doesn't exist
    if not os.path.exists('data/raw/tropical_cyclone_associated_rainfall'):
        os.makedirs('data/raw/tropical_cyclone_associated_rainfall')