import requests
from fastapi import APIRouter, Request
from msal import ConfidentialClientApplication

from .config import settings

router = APIRouter()

# Initialize client for Azure AD authentication
client = ConfidentialClientApplication(
    settings.AZURE_CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}",
    client_credential=settings.AZURE_CLIENT_SECRET
)

# Temporary storage for auth flows (replace with a secure method in production)
auth_flows = {}


@router.get("/login")
async def login():
    # Initiate the authentication code flow
    auth_flow = client.initiate_auth_code_flow(
        ["User.Read"],
        redirect_uri=settings.REDIRECT_URI
    )

    # Store the flow with a unique identifier (e.g., session ID or user ID)
    auth_flows["user_id"] = auth_flow  # Replace "user_id" with an actual unique identifier

    # Return the authorization URL to redirect the user to the Azure login page
    return {"auth_url": auth_flow["auth_uri"]}


@router.get("/callback")
async def auth_callback(request: Request):
    # Retrieve the auth flow state using the unique identifier (replace 'user_id' in production)
    auth_flow = auth_flows.get("user_id")  # Replace "user_id" with the actual unique identifier

    if not auth_flow:
        # raise HTTPException(status_code=400, detail="Invalid or expired authorization flow")
        return {"message": "ACCESS DENIED"}

    # Acquire the token using the stored flow and the provided authorization code
    result = client.acquire_token_by_auth_code_flow(auth_flow, dict(request.query_params))

    # Check if the token acquisition was successful
    if "access_token" in result:
        access_token = result["access_token"]

        # Call Microsoft Graph to get user profile details
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

        user_info = None
        if user_info_response.status_code == 200:
            user_info = user_info_response.json()
            user_name = user_info.get("displayName", "User")
            return {"message": f"Hello, {user_name}"}
        else:
            return {"message": {user_info}}
    else:
        return {"message": "ACCESS DENIED"}
