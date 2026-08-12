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


class UntappdBreweryBaseInfo(TypedDict):
    brewery_id: int
    brewery_name: str
    brewery_slug: str
    brewery_page_url: str
    brewery_label: str
    country_name: str
    location: UntappdBreweryLocation


class UntappdBreweryInfoForBeerSearch(UntappdBreweryBaseInfo):
    brewery_type: str
    brewery_stamp: str
    contact: UntappdBreweryContact
    brewery_active: Literal[0, 1]


class UntappdBeerSearchResult(TypedDict):
    checkin_count: int
    have_had: bool
    your_count: int
    beer: UntappdBeerInfo
    brewery: UntappdBreweryInfoForBeerSearch


class UntappdBeerSearchResults(TypedDict):
    count: int
    items: list[UntappdBeerSearchResult]


class UntappdBreweryInfoForBrewerySearch(UntappdBreweryBaseInfo):
    beer_count: int


class UntappdBrewerySearchResult(TypedDict):
    brewery: UntappdBreweryInfoForBrewerySearch


class UntappdBrewerySearchResults(TypedDict):
    count: int
    items: list[UntappdBrewerySearchResult]


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


class UntappdBrewerySearchResponse(TypedDict):
    found: int
    term: str
    brewery: UntappdBrewerySearchResults


class UntappdBrewerySearchResponsePayload(TypedDict):
    response: UntappdBrewerySearchResponse


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


class BreweryInfo(TypedDict):
    name: str
    beer_count: int
    country_name: str
    priority: int


class BrewerySearchResponse(TypedDict):
    found: int
    matches: list[BreweryInfo]
    summary: str


class ErrorResponse(TypedDict):
    error: str
