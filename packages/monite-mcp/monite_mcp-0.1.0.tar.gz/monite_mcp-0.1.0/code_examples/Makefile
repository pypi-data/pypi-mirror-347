.PHONY: run-auth-service

run-auth-service:
	@echo "Starting Monite Auth Service using uv..."
	uv run auth_service.py

run-pydantic-ai-agent:
	@echo "Starting Pydantic AI Agent using uv..."
	uv run pydantic_ai_agent.py

run-mcp-use-agent:
	@echo "Starting Monite Auth Service using uv..."
	uv run mcp_use_agent.py

# To run this service, ensure you have a .env file in the directory
# with CLIENT_ID and CLIENT_SECRET defined, or have them set as environment variables.
# Example .env file content:
# CLIENT_ID="your_client_id"
# CLIENT_SECRET="your_client_secret"
# MONITE_API_BASE_URL="https://api.dev.monite.com/v1" # Optional, defaults to sandbox