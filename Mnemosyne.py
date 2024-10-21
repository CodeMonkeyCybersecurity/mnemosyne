from flask import Flask, request
import os
from datetime import datetime
import json

app = Flask(__name__)

LOG_DIR = "/var/log/cybermonkey-received-logs"

# Load configuration from ssl.json
def load_ssl_config():
    with open('ssl.json', 'r') as config_file:
        return json.load(config_file)

if __name__ == '__main__':
    ssl_config = load_ssl_config()
    ssl_cert = ssl_config.get("ssl_cert")
    ssl_key = ssl_config.get("ssl_key")
    
    if ssl_cert and ssl_key:
        # Enable IPv6 by binding to '::'
        app.run(host='::', port=443, ssl_context=(ssl_cert, ssl_key))
    else:
        print("SSL certificate or key not found in ssl.json.")

@app.route('/upload_logs', methods=['POST'])
def upload_logs():
    if 'logfile' not in request.files:
        return "No log file provided.", 400
    
    logfile = request.files['logfile']
    hostname = request.form.get('hostname', 'unknown')
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Create directories if they don't exist
    save_dir = os.path.join(LOG_DIR, 'persephone', hostname, date_str)
    os.makedirs(save_dir, exist_ok=True)
    
    # Save the log file
    save_path = os.path.join(save_dir, logfile.filename)
    logfile.save(save_path)
    
    return "Log uploaded successfully.", 200
