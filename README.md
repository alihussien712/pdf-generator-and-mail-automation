# pdf-generator-and-mail-automation
A Python-based system for generating employee performance reports as PDFs and sending them via email.  Includes a modular design with separate components for PDF generation, email server/client communication,  and user interaction. Requires SMTP credentials (Gmail) for email functionality.
# Employee Report Automation System

![Python](https://img.shields.io/badge/python-3.8%2B-blue)

Automates the generation and email delivery of employee performance reports as PDFs.

## Features
- **PDF Generation**: Creates standardized reports with dynamic headers/footers.
- **Email Server**: SMTP-based server (runs on port 5000) for secure email handling.
- **Validation**: Strict email format verification for recipients.
- **Modular Design**: Separated into `pdf_generator`, `email_server`, and `client` components.

## Prerequisites
- Python 3.8+
- Gmail SMTP credentials (for email functionality)
- Libraries: `fpdf`, `smtplib`, `ssl`

