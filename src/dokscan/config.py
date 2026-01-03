import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_config():
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    config['openai_api_key'] = os.getenv('OPENAI_API_KEY')
    if config.get('enable_microsoft_integration', False):
        config['graph_client_id'] = os.getenv('GRAPH_CLIENT_ID')
        config['graph_tenant_id'] = os.getenv('GRAPH_TENANT_ID')
    return config