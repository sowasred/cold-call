import json
import logging
from datetime import datetime

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def setup_logger(log_dir):
    """Setup logger with both latest and timestamped log files."""
    # Create timestamp string
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Define log files
    latest_log = f"{log_dir}/latest.log"
    timestamped_log = f"{log_dir}/scraper_{timestamp}.log"
    
    # Configure logging to write to both files
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Handler for timestamped log
    timestamp_handler = logging.FileHandler(timestamped_log)
    timestamp_handler.setFormatter(formatter)
    logger.addHandler(timestamp_handler)
    
    # Handler for latest log (overwrite mode)
    latest_handler = logging.FileHandler(latest_log, mode='w')
    latest_handler.setFormatter(formatter)
    logger.addHandler(latest_handler)
    
    return logger
