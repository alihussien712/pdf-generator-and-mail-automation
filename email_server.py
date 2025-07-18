"""
EMAIL SERVER (Must run FIRST)
Handles all email sending operations via SMTP
Listens on port 5000 for client requests
"""
import smtplib
import socket
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EmailServer:
    def __init__(self, host='0.0.0.0', port=5000):  # Changed to 0.0.0.0 for broader access
        self.host = host
        self.port = port
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.context = ssl.create_default_context()
        self.running = False

    def _send_email(self, sender_email, sender_password, recipient_email, subject, body, attachment_path):
        """Handles the actual email sending logic"""
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            if attachment_path:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={attachment_path}",
                )
                msg.attach(part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=self.context)
                server.login(sender_email, sender_password)
                server.send_message(msg)
            return True, "Email sent successfully"
        except Exception as e:
            return False, f"SMTP Error: {str(e)}"

    def start(self):
        """Main server loop with enhanced error handling"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
            try:
                s.bind((self.host, self.port))
                s.listen()
                self.running = True
                logging.info(f"Server started on {self.host}:{self.port}")

                while self.running:
                    try:
                        conn, addr = s.accept()
                        with conn:
                            logging.info(f"Connection from {addr}")
                            data = conn.recv(1024).decode()
                            if not data:
                                continue

                            try:
                                request = json.loads(data)
                                success, message = self._send_email(
                                    request['sender_email'],
                                    request['sender_password'],
                                    request['recipient_email'],
                                    request['subject'],
                                    request['body'],
                                    request.get('attachment_path')
                                )
                                response = {"success": success, "message": message}
                                conn.sendall(json.dumps(response).encode())
                            except json.JSONDecodeError:
                                conn.sendall(json.dumps({
                                    "success": False,
                                    "message": "Invalid JSON format"
                                }).encode())
                    except ConnectionAbortedError:
                        logging.warning("Client connection aborted")
                    except Exception as e:
                        logging.error(f"Connection error: {str(e)}")
            except Exception as e:
                logging.critical(f"Server failed: {str(e)}")
            finally:
                self.running = False
                logging.info("Server stopped")

if __name__ == "__main__":
    server = EmailServer()
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("Server shutdown by user")
