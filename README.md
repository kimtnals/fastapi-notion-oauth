# Notion OAuth FastAPI Example
This is a simple FastAPI application demonstrating OAuth 2.0 login flow.

## Features
- Redirects users to Notion login page for OAuth authorization
- Handles OAuth callback and exchanges authorization code for access token
- Basic CSRF protection using state parameter stored in a cookie
- Logs key events for monitoring

## Installation
**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/notion-oauth-fastapi.git
cd notion-oauth-fastapi
```

**2. Create and activate virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file in the project root with your Notion OAuth credentials:**
```env
NOTION_CLIENT_ID=your_client_id
NOTION_CLIENT_SECRET=your_client_secret
NOTION_REDIRECT_URI=http://localhost:8000/callback
```

## Running the app
```bash
uvicorn oauth_server:app --reload
```
Access `http://localhost:8000/` in your browser to start the OAuth flow.

## Notes
- The cookie for state is set with secure=False for local development. Change it to True in production (HTTPS required).
- This example returns the access token in JSON response for demonstration only. Do not expose access tokens in production.
- Add your own token storage and user session management as needed.
