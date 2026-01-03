import requests
import json
from .config import load_config

config = load_config()

def extract_document_data(text, model="llama3.2"):
    prompt = f"""
    Extract the following information from the document text. Output ONLY valid JSON, no other text.

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

    JSON:
    """
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/chat", json=data)
    if response.status_code == 200:
        result = response.json()["message"]["content"]
        try:
            parsed = json.loads(result)
            # Ensure all required keys are present
            required_keys = ['document_type', 'issuer', 'document_date', 'amount_total', 'currency', 'due_date', 'iban', 'invoice_number', 'is_tax_relevant', 'tax_category', 'confidence', 'summary']
            for key in required_keys:
                if key not in parsed:
                    if key == 'summary':
                        parsed[key] = ["Keine Zusammenfassung verfügbar."]
                    elif key == 'confidence':
                        parsed[key] = {}
                    else:
                        parsed[key] = None
            return parsed
        except json.JSONDecodeError:
            # Fallback: return a basic dict if JSON parsing fails
            return {
                "document_type": "Sonstiges",
                "issuer": "Unbekannt",
                "document_date": None,
                "amount_total": None,
                "currency": None,
                "due_date": None,
                "iban": None,
                "invoice_number": None,
                "is_tax_relevant": False,
                "tax_category": None,
                "confidence": {},
                "summary": ["Fehler beim Parsen der Antwort."]
            }
    else:
        raise Exception(f"Ollama error: {response.text}")
