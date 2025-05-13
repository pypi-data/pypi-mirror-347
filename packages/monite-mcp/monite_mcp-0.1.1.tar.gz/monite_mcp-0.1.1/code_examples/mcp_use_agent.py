import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

ENTITY_USER_ID = os.getenv("ENTITY_USER_ID", "1e6a8edf-065d-4f9e-8525-6c6348cae208")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://0.0.0.0:8888/token")
MONITE_API_BASE = os.getenv("MONITE_AI_API_BASE", "https://api.dev.monite.com/v1/mcp")


async def main():
    load_dotenv()

    config = {
        "mcpServers": {
            "monite-mcp": {
                "command": "uv",
                "args": ["run", "monite-mcp"],
                "env": {
                    "ENTITY_USER_ID": ENTITY_USER_ID,
                    "AUTH_SERVICE_URL": AUTH_SERVICE_URL,
                    "MONITE_AI_API_BASE": MONITE_API_BASE,
                },
            }
        }
    }

    client = MCPClient.from_dict(config)

    llm = ChatOpenAI(model="gpt-4o")

    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    while True:
        try:
            user_prompt = input("Enter your question (or 'exit' to quit): ")
            if user_prompt.lower() == "exit":
                break

            result = await agent.run(user_prompt)
            print(result)
            print("-" * 50)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
