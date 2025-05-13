import logging
import os
from uuid import UUID

import dotenv
import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

# ##############################################################################
# IMPORTANT SECURITY DISCLAIMER:
# This script (`auth_service.py`) is provided as a simplified example
# for demonstration purposes only.
#
# In a real-world/production scenario, this authentication service MUST NOT
# be exposed publicly as is. Doing so could lead to critical security
# vulnerabilities. An attacker who can guess or obtain an `entity_user_id`
# could potentially gain unauthorized access by retrieving authentication tokens.
#
# A production-ready authentication service should:
# 1. Run in a private network or a securely restricted environment.
# 2. Implement robust authentication and authorization mechanisms beyond
#    just an `entity_user_id` to protect the token issuance endpoint.
# 3. Implement token caching mechanisms that respect token lifecycles
#    to reduce load on the Monite API and improve performance.
# 4. Have comprehensive logging, monitoring, and rate-limiting in place.
#
# Please ensure you understand these risks before deploying/using
# this exampple of authentication service.
# ##############################################################################

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
MONITE_API_BASE_URL = os.getenv("MONITE_API_BASE_URL", "https://api.dev.monite.com/v1")


if not CLIENT_ID:
    raise SystemExit("CLIENT_ID environment variable is not set.")
if not CLIENT_SECRET:
    raise SystemExit("CLIENT_SECRET environment variable is not set.")


app = FastAPI(
    title="Monite Auth Service",
    description="Provides Monite entity_user tokens using client credentials and entity_user_id.",
    version="0.1.0",
)


class MoniteAuthToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


async def fetch_monite_entity_user_token(entity_user_id: UUID) -> MoniteAuthToken:
    """
    Fetches an entity user token from the Monite API using the
    CLIENT_ID and CLIENT_SECRET.
    """

    token_url = f"{MONITE_API_BASE_URL}/auth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "entity_user_id": str(entity_user_id),
        "grant_type": "entity_user",
    }

    async with httpx.AsyncClient() as client:
        try:
            logger.info(
                f"Requesting entity_user token for {entity_user_id} from {token_url}"
            )
            response = await client.post(token_url, json=payload, timeout=10)
            response.raise_for_status()
        except httpx.RequestError as exc:
            logger.error(
                f"HTTP request failed when contacting Monite for {entity_user_id}: {exc}"
            )
            raise HTTPException(
                status_code=503,
                detail=f"Error connecting to Monite API: {exc}",
            )
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Monite API returned an error for {entity_user_id}: {exc.response.status_code} - {exc.response.text}"
            )
            detail = f"Monite API error: {exc.response.status_code}"
            try:
                error_details = exc.response.json()
                detail += f" - {error_details}"
            except Exception:
                detail += f" - {exc.response.text}"
            raise HTTPException(status_code=exc.response.status_code, detail=detail)

    response_json = response.json()
    logger.info(f"Successfully obtained token for entity_user_id: {entity_user_id}")
    return MoniteAuthToken(
        access_token=response_json["access_token"],
        token_type=response_json["token_type"],
        expires_in=response_json.get("expires_in"),
    )


@app.get(
    "/token",
    summary="Get Monite Entity User Token",
    response_model=MoniteAuthToken,
    description="Fetches an entity_user token from Monite for the specified entity_user_id. ",
)
async def get_token_endpoint(
    entity_user_id: UUID = Query(
        ...,
        description="The ID of the Entity User for whom the token is being generated.",
    ),
):
    try:
        token_data = await fetch_monite_entity_user_token(entity_user_id)
        return token_data
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        logger.exception(
            f"Unexpected error while processing token request for {entity_user_id}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error.")


if __name__ == "__main__":
    logger.info(
        f"Starting Monite Auth Service for Monite Environment: {MONITE_API_BASE_URL}"
    )
    uvicorn.run(app, host="0.0.0.0", port=8888)
