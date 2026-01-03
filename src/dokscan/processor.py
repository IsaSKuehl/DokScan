import os
import shutil
import logging
from .extractor import get_text_from_file
from .llm_processor import extract_document_data
from .pdf_generator import create_report_pdf
from .file_renamer import rename_file
from .calendar_integrator import create_calendar_event
from .onedrive_uploader import upload_to_onedrive
import asyncio

logger = logging.getLogger(__name__)

async def process_file(file_path, config):
    try:
        # Extract text
        text = get_text_from_file(file_path, config['tesseract_config'])

        # LLM extraction
        if config['datenschutz_modus'] == 'cloud':
            data = extract_document_data(text, config['openai_model'])
        else:
            # Local fallback - simplified, no LLM
            data = {
                'document_type': 'Sonstiges',
                'issuer': 'Unknown',
                'document_date': None,
                'amount_total': None,
                'currency': None,
                'due_date': None,
                'iban': None,
                'invoice_number': None,
                'is_tax_relevant': False,
                'tax_category': None,
                'confidence': {},
                'summary': ['Local mode: No extraction']
            }

        # Create report PDF
        report_path = file_path.replace(os.path.splitext(file_path)[1], '_report.pdf')
        create_report_pdf(data, file_path, report_path)

        # Rename
        renamed_path = rename_file(report_path, data)

        # Calendar
        if config.get('enable_microsoft_integration', False):
            await create_calendar_event(data, config)

        # OneDrive
        if config.get('enable_microsoft_integration', False):
            await upload_to_onedrive(renamed_path, data, config)

        # Move to processed
        shutil.move(renamed_path, config['processed_path'])

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        try:
            shutil.move(file_path, config['failed_path'])
        except PermissionError:
            logger.warning(f"Could not move {file_path} to failed folder due to permission error")