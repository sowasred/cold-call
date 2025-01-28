import json
import os
import pandas as pd
import sendgrid
from sendgrid.helpers.mail import Mail
from config import SENDGRID_API_KEY, TEMPLATE_ID, FROM_EMAIL, validate_config

def get_sent_emails_file() -> str:
    """Get the path to the sent emails tracking file."""
    sent_emails_dir = "sent-emails"
    if not os.path.exists(sent_emails_dir):
        os.makedirs(sent_emails_dir)
    return os.path.join(sent_emails_dir, f"{FROM_EMAIL.replace('@', '_')}.json")

def load_sent_emails() -> set:
    """Load the set of already sent email addresses."""
    sent_emails_file = get_sent_emails_file()
    if os.path.exists(sent_emails_file):
        try:
            with open(sent_emails_file, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            return set()
    return set()

def save_sent_email(email: str):
    """Save a sent email address to the tracking file."""
    sent_emails = load_sent_emails()
    sent_emails.add(email)
    sent_emails_file = get_sent_emails_file()
    with open(sent_emails_file, 'w') as f:
        json.dump(list(sent_emails), f)

def load_personalized_data(file_path: str) -> list:
    """Load personalized email data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            print(f"Loading data from {file_path}")
            data = json.load(f)
            print(f"Successfully loaded data: {data}")
            return data['emails']
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {str(e)}")
        raise
    except Exception as e:
        print(f"Error loading file {file_path}: {str(e)}")
        raise

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
    message.dynamic_template_data = {
        'subject': dynamic_template_data['subject_line'],
        'email_body': dynamic_template_data['email_body'],
        'company_name': dynamic_template_data['company_name'],
    }

    try:
        sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if response.status_code == 202:
            save_sent_email(to_email)
        return response.status_code

    except Exception as e:
        print(str(e))
        return str(e)

def main():
    """Main function to send personalized emails."""
    # Validate environment variables
    validate_config()
    
    try:
        # Load personalized data
        data = load_personalized_data('personalized_email.json')
        sent_emails = load_sent_emails()
        
        # Send emails only to new recipients
        for item in data:
            to_email = item.pop('company_email')  # Remove email from template data
            if to_email not in sent_emails:
                success = send_email(to_email, item)
                if not success:
                    print(f"Failed to send email to {to_email}")
            else:
                print(f"Email already sent to {to_email}, skipping...")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
