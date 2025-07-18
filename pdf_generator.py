"""
PDF GENERATOR (Unchanged)
Creates standardized employee reports
"""
from fpdf import FPDF
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

LOGO_PATH = r"C:\Users\Msi\Desktop\Employee_Report_2\logo.png"
OUTPUT_PDF = "Employee_Performance_Report.pdf"

class PDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, x=10, y=10, w=30)
            
        self.set_font("Helvetica", "I", 10)
        self.set_xy(150, 10)
        self.cell(0, 10, f"Generated: {datetime.now().strftime('%d %b %Y')}", align="R")
        
        self.set_xy(0, 30)
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "EMPLOYEE PERFORMANCE REPORT", ln=True, align="C")
    
    def footer(self):
        self.set_draw_color(150, 150, 150)
        self.rect(5, 5, 200, 285)

def generate_report():
    try:
        pdf = PDF()
        pdf.add_page()
        pdf.set_y(50)
        pdf.output(OUTPUT_PDF)
        logging.info(f"Generated report: {OUTPUT_PDF}")
        return OUTPUT_PDF
    except Exception as e:
        logging.error(f"PDF generation failed: {str(e)}")
        raise

if __name__ == "__main__":
    generate_report()
