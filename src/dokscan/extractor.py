import pdfplumber
import pytesseract
from PIL import Image
import io
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_image(image_path, config="--psm 6"):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, config=config)
    return text

def get_text_from_file(file_path, tesseract_config="--psm 6"):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        text = extract_text_from_pdf(file_path)
        if len(text.strip()) < 100:  # Fallback to OCR if little text
            # Convert PDF pages to images and OCR
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    img = page.to_image(resolution=300).original
                    text += pytesseract.image_to_string(img, config=tesseract_config) + "\n"
    elif ext in ['.jpg', '.jpeg', '.png', '.tiff']:
        text = extract_text_from_image(file_path, tesseract_config)
    else:
        raise ValueError("Unsupported file type")
    return text