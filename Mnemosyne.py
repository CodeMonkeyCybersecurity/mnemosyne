from flask import Flask, request
import os
from datetime import datetime
import json

app = Flask(__name__)

LOG_DIR = "/var/log/cybermonkey-received-logs"

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

if __name__ == '__main__':
    # Listen on port 5000 without SSL (for Nginx to forward traffic)
    app.run(host='::', port=5000)  # HTTP on port 5000
