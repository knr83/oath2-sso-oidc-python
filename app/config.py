import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    REDIRECT_URI = os.getenv("REDIRECT_URI")

    # Method to validate the presence of all required environment variables
    @classmethod
    def validate(cls):
        missing = [
            var_name for var_name, var_value in vars(cls).items()
            if var_name.isupper() and var_value is None
        ]
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")


# Create an instance of settings
settings = Settings()

# Validate environment variables
settings.validate()
