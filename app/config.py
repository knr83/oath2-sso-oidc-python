import os
import re

from dotenv import load_dotenv

load_dotenv()

# Environment variables (Azure AD):
# AZURE_CLIENT_ID   – Application (client) ID from Azure App Registration.
# AZURE_CLIENT_SECRET – App client secret (Certificates & secrets → New client secret → Value).
# AZURE_TENANT_ID   – Directory (tenant) ID of your Azure AD.
# REDIRECT_URI      – Redirect URI configured in App Registration (must match exactly).
# ALLOWED_ORIGINS   – CORS origins list (comma/space separated), e.g. http://localhost:4200


class Settings:
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    ALLOWED_ORIGINS = [
        o
        for o in re.split(
            r"[,\s]+", (os.getenv("ALLOWED_ORIGINS", "http://localhost:4200") or "").strip()
        )
        if o
    ]

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
