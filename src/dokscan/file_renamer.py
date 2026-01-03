import re
import os
from datetime import datetime

def sanitize_filename(name):
    return re.sub(r'[^\w\-_\.]', '_', name)

def generate_filename(data, original_ext):
    date = data['document_date'] or datetime.now().strftime('%Y-%m-%d')
    doc_type = sanitize_filename(data['document_type'])
    sender = sanitize_filename(data['issuer'][:20])
    amount = f"{data['amount_total']:.2f}" if data['amount_total'] else '0.00'
    due = data['due_date'] or ''
    tax = 'Y' if data['is_tax_relevant'] else 'N'
    filename = f"{date}__{doc_type}__{sender}__{amount}__faellig_{due}__tax_{tax}.pdf"
    return filename[:100]  # Limit length

def rename_file(original_path, data):
    dir_path = os.path.dirname(original_path)
    new_name = generate_filename(data, os.path.splitext(original_path)[1])
    new_path = os.path.join(dir_path, new_name)
    # Handle collisions
    counter = 1
    while os.path.exists(new_path):
        base, ext = os.path.splitext(new_name)
        new_path = os.path.join(dir_path, f"{base}__v{counter}{ext}")
        counter += 1
    os.rename(original_path, new_path)
    return new_path