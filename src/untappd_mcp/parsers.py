from untappd_mcp.types import (
    BeerInfo,
    BeerSearchResponse,
    BreweryInfo,
    BrewerySearchResponse,
    UntappdBeerSearchResponse,
    UntappdBeerSearchResult,
    UntappdBrewerySearchResponse,
    UntappdBrewerySearchResult,
)


def _parse_beer(
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


def parse_beer_search_result(result: UntappdBeerSearchResponse) -> BeerSearchResponse:
    found = result["found"]
    term = result["term"]
    beers = result["beers"]
    homebrews = result["homebrew"]
    beer_info = [
        _parse_beer(beer, priority) for priority, beer in enumerate(beers["items"])
    ]
    homebrew_info = [
        _parse_beer(beer, priority + len(beer_info), True)
        for priority, beer in enumerate(homebrews["items"])
    ]
    summary_tail = (
        f", out of {found} total results" if found > len(beers) + len(homebrews) else ""
    )

    if beer_info and homebrew_info:
        beer_count = beers["count"]
        homebrew_count = homebrews["count"]
        beer_plural = "s" if beer_count > 1 else ""
        homebrew_plural = "s" if homebrew_count > 1 else ""
        summary = f"Found {beer_count} commercial beer{beer_plural} and {homebrew_count} homebrew{homebrew_plural} matching '{term}'{summary_tail}"
    elif beer_info:
        plural = "s" if found > 1 else ""
        summary = f"Found {found} beer{plural} matching '{term}'{summary_tail}"
    elif homebrew_info:
        plural = "s" if found > 1 else ""
        summary = f"Found {found} homebrew{plural} matching '{term}'{summary_tail}"
    else:
        summary = f"Found no results for '{term}'"

    return {"found": found, "matches": beer_info + homebrew_info, "summary": summary}


def _parse_brewery(brewery: UntappdBrewerySearchResult, priority: int) -> BreweryInfo:
    brewery_info = brewery["brewery"]
    return {
        "name": brewery_info["brewery_name"],
        "priority": priority + 1,
        "beer_count": brewery_info["beer_count"],
        "country_name": brewery_info["country_name"],
    }


def parse_brewery_search_result(
    result: UntappdBrewerySearchResponse,
) -> BrewerySearchResponse:
    found = result["found"]
    term = result["term"]
    breweries = result["brewery"]
    brewery_info = [
        _parse_brewery(brewery, priority)
        for priority, brewery in enumerate(breweries["items"])
    ]

    if brewery_info:
        plural = "ies" if found > 1 else "y"
        summary = f"Found {found} brewer{plural} matching '{term}'"
    else:
        summary = f"Found no results for '{term}'"

    return {"found": found, "matches": brewery_info, "summary": summary}
