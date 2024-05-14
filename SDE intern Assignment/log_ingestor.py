import json
import logging
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Set up logging
loggers = {}
for api, log_file in config['logging']['log_files'].items():
    logger = logging.getLogger(api)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    loggers[api] = logger

@app.route('/log/<api>', methods=['POST'])
def log(api):
    if api not in loggers:
        return jsonify({"error": "Unknown API"}), 400
    
    log_data = request.json
    log_level = log_data.get('level', 'INFO').upper()
    log_message = log_data.get('log string', '')
    timestamp = log_data.get('timestamp', datetime.datetime.now().isoformat())
    source = log_data.get('metadata', {}).get('source', 'unknown')
    
    log_entry = f'{timestamp} {source} {log_message}'
    
    logger = loggers[api]
    if log_level == 'ERROR':
        logger.error(log_entry)
    elif log_level == 'INFO':
        logger.info(log_entry)
    elif log_level == 'SUCCESS':
        logger.info(log_entry)
    else:
        logger.info(log_entry)
    
    return jsonify({"status": "logged"}), 200

if __name__ == '_main_':
    app.run(debug=True)