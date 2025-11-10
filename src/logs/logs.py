'''
    Data Pipeline Logs
'''
import pandas as pd
from datetime import datetime

def generate_logs(log_message: str) -> None:
    '''
        Function to generate logs based on the ETL Pipeline job/s.
    '''
    format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(format)
    
    # Generate logs usins pandas for logs dataset (csv format)
    logs = pd.read_csv('src/logs/logs.csv')
    logs = pd.concat([logs, pd.DataFrame({'messages': [log_message], 'timestamps': [timestamp]})], ignore_index=True)
    logs.to_csv('src/logs/logs.csv', index=False)

if __name__ == '__main__':
    generate_logs('START')