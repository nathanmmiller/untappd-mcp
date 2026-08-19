import os

import httpx2
from dotenv import load_dotenv
from mcp.server import MCPServer
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings

from untappd_mcp.parsers import parse_beer_search_result, parse_brewery_search_result
from untappd_mcp.types import (
    BeerSearchResponse,
    BrewerySearchResponse,
    ErrorResponse,
    UntappdBeerSearchResponsePayload,
    UntappdBrewerySearchResponsePayload,
)

load_dotenv()

UNTAPPD_BASE_URL = "https://api.untappd.com/v4/"


class SimpleTokenVerifier(TokenVerifier):
    """Basically we assume every token is valid because it's not up to us.
    If Untappd rejects it, the actual API call will fail. Fine. Whatever.
    But we need to capture it when running in streamable-http mode since the user will supply it."""

    async def verify_token(self, token: str) -> AccessToken | None:
        return AccessToken(token=token, client_id=token, scopes=["api"])


mcp = MCPServer(
    "untappd-mcp",
    token_verifier=SimpleTokenVerifier(),
    auth=AuthSettings(
        issuer_url="https://untappd.com/oauth/authenticate",
        resource_server_url=UNTAPPD_BASE_URL,
    ),
)


def _prepare_authentication_optional_search_parameters(
    query: str, offset: int | None = None
) -> dict[str, str | int | None]:
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    header_access_token = get_access_token()
    token_from_header = header_access_token.token if header_access_token else None
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN") or token_from_header
    parameters = {"q": query, "limit": 50}
    if ACCESS_TOKEN:
        parameters["access_token"] = ACCESS_TOKEN
    else:
        parameters["client_id"] = CLIENT_ID
        parameters["client_secret"] = CLIENT_SECRET
    if offset:
        parameters["offset"] = offset

    return parameters


@mcp.tool()
async def beer_search(
    name: str,
    offset: int | None = None,
) -> BeerSearchResponse | ErrorResponse:
    """
    Search Untappd for a beer by name.
    Offset should be used for "more results". By default only the first 50 results are returned.
    Results will be tagged with a "priority" - lower number = higher priority. When searching for a beer, always consider a lower 'priority' number to be a more relevant search result.
    """
    parameters = _prepare_authentication_optional_search_parameters(name, offset)
    async with httpx2.AsyncClient() as client:
        response = await client.get(UNTAPPD_BASE_URL + "search/beer", params=parameters)
    if response.status_code >= 400:
        try:
            error = response.json()["meta"]["error_detail"]
        except:  # noqa: E722 - fine with all exceptions caught here because we're catching an API error
            error = response.status_code
        return {"error": f"Search Errored: {error}"}
    result: UntappdBeerSearchResponsePayload = response.json()

    return parse_beer_search_result(result["response"])


@mcp.tool()
async def brewery_search(
    name: str, offset: int | None = None
) -> BrewerySearchResponse | ErrorResponse:
    """
    Search Untappd for a brewery by name.
    Offset should be used for "more results". By default only the first 50 results are returned.
    Results will be tagged with a "priority" - lower number = higher priority. When searching for a brewery, always consider a lower 'priority' number to be a more relevant search result.
    """
    parameters = _prepare_authentication_optional_search_parameters(name, offset)
    async with httpx2.AsyncClient() as client:
        response = await client.get(
            UNTAPPD_BASE_URL + "search/brewery", params=parameters
        )
    if response.status_code >= 400:
        try:
            error = response.json()["meta"]["error_detail"]
        except:  # noqa: E722 - fine with all exceptions caught here because we're catching an API error
            error = response.status_code
        return {"error": f"Search Errored: {error}"}
    result: UntappdBrewerySearchResponsePayload = response.json()

    return parse_brewery_search_result(result["response"])


# To run this as a service instead of locally, uncomment the below and run this module
# if __name__ == "__main__":
#     mcp.run(transport="streamable-http", stateless_http=True)
