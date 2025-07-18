"""
EMAIL CLIENT COMPONENT
Communicates with email server to send messages
Handles all client-side email operations
"""

import socket
import json
import getpass

class EmailClient:
    """
    Client that:
    - Connects to email server
    - Formats requests as JSON
    - Handles server responses
    """
    
    def __init__(self, server_host='localhost', server_port=5000):
        """Initialize with server connection details"""
        self.server_host = server_host  # Matches server's host
        self.server_port = server_port  # Matches server's port

    def send_email(self, sender_email, sender_password, recipient_email, subject, body, attachment_path=None):
        """
        Sends email by:
        1. Creating request dictionary
        2. Converting to JSON
        3. Sending to server
        4. Returning response
        """
        try:
            # Build complete request object
            request = {
                'sender_email': sender_email,
                'sender_password': sender_password,
                'recipient_email': recipient_email,
                'subject': subject,
                'body': body,
                'attachment_path': attachment_path  # None if no attachment
            }

            # Network communication
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.server_host, self.server_port))
                s.sendall(json.dumps(request).encode())  # Send JSON
                response = s.recv(1024).decode()  # Get response
                return response
        except Exception as e:
            return f"Error: {str(e)}"  # Return any errors

def start_email_service(pdf_generator_func, hr_email):
    """
    Automated email service that:
    - Uses fixed sender credentials
    - Generates PDF reports
    - Sends them periodically
    """
    # Fixed credentials (would be environment variables in production)
    sender_email = "*****@gmail.com"
    sender_password = "*****"  # App-specific password
    
    client = EmailClient()  # Initialize client
    
    while True:  # Continuous operation
        # Generate new report
        pdf_path = pdf_generator_func()  # Get fresh PDF
        
        # Email details
        subject = "Employee Performance Report"
        body = "Please find attached the latest employee performance report."
        
        # Send and get response
        response = client.send_email(
            sender_email,
            sender_password,
            hr_email,
            subject,
            body,
            pdf_path  # Attach generated PDF
        )
        
        print(f"Email sent to {hr_email}. Server response: {response}")
