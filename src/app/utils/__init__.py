# This file makes the directory a Python package

from datetime import datetime
from flask import current_app
import os
import logging

# Configure logger
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(console_handler)

def log_activity(action, filename):
    """Log user activity"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {action}: {filename}\n"
    log_file = os.path.join(current_app.config['LOG_FOLDER'], 'activity.log')
    with open(log_file, 'a') as f:
        f.write(log_entry)

def generate_document_number(sequence):
    """Generate a unique document number"""
    return f"{sequence:04d}"

def validate_file(filename):
    """Validate file extension"""
    allowed_extensions = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
