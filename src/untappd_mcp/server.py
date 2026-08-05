import os

import requests
from dotenv import load_dotenv
from mcp.server import MCPServer
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings

from untappd_mcp.types import (
    BeerInfo,
    BeerSearchResponse,
    ErrorResponse,
    UntappdBeerSearchResponse,
    UntappdBeerSearchResponsePayload,
    UntappdBeerSearchResult,
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


def parse_beer(
    beer: UntappdBeerSearchResult, priority: int, isHomebrew: bool = False
) -> BeerInfo:
    return {
        "name": beer["beer"]["beer_name"],
        "priority": priority + 1,
        "brewery": beer["brewery"]["brewery_name"]
        + (" (Homebrew)" if isHomebrew else ""),
        "style": beer["beer"]["beer_style"],
        "abv": beer["beer"]["beer_abv"],
    }


def parse_result(result: UntappdBeerSearchResponse) -> BeerSearchResponse:
    found = result["found"]
    term = result["term"]
    beers = result["beers"]
    homebrews = result["homebrew"]
    beer_info = [
        parse_beer(beer, priority) for priority, beer in enumerate(beers["items"])
    ]
    homebrew_info = [
        parse_beer(beer, priority + len(beer_info), True)
        for priority, beer in enumerate(homebrews["items"])
    ]

    if beer_info and homebrew_info:
        beer_count = beers["count"]
        homebrew_count = homebrews["count"]
        beer_plural = "s" if beer_count > 1 else ""
        homebrew_plural = "s" if homebrew_count > 1 else ""
        summary = f"Found {beer_count} commercial beer{beer_plural} and {homebrew_count} homebrew{homebrew_plural} matching '{term}'"
    elif beer_info:
        plural = "s" if found > 1 else ""
        summary = f"Found {found} beer{plural} matching '{term}'"
    elif homebrew_info:
        plural = "s" if found > 1 else ""
        summary = f"Found {found} homebrew{plural} matching '{term}'"
    else:
        summary = f"Found no results for '{term}'"

    return {
        "found": found,
        "matches": beer_info + homebrew_info,
        "summary": summary,
    }


@mcp.tool()
def search_for_beer(
    name: str,
    offset: int | None = None,
) -> BeerSearchResponse | ErrorResponse:
    """
    Search Untappd for a beer by name.
    Offset should be used for "more results".
    Results will be tagged with a "priority" - lower number = higher priority. When searching for a beer, always consider a lower priority to be a more relevant search result.
    """
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    header_access_token = get_access_token()
    token_from_header = header_access_token.token if header_access_token else None
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN") or token_from_header
    parameters = {"q": name, "limit": 50}
    if ACCESS_TOKEN:
        parameters["access_token"] = ACCESS_TOKEN
    else:
        parameters["client_id"] = CLIENT_ID
        parameters["client_secret"] = CLIENT_SECRET
    if offset:
        parameters["offset"] = offset
    response = requests.get(
        UNTAPPD_BASE_URL + "search/beer",
        parameters,
    )
    if response.status_code >= 400:
        try:
            error = response.json()["meta"]["error_detail"]
        except:  # noqa: E722 - fine with all exceptions caught here because we're catching an API error
            error = response.status_code
        return {"error": f"Search Errored: {error}"}
    result: UntappdBeerSearchResponsePayload = response.json()

    return parse_result(result["response"])


# To run this as a service instead of locally, uncomment the below and run this module
# if __name__ == "__main__":
#     mcp.run(transport="streamable-http", stateless_http=True)
