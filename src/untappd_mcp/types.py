from typing import Literal, TypedDict


class UntappdBeerInfo(TypedDict):
    bid: int
    beer_name: str
    beer_slug: str
    beer_label: str
    beer_abv: float
    beer_ibu: int
    beer_description: str
    created_at: str
    beer_style: str
    in_production: Literal[0, 1]
    auth_rating: int
    wish_list: bool


class UntappdBreweryContact(TypedDict):
    twitter: str
    facebook: str
    instagram: str
    url: str


class UntappdBreweryLocation(TypedDict):
    brewery_city: str
    brewery_state: str
    lat: float
    lng: float


class UntappdBreweryInfo(TypedDict):
    brewery_id: int
    brewery_name: str
    brewery_type: str
    brewery_slug: str
    brewery_page_url: str
    brewery_label: str
    brewery_stamp: str
    country_name: str
    contact: UntappdBreweryContact
    location: UntappdBreweryLocation
    brewery_active: Literal[0, 1]


class UntappdBeerSearchResult(TypedDict):
    checkin_count: int
    have_had: bool
    your_count: int
    beer: UntappdBeerInfo
    brewery: UntappdBreweryInfo


class UntappdBeerSearchResults(TypedDict):
    count: int
    items: list[UntappdBeerSearchResult]


class UntappdBrewerySearchResults(TypedDict):
    count: int
    items: list[UntappdBreweryInfo]


class UntappdBeerSearchResponse(TypedDict):
    found: int
    offset: int
    limit: int
    term: str
    parsed_term: str
    beers: UntappdBeerSearchResults
    homebrew: UntappdBeerSearchResults
    breweries: UntappdBrewerySearchResults


class UntappdBeerSearchResponsePayload(TypedDict):
    response: UntappdBeerSearchResponse


class BeerInfo(TypedDict):
    name: str
    brewery: str
    style: str
    abv: float
    priority: int


class BeerSearchResponse(TypedDict):
    found: int
    matches: list[BeerInfo]
    summary: str


class ErrorResponse(TypedDict):
    error: str
