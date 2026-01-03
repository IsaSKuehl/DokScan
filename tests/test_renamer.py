import pytest
from dokscan.file_renamer import generate_filename, sanitize_filename

def test_sanitize_filename():
    assert sanitize_filename("Test: File.pdf") == "Test__File.pdf"

def test_generate_filename():
    data = {
        'document_type': 'Rechnung',
        'issuer': 'Firma GmbH',
        'document_date': '2023-10-01',
        'amount_total': 100.50,
        'due_date': '2023-10-15',
        'is_tax_relevant': True
    }
    filename = generate_filename(data, '.pdf')
    assert '2023-10-01__Rechnung__Firma_GmbH__100.50__faellig_2023-10-15__tax_Y.pdf' in filename