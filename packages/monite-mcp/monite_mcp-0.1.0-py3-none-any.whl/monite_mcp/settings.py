import os

USER_AGENT = "monite-mcp/0.1"
MONITE_API_VERSION = "2024-05-25"

MONITE_AI_API_BASE = os.getenv(
    "MONITE_AI_API_BASE", "https://api.sandbox.monite.com/v1/mcp"
)

ENTITY_USER_ID = os.getenv("ENTITY_USER_ID")
if not ENTITY_USER_ID:
    raise SystemExit(
        "ENTITY_USER_ID environment variable is not set. "
        "It is required to run the Monite MCP server."
    )

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
if not AUTH_SERVICE_URL:
    raise SystemExit(
        "AUTH_SERVICE_URL environment variable is not set. "
        "It is required to run the Monite MCP server."
    )
