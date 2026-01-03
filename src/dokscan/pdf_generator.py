from fpdf import FPDF
from pypdf import PdfMerger
import os

def create_report_pdf(data, original_path, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Document Report", ln=True, align='C')

    pdf.cell(200, 10, txt="Summary:", ln=True)
    for bullet in data['summary']:
        pdf.cell(200, 10, txt=f"- {bullet}", ln=True)

    pdf.cell(200, 10, txt="Key Data:", ln=True)
    pdf.cell(200, 10, txt=f"Type: {data['document_type']}", ln=True)
    pdf.cell(200, 10, txt=f"Issuer: {data['issuer']}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {data['document_date']}", ln=True)
    pdf.cell(200, 10, txt=f"Amount: {data['amount_total']} {data['currency']}", ln=True)
    pdf.cell(200, 10, txt=f"Due Date: {data['due_date']}", ln=True)
    pdf.cell(200, 10, txt=f"IBAN: {data['iban']}", ln=True)
    pdf.cell(200, 10, txt=f"Invoice Number: {data['invoice_number']}", ln=True)
    pdf.cell(200, 10, txt=f"Tax Relevant: {'Yes' if data['is_tax_relevant'] else 'No'}", ln=True)
    pdf.cell(200, 10, txt=f"Tax Category: {data['tax_category']}", ln=True)

    pdf.cell(200, 10, txt="Original document follows.", ln=True)

    pdf.output(output_path)

    # Append original PDF
    if original_path.endswith('.pdf'):
        merger = PdfMerger()
        merger.append(output_path)
        merger.append(original_path)
        merger.write(output_path)
        merger.close()
    else:
        # For images, convert to PDF - simplified
        pass