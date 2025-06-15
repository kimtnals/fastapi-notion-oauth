# Notion OAuth FastAPI Example
This is a simple FastAPI application demonstrating OAuth 2.0 login flow.

## Features
- Redirects users to Notion login page for OAuth authorization
- Handles OAuth callback and exchanges authorization code for access token
- Basic CSRF protection using state parameter stored in a cookie
- Logs key events for monitoring

## Installation
**1. Create OAuth integration in Notion**
1. Visit [Notion Integrations page](https://www.notion.so/profile/integrations).
2. Click **"Create new integration"**.
3. Fill in the integration name and other required info.
4. Set the **Redirect URI** to `http://localhost:8000/callback` (this must match your `.env` setting).
5. After creation, copy the **Client ID** and **Client Secret**.


**2. Clone the repository:**
```bash
git clone https://github.com/yourusername/notion-oauth-fastapi.git
cd notion-oauth-fastapi
```

**3. Create and activate virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

**4. Install dependencies:**
```bash
pip install -r requirements.txt
```

**5. Create a `.env` file in the project root with your Notion OAuth credentials:**
```env
NOTION_CLIENT_ID=your_client_id
NOTION_CLIENT_SECRET=your_client_secret
NOTION_REDIRECT_URI=http://localhost:8000/callback
```

## Running the app
```bash
uvicorn oauth_server:app --host localhost --reload
```
Access `http://localhost:8000/` in your browser to start the OAuth flow.

## Notes
- The cookie for state is set with secure=False for local development. Change it to True in production (HTTPS required).
- This example returns the access token in JSON response for demonstration only. Do not expose access tokens in production.
- Add your own token storage and user session management as needed.
