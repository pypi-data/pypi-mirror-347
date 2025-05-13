import asyncio
import os
from logging import getLogger

import dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

logger = getLogger(__name__)

dotenv.load_dotenv()

ENTITY_USER_ID = os.getenv("ENTITY_USER_ID", "1e6a8edf-065d-4f9e-8525-6c6348cae208")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://0.0.0.0:8888/token")


async def main():
    monite_mcp_server = MCPServerStdio(
        "uv",
        args=[
            "run",
            "monite-mcp",
        ],
        env={
            "ENTITY_USER_ID": ENTITY_USER_ID,
            "AUTH_SERVICE_URL": AUTH_SERVICE_URL,
        },
    )

    agent = Agent(
        "openai:gpt-4o",
        mcp_servers=[monite_mcp_server],
    )

    async with agent.run_mcp_servers():
        while True:
            try:
                user_prompt = input("Enter your question (or 'exit' to quit): ")
                if user_prompt.lower() == "exit":
                    break

                result = await agent.run(user_prompt)
                print(result.output)
                print("-" * 50)
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
