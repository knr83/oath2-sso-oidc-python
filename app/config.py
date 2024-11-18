import json
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configuration from JSON file
def load_config(config_file='config.json'):
    if os.path.isfile(config_file):
        with open('config.json') as config_file:
            config = json.load(config_file)
            print("Configuration loaded")
            return config
    else:
        raise ValueError(f"Configuration not found: config.json")

class Settings:
    # AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    # AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    # AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    # REDIRECT_URI = os.getenv("REDIRECT_URI")
    config = load_config()
    AZURE_CLIENT_ID = config['azure_client_id']
    AZURE_CLIENT_SECRET = config['azure_client_secret']
    AZURE_TENANT_ID = config['azure_tenant_id']
    REDIRECT_URI = config['redirect_uri']

    # Method to validate the presence of all required environment variables
    @classmethod
    def validate(cls):
        missing = [
            var_name for var_name, var_value in vars(cls).items()
            if var_name.isupper() and var_value is None
        ]
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")

settings = Settings()
settings.validate()
