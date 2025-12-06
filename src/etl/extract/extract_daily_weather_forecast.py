'''
    Module to extract daily weather forecast data
    from the data/raw subdirectory on the local machine.
'''
import pandas as pd

def stage_issued_datetime(
        issued_datetime_filepath: str
) -> None:
    '''
    Stages the JSON file that contains
    the issued datetime of the daily weather
    forecast in the data/stage subdirectory
    on the local machine.

    :param issued_datetime_filepath: Relative
        filepath of the JSON file that contains
        the issued datetime of the daily weather
        forecast
    :type issued_datetime_filepath: str
    '''