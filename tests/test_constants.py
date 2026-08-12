from untappd_mcp.types import (
    UntappdBeerInfo,
    UntappdBeerSearchResult,
    UntappdBreweryInfoForBeerSearch,
    UntappdBrewerySearchResult,
)

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
SAMPLE_BREWERY: UntappdBreweryInfoForBeerSearch = {
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

SAMPLE_BREWERY_SEARCH_RESULT: UntappdBrewerySearchResult = {
    "brewery": {
        "brewery_id": 61690,
        "brewery_name": "Suarez Family Brewery",
        "brewery_slug": "suarez-family-brewery",
        "brewery_page_url": "/SuarezFamilyBrewery",
        "beer_count": 920,
        "brewery_label": "suarez.jpg",
        "country_name": "United States",
        "location": {
            "brewery_city": "Hudson",
            "brewery_state": "NY",
            "lat": 42.1109009,
            "lng": -73.8123016,
        },
    }
}
