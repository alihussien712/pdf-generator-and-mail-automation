"""
MAIN APPLICATION (Run SECOND)
Handles user interaction and workflow
"""
from pdf_generator import generate_report
from email_sender import start_email_service
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_email(email):
    """Strict email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def get_hr_email():
    """Interactive email collection with validation"""
    while True:
        print("\n" + "="*40)
        email = input("Enter HR email address to receive reports: ").strip()
        
        if not validate_email(email):
            logging.error("Invalid email format")
            continue
            
        confirm = input(f"Confirm sending reports to {email}? (y/n): ").lower()
        if confirm == 'y':
            return email
        logging.warning("Email not confirmed")

if __name__ == "__main__":
    try:
        print("\n" + "="*40)
        print("  EMPLOYEE REPORT AUTOMATION SYSTEM")
        print("="*40)
        print("NOTE: You must run email_server.py FIRST in another terminal")
        print("="*40)
        
        hr_email = get_hr_email()
        logging.info(f"Starting service for {hr_email}")
        start_email_service(generate_report, hr_email)
        
    except KeyboardInterrupt:
        logging.info("Application stopped by user")
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}")