import openai
import json
from .config import load_config

config = load_config()

client = openai.OpenAI(api_key=config['openai_api_key'])

def extract_document_data(text, model="gpt-4"):
    prompt = f"""
    Extract the following information from the document text. Output as JSON.

    Document types: Steuerbescheid, Handwerkerrechnung, Versicherung, Mahnung, Vertrag, Sonstiges

    Fields:
    - document_type: string (one of the above)
    - issuer: string
    - document_date: string (YYYY-MM-DD)
    - amount_total: float or null
    - currency: string or null
    - due_date: string (YYYY-MM-DD) or null
    - iban: string or null
    - invoice_number: string or null
    - is_tax_relevant: boolean
    - tax_category: string (Einkommensteuer, Werbungskosten, Haushaltnahe DL, Betriebsausgabe, Sonstiges) or null
    - confidence: dict with keys for each field, values 0-1
    - summary: list of up to 8 bullet points

    Text: {text[:4000]}  # Limit text length
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    result = response.choices[0].message.content
    return json.loads(result)