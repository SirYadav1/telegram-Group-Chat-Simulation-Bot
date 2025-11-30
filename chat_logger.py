import json
import csv
from datetime import datetime
import os

class ChatLogger:
    def __init__(self):
        self.log_file = "chat_logs.json"
        self.csv_file = "chat_logs.csv"
        self.ensure_files_exist()
    
    def ensure_files_exist(self):
        """Create log files if they don't exist"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'account', 'message', 'personality'])
    
    def log_message(self, account_name, message, personality):
        """Log message to JSON and CSV"""
        timestamp = datetime.now().isoformat()
        
        # JSON logging
        log_entry = {
            'timestamp': timestamp,
            'account': account_name,
            'message': message,
            'personality': personality
        }
        
        with open(self.log_file, 'r+') as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=2)
        
        # CSV logging
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, account_name, message, personality])
    
    def get_logs(self, limit=None):
        """Retrieve chat logs"""
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        
        if limit:
            return logs[-limit:]
        return logs