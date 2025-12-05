'''
    Module for executing ingestion, transformation,
    and loading functions for the tropical cyclone
    associated rainfall from the PAGASA-DOST website.
'''
from ingest.tropical_cyclone_associated_rainfall import create_subdir
from ingest.tropical_cyclone_associated_rainfall import extract_beautiful_soup_object

def ingest_tropical_cyclone_associated_rainfall(
) -> None:
    '''
        Ingest the tropical cyclone
        associated rainfall from the
        PAGASA-DOST website by executing
        all functions in the 
        tropical_cyclone_associated_rainfall
        module of the src/ingest package.
    '''
    # Run all functions to ingest weather advisory data
    create_subdir()
    soup = extract_beautiful_soup_object(
        'https://www.pagasa.dost.gov.ph/climate/tropical-cyclone-associated-rainfall'
    )