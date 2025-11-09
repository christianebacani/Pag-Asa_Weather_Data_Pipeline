'''
    Data Pipeline Logs
'''
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