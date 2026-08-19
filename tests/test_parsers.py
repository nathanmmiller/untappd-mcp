from tests.test_constants import SAMPLE_BEER_SEARCH_RESULT, SAMPLE_BREWERY_SEARCH_RESULT
from untappd_mcp.parsers import parse_beer_search_result, parse_brewery_search_result
from untappd_mcp.types import BeerSearchResponse, BrewerySearchResponse


def test_parse_beer_search_result_with_no_results():
    result = parse_beer_search_result(
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
    expected: BeerSearchResponse = {
        "found": 0,
        "matches": [],
        "summary": "Found no results for 'suarez palatine'",
    }
    assert result == expected


def test_parse_beer_search_result_with_only_homebrew():
    result = parse_beer_search_result(
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
    expected: BeerSearchResponse = {
        "found": 1,
        "matches": [
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery (Homebrew)",
                "style": "Pilsner - German",
                "abv": 4.9,
                "priority": 1,
            }
        ],
        "summary": "Found 1 homebrew matching 'suarez palatine'",
    }
    assert result == expected


def test_parse_beer_search_result_with_commercial_beers_and_homebrews():
    result = parse_beer_search_result(
        {
            "found": 5,
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
    expected: BeerSearchResponse = {
        "found": 5,
        "matches": [
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery",
                "style": "Pilsner - German",
                "abv": 4.9,
                "priority": 1,
            },
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery",
                "style": "Pilsner - German",
                "abv": 4.9,
                "priority": 2,
            },
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery (Homebrew)",
                "style": "Pilsner - German",
                "abv": 4.9,
                "priority": 3,
            },
            {
                "name": "Palatine Pils",
                "brewery": "Suarez Family Brewery (Homebrew)",
                "style": "Pilsner - German",
                "abv": 4.9,
                "priority": 4,
            },
        ],
        "summary": "Found 2 commercial beers and 2 homebrews matching 'suarez palatine', out of 5 total results",
    }
    assert result == expected


def test_parse_brewery_search_result_with_no_results():
    result = parse_brewery_search_result(
        {"found": 0, "term": "suarez", "brewery": {"count": 0, "items": []}}
    )
    expected: BrewerySearchResponse = {
        "found": 0,
        "matches": [],
        "summary": "Found no results for 'suarez'",
    }
    assert result == expected


def test_parse_brewery_search_result_with_multiple_results():
    result = parse_brewery_search_result(
        {
            "found": 2,
            "term": "suarez",
            "brewery": {
                "count": 2,
                "items": [SAMPLE_BREWERY_SEARCH_RESULT, SAMPLE_BREWERY_SEARCH_RESULT],
            },
        }
    )
    expected: BrewerySearchResponse = {
        "found": 2,
        "matches": [
            {
                "name": "Suarez Family Brewery",
                "beer_count": 920,
                "country_name": "United States",
                "priority": 1,
            },
            {
                "name": "Suarez Family Brewery",
                "beer_count": 920,
                "country_name": "United States",
                "priority": 2,
            },
        ],
        "summary": "Found 2 breweries matching 'suarez'",
    }
    assert result == expected
