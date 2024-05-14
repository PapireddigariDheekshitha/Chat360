import os
import re
from datetime import datetime
import json

LOG_DIR = 'logs/'

def search_logs(level=None, log_string=None, start_time=None, end_time=None, source=None):
    results = []
    
    for log_file in os.listdir(LOG_DIR):
        if log_file.endswith('.log'):
            with open(os.path.join(LOG_DIR, log_file), 'r') as f:
                for line in f:
                    if level and level not in line:
                        continue
                    if log_string and log_string not in line:
                        continue
                    if source and source not in line:
                        continue
                    timestamp = line.split()[0]
                    if start_time and datetime.fromisoformat(timestamp) < datetime.fromisoformat(start_time):
                        continue
                    if end_time and datetime.fromisoformat(timestamp) > datetime.fromisoformat(end_time):
                        continue
                    results.append(line)
    
    return results

def main():
    query = {
        "level": "ERROR",
        "log_string": "Failed to connect",
        "start_time": "2023-09-10T00:00:00",
        "end_time": "2023-09-15T23:59:59"
    }
    
    results = search_logs(**query)
    for result in results:
        print(result)

if __name__ == '_main_':
    main()