import json
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import SENDGRID_API_KEY, TEMPLATE_ID, FROM_EMAIL, validate_config

def load_personalized_data(file_path: str) -> list:
    """Load personalized email data from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def send_email(to_email: str, dynamic_template_data: dict) -> bool:
    """
    Send a personalized email using SendGrid template.
    
    Args:
        to_email: Recipient's email address
        dynamic_template_data: Dictionary containing template variables
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email
    )
    message.template_id = TEMPLATE_ID
    message.dynamic_template_data = dynamic_template_data

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {to_email}. Status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending email to {to_email}: {str(e)}")
        return False

def main():
    """Main function to send personalized emails."""
    # Validate environment variables
    validate_config()
    
    try:
        # Load personalized data
        data = load_personalized_data('personalized_email.json')
        
        # Send emails
        for item in data:
            to_email = item.pop('email')  # Remove email from template data
            success = send_email(to_email, item)
            if not success:
                print(f"Failed to send email to {to_email}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
