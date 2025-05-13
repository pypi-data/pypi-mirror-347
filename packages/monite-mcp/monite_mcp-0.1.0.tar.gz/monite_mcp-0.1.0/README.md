# Monite MCP Server

This project provides a Monite MCP (Model Context Protocol) server that seamlessly integrates Monite's advanced AI functionalities as tools for AI agents and AI-driven applications. It offers a streamlined solution for Monite's onboarded clients to leverage AI-driven insights and automation with their financial data, enhancing operational efficiency and decision-making capabilities.

This server is specifically designed to be valuable and easily usable for Monite customers, allowing them to extend their Monite platform experience with powerful AI capabilities.

**Status:** The MCP server is ready for use but is under active development. New tools and features may be added, and existing ones might be refined.

## Main Goals

*   Provides a set of tools corresponding to various Monite AI features, exposed via as a MCP server.
*   Enables easy integration with AI agent frameworks that support the MCP specification.

## Prerequisites

The primary requirement for running the Monite MCP server is a **Monite Authentication Service**. This service is responsible for providing Entity User authentication tokens, which the MCP server uses to make authorized calls to the Monite AI API.

A Python example implementation of such an authentication service (`auth_service.py`) is available in the `code_examples/` directory.

For comprehensive details on Monite's authorization levels and credential management, please refer to the [Monite API Documentation](https://docs.monite.com/get-started/credentials).

## Getting Started

This guide assumes you are familiar with the Monite API, possess partner credentials (`CLIENT_ID` and `CLIENT_SECRET`), and have an onboarded entity with existing data.

The Monite MCP server is intended for use with Monite Entity User tokens. Consequently, `monite-mcp` relies on an external authorization service that securely manages your `CLIENT_ID` and `CLIENT_SECRET`.

### Environment Variables

A Monite MCP server instance requires the following environment variables to be configured:

*   **`AUTH_SERVICE_URL`**: The URL of your authentication service. This service must expose a `GET /token` endpoint that accepts an `entity_user_id` query parameter and returns a Monite Entity User token.
*   **`ENTITY_USER_ID`**: The ID of the Entity User for whom the MCP server will operate.
*   **`MONITE_AI_API_BASE`**: (Optional) The base URL for the Monite AI API. Defaults to the Monite Sandbox environment: `https://api.sandbox.monite.com/v1/mcp`.

The `AUTH_SERVICE_URL` and `ENTITY_USER_ID` variables are mandatory for each Monite MCP server instance. Your `CLIENT_ID` and `CLIENT_SECRET` will be required by the authentication service itself (see example below).

### Running the Example Authentication Service

The `code_examples/` directory includes an example authentication service (`auth_service.py`). To run it:

1.  Ensure your `CLIENT_ID` and `CLIENT_SECRET` are set as environment variables.
2.  Navigate to the `code_examples/` directory.
3.  Execute the following command:
    ```bash
    make run-auth-service
    ```
    This will start `auth_service.py`, which the MCP server can then use to fetch tokens. By default, it runs on `http://localhost:8888`, so your `AUTH_SERVICE_URL` would be `http://localhost:8888/token`.

### Running the Monite MCP Server and Example Agents

The Monite MCP server communicates via standard input/output (stdio) and is typically started as a subprocess by an AI agent.

The `code_examples/` directory contains `pydantic_ai_agent.py` and `mcp_use_agent.py`, which demonstrate how to instantiate and use the `monite-mcp` server with different agent frameworks.

> These examples require `OPENAI_API_KEY` in the environment :)

To run these examples (ensure the example authentication service is running first):

1.  Navigate to the `code_examples/` directory.
2.  Use one of the following commands:
    *   For the Pydantic AI example:
        ```bash
        make run-pydantic-ai-agent
        ```
    *   For the MCP-Use example:
        ```bash
        make run-mcp-use-agent
        ```

These commands will execute the respective agent scripts, which in turn start and interact with the `monite-mcp` server.

## Active Development

This project is actively being developed. Contributions, bug reports, and feature requests are welcome!

