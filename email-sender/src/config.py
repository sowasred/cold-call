import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SendGrid configuration
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
TEMPLATE_ID = os.getenv('TEMPLATE_ID')
FROM_EMAIL = os.getenv('FROM_EMAIL')

def validate_config():
    """Validate that all required environment variables are set."""
    required_vars = ['SENDGRID_API_KEY', 'TEMPLATE_ID', 'FROM_EMAIL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
