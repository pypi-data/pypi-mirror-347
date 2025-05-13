import json
from typing import Annotated, Any, Literal

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from monite_mcp_server.schemas import MoniteAuthToken
from monite_mcp_server.settings import (
    AUTH_SERVICE_URL,
    ENTITY_USER_ID,
    MONITE_AI_API_BASE,
    MONITE_API_VERSION,
    USER_AGENT,
)

mcp = FastMCP("monite-mcp")


McpError = str


async def fetch_auth_token() -> MoniteAuthToken:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            AUTH_SERVICE_URL,  # type: ignore
            params={"entity_user_id": ENTITY_USER_ID},
        )
        response.raise_for_status()
        return MoniteAuthToken(
            access_token=response.json()["access_token"],
            token_type=response.json()["token_type"],
            expires_in=response.json()["expires_in"],
        )


async def make_get_request(
    url: str,
    monite_auth_token: MoniteAuthToken,
    params: dict[str, Any] = {},
) -> dict[str, Any] | McpError:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "x-monite-version": MONITE_API_VERSION,
        "Authorization": f"{monite_auth_token.token_type} {monite_auth_token.access_token}",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                headers=headers,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Failed to make request to monite-ai: {e}"


@mcp.tool(
    name="get_counterparties_list",
    description="Get a list of counterparties, optionally filtered by vendor or customer status.",
)
async def get_counterparties_list(
    is_vendor: bool = False,
    is_customer: bool = False,
) -> str:
    url = f"{MONITE_AI_API_BASE}/counterparties_list"
    monite_auth_token = await fetch_auth_token()
    data = await make_get_request(
        url,
        monite_auth_token,
        params={
            "is_vendor": is_vendor,
            "is_customer": is_customer,
        },
    )
    return json.dumps(data)


@mcp.tool(
    name="get_payables_waiting_to_be_paid",
    description="Retrieves all payables with status 'waiting_to_be_paid' (payables that need to be paid by us)",
)
async def get_payables_waiting_to_be_paid() -> str:
    url = f"{MONITE_AI_API_BASE}/payables_waiting_to_be_paid"
    monite_auth_token = await fetch_auth_token()
    data = await make_get_request(
        url,
        monite_auth_token,
    )
    return json.dumps(data)


@mcp.tool(
    name="get_pending_receivables_total_amount",
    description="Retrieval of the total amount of pending receivables for a given period.",
)
async def get_pending_receivables_total_amount(
    period: Literal["THIS_MONTH", "LAST_MONTH", "NEXT_MONTH"] = "THIS_MONTH",
) -> str:
    """Retrieves the total amount of pending receivables for a given period.

    Args:
        period: The period to retrieve the total amount of pending receivables for. Available options: THIS_MONTH, LAST_MONTH, NEXT_MONTH.
    """
    url = f"{MONITE_AI_API_BASE}/pending_receivables_total_amount"
    monite_auth_token = await fetch_auth_token()
    data = await make_get_request(
        url,
        monite_auth_token,
        params={"period": period},
    )
    return json.dumps(data)


@mcp.tool(
    name="get_overdue_receivables_total_amount",
    description="Retrieval of the total amount of overdue receivables.",
)
async def get_overdue_receivables_total_amount() -> str:
    url = f"{MONITE_AI_API_BASE}/overdue_receivables_total_amount"
    monite_auth_token = await fetch_auth_token()
    data = await make_get_request(url, monite_auth_token, params={})
    return json.dumps(data)


@mcp.tool(
    name="get_expired_receivables_count",
    description="Retrieval of the count of expired receivables for a given period.",
)
async def get_expired_receivables_count(
    period: Literal[
        "THIS_MONTH", "LAST_MONTH", "TWO_MONTHS_AGO", "ALL_TIME"
    ] = "LAST_MONTH",
) -> str:
    """Retrieves the count of expired receivables for a given period.

    Args:
        period: The period to retrieve the count of expired receivables for.
                Available options: THIS_MONTH, LAST_MONTH, TWO_MONTHS_AGO, ALL_TIME.
    """
    url = f"{MONITE_AI_API_BASE}/expired_receivables_count"
    monite_auth_token = await fetch_auth_token()
    data = await make_get_request(
        url,
        monite_auth_token,
        params={"period": period},
    )
    return json.dumps(data)


@mcp.tool(
    name="get_overdue_receivables",
    description="Retrieval of overdue receivables.",
)
async def get_overdue_receivables() -> str:
    url = f"{MONITE_AI_API_BASE}/overdue_receivables"
    monite_auth_token = await fetch_auth_token()
    data = await make_get_request(url, monite_auth_token, params={})
    return json.dumps(data)


@mcp.tool(
    name="get_owed_receivables",
    description="Retrieval of owed receivables based on status filters.",
)
async def get_owed_receivables(
    include_issued: Annotated[
        bool, Field(description="Whether to include issued receivables")
    ] = True,
    include_partially_paid: Annotated[
        bool, Field(description="Whether to include partially paid receivables")
    ] = True,
    include_overdue: Annotated[
        bool, Field(description="Whether to include overdue receivables")
    ] = True,
) -> str:
    url = f"{MONITE_AI_API_BASE}/owed_receivables"
    monite_auth_token = await fetch_auth_token()
    params = {
        "include_issued": include_issued,
        "include_partially_paid": include_partially_paid,
        "include_overdue": include_overdue,
    }
    data = await make_get_request(url, monite_auth_token, params=params)
    return json.dumps(data)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
