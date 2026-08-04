import json
from typing import cast
from unittest import mock

import pytest
from mcp import Client
from mcp.types import TextContent
from pytest_mock import MockerFixture

from untappd_mcp.server import mcp, parse_result
from untappd_mcp.types import (
    BeerSearchResponse,
    UntappdBeerInfo,
    UntappdBeerSearchResponse,
    UntappdBeerSearchResult,
    UntappdBreweryInfo,
)

BASE_PATH = "src.untappd_mcp.server."

SAMPLE_BEER: UntappdBeerInfo = {
    "bid": 92087,
    "beer_name": "Palatine Pils",
    "beer_label": "palatine.jpg",
    "beer_abv": 4.9,
    "beer_slug": "suarez-family-brewery-palatine-pils",
    "beer_ibu": 0,
    "beer_description": "Just a perfect pilsner.",
    "created_at": "Sun, 20 Sep 1987 17:38:11 -0600",
    "beer_style": "Pilsner - German",
    "in_production": 1,
    "auth_rating": 0,
    "wish_list": False,
}
SAMPLE_BREWERY: UntappdBreweryInfo = {
    "brewery_id": 61690,
    "brewery_name": "Suarez Family Brewery",
    "brewery_slug": "suarez-family-brewery",
    "brewery_page_url": "/SuarezFamilyBrewery",
    "brewery_type": "Micro Brewery",
    "brewery_label": "suarez.jpg",
    "brewery_stamp": "suarez.jpg",
    "country_name": "United States",
    "contact": {"twitter": "", "facebook": "", "instagram": "", "url": ""},
    "location": {
        "brewery_city": "Hudson",
        "brewery_state": "NY",
        "lat": 42.1109009,
        "lng": -73.8123016,
    },
    "brewery_active": 1,
}
SAMPLE_BEER_SEARCH_RESULT: UntappdBeerSearchResult = {
    "checkin_count": 92087,
    "have_had": False,
    "your_count": 0,
    "beer": SAMPLE_BEER,
    "brewery": SAMPLE_BREWERY,
}
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


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with Client(mcp, raise_exceptions=True) as c:
        yield c


@pytest.mark.anyio
async def test_call_search_for_beer_tool(client: Client, mocker: MockerFixture) -> None:
    ok_response = mock.MagicMock()
    ok_response.status_code = 200
    ok_response.json.return_value = {"response": SAMPLE_BEER_RESPONSE}
    mock_requests = mocker.patch(BASE_PATH + "requests.get", return_value=ok_response)
    mocker.patch(
        BASE_PATH + "os.environ",
        {"CLIENT_ID": "some-client-id", "CLIENT_SECRET": "some-client-secret"},
    )
    result = await client.call_tool("search_for_beer", {"name": "suarez palatine"})
    expected_response: BeerSearchResponse = {
        "found": 1,
        "matches": [
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery",
                "style": "Pilsner - German",
                "abv": 4.9,
            }
        ],
        "summary": "Found 1 beer matching 'suarez palatine'",
    }
    assert json.loads(cast(TextContent, result.content[0]).text) == expected_response
    mock_requests.assert_called_once_with(
        "https://api.untappd.com/v4/search/beer",
        {
            "q": "suarez palatine",
            "client_id": "some-client-id",
            "client_secret": "some-client-secret",
            "limit": 50,
        },
    )


@pytest.mark.anyio
async def test_call_search_for_beer_tool_with_offset_parameter(
    client: Client, mocker: MockerFixture
) -> None:
    ok_response = mock.MagicMock()
    ok_response.status_code = 200
    ok_response.json.return_value = {"response": SAMPLE_BEER_RESPONSE}
    mock_requests = mocker.patch(BASE_PATH + "requests.get", return_value=ok_response)
    mocker.patch(
        BASE_PATH + "os.environ",
        {"CLIENT_ID": "some-client-id", "CLIENT_SECRET": "some-client-secret"},
    )
    result = await client.call_tool(
        "search_for_beer",
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
            }
        ],
        "summary": "Found 1 beer matching 'suarez palatine'",
    }
    assert json.loads(cast(TextContent, result.content[0]).text) == expected_response
    mock_requests.assert_called_once_with(
        "https://api.untappd.com/v4/search/beer",
        {
            "q": "suarez palatine",
            "client_id": "some-client-id",
            "client_secret": "some-client-secret",
            "limit": 50,
            "offset": 1,
        },
    )


@pytest.mark.anyio
async def test_call_search_for_beer_tool_with_errors(
    client: Client, mocker: MockerFixture
) -> None:
    error_response = mock.MagicMock()
    error_response.status_code = 500
    error_response.json.return_value = {}
    mocker.patch(BASE_PATH + "requests.get", return_value=error_response)
    mocker.patch(
        BASE_PATH + "os.environ",
        {"CLIENT_ID": "some-client-id", "CLIENT_SECRET": "some-client-secret"},
    )
    result = await client.call_tool(
        "search_for_beer",
        {"name": "suarez palatine"},
    )
    assert json.loads(cast(TextContent, result.content[0]).text) == {
        "error": "Search Errored: 500"
    }
    error_response.json.return_value = {"meta": {"error_detail": "uh oh!"}}
    result = await client.call_tool(
        "search_for_beer",
        {"name": "suarez palatine"},
    )
    assert json.loads(cast(TextContent, result.content[0]).text) == {
        "error": "Search Errored: uh oh!"
    }


def test_parse_result_with_no_results():
    result = parse_result(
        {
            "found": 0,
            "limit": 50,
            "offset": 0,
            "term": "suarez palatine",
            "parsed_term": "suarez palatine",
            "beers": {"count": 0, "items": []},
            "breweries": {"count": 0, "items": []},
            "homebrew": {"count": 0, "items": []},
        }
    )
    assert result == {
        "found": 0,
        "matches": [],
        "summary": "Found no results for 'suarez palatine'",
    }


def test_parse_result_with_only_homebrew():
    result = parse_result(
        {
            "found": 1,
            "limit": 50,
            "offset": 0,
            "term": "suarez palatine",
            "parsed_term": "bogus beer",
            "beers": {"count": 0, "items": []},
            "breweries": {"count": 0, "items": []},
            "homebrew": {"count": 1, "items": [SAMPLE_BEER_SEARCH_RESULT]},
        }
    )
    assert result == {
        "found": 1,
        "matches": [
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery (Homebrew)",
                "style": "Pilsner - German",
                "abv": 4.9,
            }
        ],
        "summary": "Found 1 homebrew matching 'suarez palatine'",
    }


def test_parse_result_with_commercial_beers_and_homebrews():
    result = parse_result(
        {
            "found": 4,
            "limit": 50,
            "offset": 0,
            "term": "suarez palatine",
            "parsed_term": "bogus beer",
            "beers": {
                "count": 2,
                "items": [SAMPLE_BEER_SEARCH_RESULT, SAMPLE_BEER_SEARCH_RESULT],
            },
            "breweries": {"count": 0, "items": []},
            "homebrew": {
                "count": 2,
                "items": [SAMPLE_BEER_SEARCH_RESULT, SAMPLE_BEER_SEARCH_RESULT],
            },
        }
    )
    assert result == {
        "found": 4,
        "matches": [
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery",
                "style": "Pilsner - German",
                "abv": 4.9,
            },
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery",
                "style": "Pilsner - German",
                "abv": 4.9,
            },
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery (Homebrew)",
                "style": "Pilsner - German",
                "abv": 4.9,
            },
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery (Homebrew)",
                "style": "Pilsner - German",
                "abv": 4.9,
            },
        ],
        "summary": "Found 2 commercial beers and 2 homebrews matching 'suarez palatine'",
    }
