# adyates-SDK

Sample SDK against The One Ring API.  Developed with (and requires) Python3.

# Using the SDK

## Keys

You will need have an API key from [The One API](https://the-one-api.dev/).

## Environment Variables

| Name | Required | Purpose |
|------|----------|---------|
| TOR_ONEAPIKEY | Yes | To make authenticated requests against the The One API |
| TOR_BASEURI | No (Default: `https://the-one-api.dev/v2`) | Base URL for all issued API requests |


## Installation
Install from PyPI using the following command

```
python -m pip install pandelyon-theonesdk
```

Or whatever package manager you choose to use.


To use the SDK, import as follows:

```
import tor
```

## Querying

Successful results are returned as a list of dicts with the direct API values along with meta information about
the query, useful for pagination (if needed).

```
## Fetching the list of Lord of the Rings movies
movies = tor.Movies().get()

movies.results  # [{"_id": "5cd95395de30eff6ebccde5b","name": "The Two Towers", ...]
movies.meta     # {"total": 8, "limit": 1000, "offset": 0, "page": 1, "pages": 1}


## Fetching only The Two Towers

two_towers = tor.Movies("5cd95395de30eff6ebccde5b")

## Fetching quotes from The Two Towers
two_towers = tor.Movies(
    "5cd95395de30eff6ebccde5b",
    quotes=True
).get()

## ...in a specific order
two_towers = tor.Movies(
    "5cd95395de30eff6ebccde5b",
    quotes=True,
    sortby="character:asc"  # Or "character:desc"
).get()

## Paging through quotes from The Two Towers

#### Using offsets
two_towers = tor.Movies(
    "5cd95395de30eff6ebccde5b",
    quotes=True,
    pagination={"limit": 10, "offset": 30}
).get()

#### .. Or by page
two_towers = tor.Movies(
    "5cd95395de30eff6ebccde5b",
    quotes=True,
    pagination={"limit": 10, "page": 4}
).get()

## Filtering the results (But see the Notes below)

two_towers = tor.Movies(
    "5cd95395de30eff6ebccde5b",
    quotes=True,
    filters=[
        "character!=5cd99d4bde30eff6ebccfc15",
        "dialog=/Dwarf/"
    ]
).get()
```

## Exceptions

When executing a query, the following exceptions may occur prior to `requests` making the query:

* `RuntimeError`: If the SDK environment variables (e.g. the API Key) are not properly set
* `requests.RequestError`: If the parameters for any request are incorrectly formed

Any other errors thrown by `requests.get()` will be passed to the user.


# Notes about the behavior of API itself

* When building a paginated query, `offset` and `page` cannot be used at the same time.  If both are present, the `offset` parameter will take priority over `page`.
* Although the filtering API will work on other queries, `/movies` seems to ignore them (e.g. Attempting to regex quotes only containing Dwarf or to a specific character will not work). This isn't apparent in this SDK but is more obvious when performing the same examples on `/character`. 


# Contributing and Development

Development is done with [`poetry`](https://python-poetry.org/).  

Install with test dependecies included:

```poetry install --with test```

Run tests with `poe`:

```poe test```


By default, test coverage results are located in two places:

* Human-readable `htmlcov/index.html`
* Machine-interpretable `test-reports/coverage.xml`
