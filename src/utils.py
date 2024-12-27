import json
import logging

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def setup_logger(log_file):
    """Setup logger for logging events."""
    logging.basicConfig(
        filename=log_file,
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    return logging.getLogger()
