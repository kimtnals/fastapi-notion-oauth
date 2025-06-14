from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic_settings import BaseSettings
from pydantic import Field
from urllib.parse import urlencode
from uuid import uuid4
import httpx
import logging

# Logging Configuration 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use Pydantic BaseSettings to load and validate environment variables with type hints.
class Settings(BaseSettings):
    CLIENT_ID: str = Field(validation_alias="NOTION_CLIENT_ID")
    CLIENT_SECRET: str = Field(validation_alias="NOTION_CLIENT_SECRET")
    REDIRECT_URI: str = Field(validation_alias="NOTION_REDIRECT_URI")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()
app = FastAPI()

# Root: Redirect user to Notion login page upon access
@app.get("/")
async def start_oauth() -> RedirectResponse:
    state = str(uuid4())
    query = urlencode({
        "client_id": settings.CLIENT_ID,
        "response_type": "code",
        "owner": "workspace",
        "redirect_uri": settings.REDIRECT_URI,
        "state": state,
    })

    # Create redirect response
    redirect_url = f"https://api.notion.com/v1/oauth/authorize?{query}"
    response = RedirectResponse(url=redirect_url)

    # Store state in cookie (enhanced security settings)
    response.set_cookie(
        key="oauth_state",      # Name of the cookie (stores the OAuth state value)
        value=state,            # The random state value used to prevent CSRF attacks
        httponly=True,          # Prevents JavaScript access to the cookie (helps mitigate XSS)
        secure=False,           # Set to True in production to ensure cookie is sent only over HTTPS
        samesite="lax",         # Restricts cross-site requests to prevent CSRF attacks
        max_age=300             # Expiration time of the cookie in seconds (here, 5 minutes)
    )
    logger.info("OAuth process started")
    return response


# Callback: Request access_token using code after login redirection
@app.get("/callback")
async def notion_callback(request: Request, code: str, state: str, response: Response):
    stored_state = request.cookies.get("oauth_state")

    if not stored_state or stored_state != state:
        logger.warning("Invalid state detected - possible CSRF attack")
        raise HTTPException(status_code=400, detail="Invalid state. Possible CSRF attack.")
    
    # Delete state cookie after use to prevent reuse or CSRF risk
    response.delete_cookie("oauth_state")

    token_url = "https://api.notion.com/v1/oauth/token"
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            token_url,
            auth=(settings.CLIENT_ID, settings.CLIENT_SECRET),
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.REDIRECT_URI
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Notion-Version": "2022-06-28"
            }
        )

        if token_response.status_code != 200:
            logger.error(f"Failed to get access token from Notion API. Status: {token_response.status_code}")
            raise HTTPException(status_code=500, detail=f"Failed to get access token from Notion API.")

        data = token_response.json()
        access_token = data.get("access_token")
        logger.info("User logged in successfully")

        # Exposing access_token directly is a security risk.
        # Store it securely and avoid sending it to the client directly in production.
        return JSONResponse(content={"access_token": access_token})
