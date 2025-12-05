'''
    Module for executing ingestion, transformation,
    and loading functions for the tropical cyclone
    associated rainfall from the PAGASA-DOST website.
'''
from ingest.tropical_cyclone_associated_rainfall import create_subdir

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