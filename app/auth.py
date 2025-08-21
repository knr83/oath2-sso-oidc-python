import requests
from fastapi import APIRouter, Request, HTTPException, status
from msal import ConfidentialClientApplication

from app.config import settings

router = APIRouter()

# Initialize client for Azure AD authentication
client = ConfidentialClientApplication(
    settings.AZURE_CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}",
    client_credential=settings.AZURE_CLIENT_SECRET
)

# Temporary in-memory storage for authorization flows (demo only)
auth_flows = {}


@router.get("/login")
async def login() -> dict:
    auth_flow = client.initiate_auth_code_flow(
        ["User.Read"],
        redirect_uri=settings.REDIRECT_URI
    )

    # Store the flow (use a real user/session ID in production)
    auth_flows["user_id"] = auth_flow

    return {"auth_url": auth_flow["auth_uri"]}


@router.get("/callback")
async def auth_callback(request: Request) -> dict:
    auth_flow = auth_flows.get("user_id")

    if not auth_flow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired authorization flow",
        )

    params = dict(request.query_params)
    result = client.acquire_token_by_auth_code_flow(auth_flow, params)

    # Handle token acquisition errors from MSAL
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error_description") or "Authorization failed",
        )

    if "access_token" in result:
        access_token = result["access_token"]

        # Fetch basic user profile from Microsoft Graph
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            user_info_response = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers=headers,
                timeout=5,
            )
        except requests.RequestException:
            raise HTTPException(status_code=502, detail="Graph request failed")

        user_info = None
        if user_info_response.status_code == 200:
            user_info = user_info_response.json()
            user_name = user_info.get("displayName", "User")
            return {"message": f"Hello, {user_name}"}
        else:
            raise HTTPException(
                status_code=user_info_response.status_code,
                detail="Failed to fetch user profile from Microsoft Graph",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to acquire access token",
        )
