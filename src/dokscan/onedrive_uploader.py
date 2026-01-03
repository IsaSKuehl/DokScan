from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
import os
import asyncio

async def upload_to_onedrive(file_path, data, config):
    credential = DeviceCodeCredential(
        client_id=config['graph_client_id'],
        tenant_id=config['graph_tenant_id']
    )
    scopes = ['Files.ReadWrite']
    client = GraphServiceClient(credential, scopes)

    year = data['document_date'][:4] if data['document_date'] else datetime.now().year
    month = data['document_date'][5:7] if data['document_date'] else datetime.now().month
    folder_path = f"{config['onedrive_root']}/{data['document_type']}/{year}/{month:02d}"

    # Create folder if not exists
    await client.me.drive.root.item_with_path(folder_path).request().mkdir()

    with open(file_path, 'rb') as f:
        content = f.read()

    filename = os.path.basename(file_path)
    await client.me.drive.root.item_with_path(f"{folder_path}/{filename}").content.request().upload(content)