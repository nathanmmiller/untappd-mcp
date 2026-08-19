import json
from typing import cast

import pytest
import respx
from mcp import Client
from mcp.server.auth.provider import AccessToken
from mcp.types import TextContent
from pytest_mock import MockerFixture

from tests.test_constants import SAMPLE_BEER_SEARCH_RESULT, SAMPLE_BREWERY_SEARCH_RESULT
from untappd_mcp.server import UNTAPPD_BASE_URL, SimpleTokenVerifier, mcp
from untappd_mcp.types import (
    BeerSearchResponse,
    BrewerySearchResponse,
    UntappdBeerSearchResponse,
    UntappdBrewerySearchResponse,
)

BASE_PATH = "src.untappd_mcp.server."
SAMPLE_BEER_RESPONSE: UntappdBeerSearchResponse = {
    "found": 1,
    "offset": 0,
    "limit": 50,
    "term": "suarez palatine",
    "parsed_term": "suarez palatine",
    "beers": {"count": 1, "items": [SAMPLE_BEER_SEARCH_RESULT]},
    "homebrew": {"count": 0, "items": []},
    "breweries": {"count": 0, "items": []},
}
SAMPLE_BREWERY_RESPONSE: UntappdBrewerySearchResponse = {
    "found": 1,
    "term": "suarez",
    "brewery": {"count": 1, "items": [SAMPLE_BREWERY_SEARCH_RESULT]},
}


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with Client(mcp, raise_exceptions=True) as c:
        yield c


@pytest.mark.anyio
async def test_call_beer_search_tool(
    client: Client, mocker: MockerFixture, httpx2_mock: respx.Router
) -> None:
    mock_route = httpx2_mock.get(UNTAPPD_BASE_URL + "search/beer").respond(
        200, json={"response": SAMPLE_BEER_RESPONSE}
    )
    mocker.patch(
        BASE_PATH + "os.environ",
        {"CLIENT_ID": "some-client-id", "CLIENT_SECRET": "some-client-secret"},
    )
    result = await client.call_tool("beer_search", {"name": "suarez palatine"})
    expected_response: BeerSearchResponse = {
        "found": 1,
        "matches": [
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery",
                "style": "Pilsner - German",
                "abv": 4.9,
                "priority": 1,
            }
        ],
        "summary": "Found 1 beer matching 'suarez palatine'",
    }
    assert json.loads(cast(TextContent, result.content[0]).text) == expected_response
    assert dict(mock_route.calls[0].request.url.params) == {
        "q": "suarez palatine",
        "client_id": "some-client-id",
        "client_secret": "some-client-secret",
        "limit": "50",
    }


@pytest.mark.anyio
async def test_call_beer_search_tool_using_access_token(
    client: Client, mocker: MockerFixture, httpx2_mock: respx.Router
) -> None:
    mock_route = httpx2_mock.get(UNTAPPD_BASE_URL + "search/beer").respond(
        200, json={"response": SAMPLE_BEER_RESPONSE}
    )
    mocker.patch(
        BASE_PATH + "os.environ",
        {"ACCESS_TOKEN": "some-access-token"},
    )
    result = await client.call_tool("beer_search", {"name": "suarez palatine"})
    expected_response: BeerSearchResponse = {
        "found": 1,
        "matches": [
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery",
                "style": "Pilsner - German",
                "abv": 4.9,
                "priority": 1,
            }
        ],
        "summary": "Found 1 beer matching 'suarez palatine'",
    }
    assert json.loads(cast(TextContent, result.content[0]).text) == expected_response
    assert dict(mock_route.calls[0].request.url.params) == {
        "q": "suarez palatine",
        "access_token": "some-access-token",
        "limit": "50",
    }


@pytest.mark.anyio
async def test_call_beer_search_tool_with_offset_parameter(
    client: Client, mocker: MockerFixture, httpx2_mock: respx.Router
) -> None:
    mock_route = httpx2_mock.get(UNTAPPD_BASE_URL + "search/beer").respond(
        200, json={"response": SAMPLE_BEER_RESPONSE}
    )
    mocker.patch(
        BASE_PATH + "os.environ",
        {"CLIENT_ID": "some-client-id", "CLIENT_SECRET": "some-client-secret"},
    )
    result = await client.call_tool(
        "beer_search",
        {"name": "suarez palatine", "offset": 1},
    )
    expected_response: BeerSearchResponse = {
        "found": 1,
        "matches": [
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery",
                "style": "Pilsner - German",
                "abv": 4.9,
                "priority": 1,
            }
        ],
        "summary": "Found 1 beer matching 'suarez palatine'",
    }
    assert json.loads(cast(TextContent, result.content[0]).text) == expected_response
    assert dict(mock_route.calls[0].request.url.params) == {
        "q": "suarez palatine",
        "client_id": "some-client-id",
        "client_secret": "some-client-secret",
        "limit": "50",
        "offset": "1",
    }


@pytest.mark.anyio
async def test_call_beer_search_tool_with_errors(
    client: Client, mocker: MockerFixture, httpx2_mock: respx.Router
) -> None:
    mock_route = httpx2_mock.get(UNTAPPD_BASE_URL + "search/beer").respond(500)
    mocker.patch(
        BASE_PATH + "os.environ",
        {"CLIENT_ID": "some-client-id", "CLIENT_SECRET": "some-client-secret"},
    )
    result = await client.call_tool(
        "beer_search",
        {"name": "suarez palatine"},
    )
    assert json.loads(cast(TextContent, result.content[0]).text) == {
        "error": "Search Errored: 500"
    }
    assert mock_route.called

    mock_route = httpx2_mock.get(UNTAPPD_BASE_URL + "search/beer").respond(
        500, json={"meta": {"error_detail": "uh oh!"}}
    )
    result = await client.call_tool(
        "beer_search",
        {"name": "suarez palatine"},
    )
    assert json.loads(cast(TextContent, result.content[0]).text) == {
        "error": "Search Errored: uh oh!"
    }
    assert mock_route.called


@pytest.mark.anyio
async def test_call_brewery_search_tool(
    client: Client, mocker: MockerFixture, httpx2_mock: respx.Router
) -> None:
    mock_route = httpx2_mock.get(UNTAPPD_BASE_URL + "search/brewery").respond(
        200, json={"response": SAMPLE_BREWERY_RESPONSE}
    )
    mocker.patch(
        BASE_PATH + "os.environ",
        {"CLIENT_ID": "some-client-id", "CLIENT_SECRET": "some-client-secret"},
    )
    result = await client.call_tool("brewery_search", {"name": "suarez"})
    expected_response: BrewerySearchResponse = {
        "found": 1,
        "matches": [
            {
                "name": "Suarez Family Brewery",
                "beer_count": 920,
                "country_name": "United States",
                "priority": 1,
            }
        ],
        "summary": "Found 1 brewery matching 'suarez'",
    }
    assert json.loads(cast(TextContent, result.content[0]).text) == expected_response
    assert dict(mock_route.calls[0].request.url.params) == {
        "q": "suarez",
        "client_id": "some-client-id",
        "client_secret": "some-client-secret",
        "limit": "50",
    }


@pytest.mark.anyio
async def test_call_brewery_search_tool_using_access_token(
    client: Client, mocker: MockerFixture, httpx2_mock: respx.Router
) -> None:
    mock_route = httpx2_mock.get(UNTAPPD_BASE_URL + "search/brewery").respond(
        200, json={"response": SAMPLE_BREWERY_RESPONSE}
    )
    mocker.patch(
        BASE_PATH + "os.environ",
        {"ACCESS_TOKEN": "some-access-token"},
    )
    result = await client.call_tool("brewery_search", {"name": "suarez"})
    expected_response: BrewerySearchResponse = {
        "found": 1,
        "matches": [
            {
                "name": "Suarez Family Brewery",
                "beer_count": 920,
                "country_name": "United States",
                "priority": 1,
            }
        ],
        "summary": "Found 1 brewery matching 'suarez'",
    }
    assert json.loads(cast(TextContent, result.content[0]).text) == expected_response
    assert dict(mock_route.calls[0].request.url.params) == {
        "q": "suarez",
        "access_token": "some-access-token",
        "limit": "50",
    }


@pytest.mark.anyio
async def test_call_brewery_search_tool_with_offset_parameter(
    client: Client, mocker: MockerFixture, httpx2_mock: respx.Router
) -> None:
    mock_route = httpx2_mock.get(UNTAPPD_BASE_URL + "search/brewery").respond(
        200, json={"response": SAMPLE_BREWERY_RESPONSE}
    )
    mocker.patch(
        BASE_PATH + "os.environ",
        {"CLIENT_ID": "some-client-id", "CLIENT_SECRET": "some-client-secret"},
    )
    result = await client.call_tool(
        "brewery_search",
        {"name": "suarez", "offset": 1},
    )
    expected_response: BrewerySearchResponse = {
        "found": 1,
        "matches": [
            {
                "name": "Suarez Family Brewery",
                "beer_count": 920,
                "country_name": "United States",
                "priority": 1,
            }
        ],
        "summary": "Found 1 brewery matching 'suarez'",
    }
    assert json.loads(cast(TextContent, result.content[0]).text) == expected_response
    assert dict(mock_route.calls[0].request.url.params) == {
        "q": "suarez",
        "client_id": "some-client-id",
        "client_secret": "some-client-secret",
        "limit": "50",
        "offset": "1",
    }


@pytest.mark.anyio
async def test_call_brewery_search_tool_with_errors(
    client: Client, mocker: MockerFixture, httpx2_mock: respx.Router
) -> None:
    mock_route = httpx2_mock.get(UNTAPPD_BASE_URL + "search/brewery").respond(500)
    mocker.patch(
        BASE_PATH + "os.environ",
        {"CLIENT_ID": "some-client-id", "CLIENT_SECRET": "some-client-secret"},
    )
    result = await client.call_tool(
        "brewery_search",
        {"name": "suarez"},
    )
    assert json.loads(cast(TextContent, result.content[0]).text) == {
        "error": "Search Errored: 500"
    }
    assert mock_route.called

    mock_route = httpx2_mock.get(UNTAPPD_BASE_URL + "search/brewery").respond(
        500, json={"meta": {"error_detail": "uh oh!"}}
    )
    result = await client.call_tool(
        "brewery_search",
        {"name": "suarez"},
    )
    assert json.loads(cast(TextContent, result.content[0]).text) == {
        "error": "Search Errored: uh oh!"
    }
    assert mock_route.called


@pytest.mark.anyio
async def test_SimpleTokenVerifier():
    result = await SimpleTokenVerifier().verify_token("SOME_TOKEN")
    assert result == AccessToken(
        token="SOME_TOKEN", client_id="SOME_TOKEN", scopes=["api"]
    )
