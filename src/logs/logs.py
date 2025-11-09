'''
    Data Pipeline Logs
'''
import pandas as pd

from datetime import datetime

def generate_logs_from_pipeline_job(job: str) -> None:
    '''
        Generate function to generate logs
        when executing different jobs of
        the pipeline
    '''
    format = '%Y-%m-%d %H:%M:%s'
    now = datetime.now()
    timestamp = now.strftime(format)

    logs = pd.read_csv('src/logs/logs.csv')
    logs = pd.concat([logs, pd.DataFrame({'jobs': [job], 'timestamps': [timestamp]})], ignore_index=True)
    logs.to_csv('src/logs/logs.csv', index=False)