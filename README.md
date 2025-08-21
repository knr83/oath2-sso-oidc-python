🔐 Azure AD OAuth2/OIDC FastAPI Demo
===================================

Minimal FastAPI service that demonstrates user sign‑in with Azure Active Directory (MSAL) and a call to Microsoft Graph
`/v1.0/me`.

⚙️ Features
----------

- OAuth2 Authorization Code Flow via MSAL (Confidential Client)
- Fetch basic user profile from Microsoft Graph
- CORS configured via environment variable `ALLOWED_ORIGINS`

📦 Requirements
---------------

- Python 3.11+
- Azure AD App Registration with a client secret

🔧 Azure setup
-------------

1. Create an App Registration (type: Web) in Azure AD.
2. Add Redirect URI: `http://localhost:8000/auth/callback`.
3. Add Microsoft Graph delegated permission: `User.Read` (grant admin consent if required).
4. Create a client secret and copy its Value.

🧩 Environment
-------------
Create a `.env` file in the project root:

```
AZURE_CLIENT_ID=your-app-client-id
AZURE_CLIENT_SECRET=your-app-client-secret
AZURE_TENANT_ID=your-tenant-id
REDIRECT_URI=http://localhost:8000/auth/callback
ALLOWED_ORIGINS=http://localhost:4200
```

🛠️ Setup
--------
Windows PowerShell:

```
python -m venv .venv
 .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS/Linux:

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

▶️ Run
------

```
uvicorn app.main:app --reload
```

Open API docs: http://localhost:8000/docs

📚 Endpoints
-----------

- `GET /auth/login` – starts the Azure AD login flow and returns an `auth_url` for redirect.
- `GET /auth/callback` – handles redirect from Azure AD, exchanges code for token, then calls Graph `/me` and returns a
  greeting.
- `GET /test` – simple CORS check endpoint.

🧪 How to test the flow
----------------------

1) Start the app and open `http://localhost:8000/docs`.
2) Call `GET /auth/login` (or via browser) and copy the `auth_url`.
3) Open the `auth_url` in the browser, sign in/consent.
4) Azure redirects to `/auth/callback` and the API returns a short greeting.

🧭 Auth Flow (high level)
------------------------

1) Client hits `/auth/login` and is redirected to Azure AD authorization page.
2) After consent/sign‑in, Azure AD redirects to `REDIRECT_URI` (`/auth/callback`).
3) Backend exchanges the authorization code for an access token via MSAL.
4) Backend calls Microsoft Graph `/v1.0/me` and returns a short response with the display name.

⚠️ Notes & Limitations
----------------------

- This is a learning/demo project. Authorization flow state is stored in memory and not suitable for production.
- Network call to Graph uses a small timeout and basic error handling.
- Keep secrets out of version control. Use environment variables/secret managers in real deployments.

🩺 Troubleshooting
-----------------

- Error about missing env vars: check `.env` values and names.
- 400 at callback: ensure `REDIRECT_URI` in Azure App matches exactly.
- CORS errors in browser: update `ALLOWED_ORIGINS` to include your frontend origin.


