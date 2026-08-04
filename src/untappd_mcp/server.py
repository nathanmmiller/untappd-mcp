import os

import requests
from dotenv import load_dotenv
from mcp.server import MCPServer

from untappd_mcp.types import (
    BeerInfo,
    BeerSearchResponse,
    ErrorResponse,
    UntappdBeerSearchResponse,
    UntappdBeerSearchResponsePayload,
    UntappdBeerSearchResult,
)

load_dotenv()

mcp = MCPServer("untappd-mcp")
UNTAPPD_BASE_URL = "https://api.untappd.com/v4/"


def parse_beer(beer: UntappdBeerSearchResult, isHomebrew: bool = False) -> BeerInfo:
    return {
        "name": beer["beer"]["beer_name"],
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
    beer_info = [parse_beer(beer) for beer in beers["items"]]
    homebrew_info = [parse_beer(beer, True) for beer in homebrews["items"]]

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
    """
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    parameters = {
        "q": name,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "limit": 50,
    }
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
