from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from datetime import datetime, timedelta
import asyncio

async def create_calendar_event(data, config):
    if not data['due_date'] or not data['amount_total']:
        return

    credential = DeviceCodeCredential(
        client_id=config['graph_client_id'],
        tenant_id=config['graph_tenant_id']
    )
    scopes = ['Calendars.ReadWrite']
    client = GraphServiceClient(credential, scopes)

    due_date = datetime.fromisoformat(data['due_date'])
    event = {
        "subject": f"Zahlung: {data['issuer']} - {data['amount_total']} {data['currency']} ({data['document_type']})",
        "start": {
            "dateTime": due_date.replace(hour=9).isoformat(),
            "timeZone": "Europe/Berlin"
        },
        "end": {
            "dateTime": (due_date.replace(hour=9) + timedelta(hours=1)).isoformat(),
            "timeZone": "Europe/Berlin"
        },
        "body": {
            "content": f"IBAN: {data['iban']}\nReferenz: {data['invoice_number']}\nZusammenfassung: {'; '.join(data['summary'])}",
            "contentType": "text"
        }
    }

    await client.me.events.post(event)