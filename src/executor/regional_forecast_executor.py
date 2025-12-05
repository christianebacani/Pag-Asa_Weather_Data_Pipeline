'''
    Module for executing ingestion, transformation,
    and loading functions for the regional forecast
    specifically for the Province of Tarlac and Bataan
    from the PAGASA-DOST website.
'''
from ingest.regional_forecast import create_subdir

def ingest_regional_forecast(
) -> None:
    '''
        Ingest the regional forecast
        specifically for the Province
        of Tarlac and Bataan from the
        PAGASA-DOST website by executing
        all functions in the regional_forecast
        module of the src/ingest package.
    '''
    # Run all functions to ingest weather advisory data
    create_subdir()