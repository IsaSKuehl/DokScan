import pytest
from dokscan.extractor import extract_text_from_pdf
import os

def test_extract_text():
    # Mock or use sample
    # Assuming sample.pdf exists
    if os.path.exists('sample_docs/sample.pdf'):
        text = extract_text_from_pdf('sample_docs/sample.pdf')
        assert isinstance(text, str)