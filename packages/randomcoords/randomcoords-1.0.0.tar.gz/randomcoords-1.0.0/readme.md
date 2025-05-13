# RandomCoords Python Client

[![PyPI version](https://img.shields.io/pypi/v/randomcoords)](https://pypi.org/project/randomcoords/)
![CI](https://github.com/TalhaAwan/randomcoords-python/actions/workflows/ci.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://www.python.org/)
[![Downloads](https://img.shields.io/pypi/dm/randomcoords)](https://pypi.org/project/randomcoords/)

The Python client for the RandomCoords API to fetch random geographic coordinates worldwide.

## Installation

```bash
pip install randomcoords
```

## Requirements

- Python 3.8 or higher.
- An `api_token` from [RandomCoords](https://www.randomcoords.com/docs/rest).

## Usage

```python
from randomcoords import RandomCoords

client = RandomCoords({"api_token": "your-api-token"})

# Get random coordinates from the United States
coords = client.get_country_coordinates("united-states", {"limit": 10})
print(coords)
```

## Available Methods

### `get_regions()`

#### Parameters

None

#### Returns (`RegionsResponse`)

Metadata and a list of supported regions.

### `get_countries()`

#### Parameters

None

#### Returns (`CountriesResponse`)

Metadata and a list of supported countries.

### `get_region_coordinates(region, options)`

#### Parameters

- `region` (`str`) – The region identifier (e.g., `"world"`, `"europe"`).
- `options` (`dict`, optional):
  - `limit` (`int`, optional) – Maximum number of coordinates to return (default: `1`, maximum: `100`).

#### Returns (`RegionCoordinatesResponse`)

Metadata and random coordinates within the specified region.

### `get_country_coordinates(country, options)`

#### Parameters

- `country` (`str`) – The country identifier (e.g., `"united-states"`, `"australia"`).
- `options` (`dict`, optional):
  - `limit` (`int`, optional) – Maximum number of coordinates to return (default: `1`, maximum: `100`).

#### Returns (`CountryCoordinatesResponse`)

Metadata and random coordinates within the specified country.

## Error Handling

The library throws:

- `ValueError` – for validation or unexpected usage issues (e.g., invalid inputs).
- `RandomCoordsApiError` – for HTTP/API-related failures. This custom error includes:
  - `statusCode`: HTTP status code (e.g., `401`, `404`, `429`).
  - `url`: The API request URL.
  - `message`: A descriptive error message.

**Example:**

```python
from randomcoords import RandomCoordsApiError

try:
    # a method call
except ValueError as ve:
    print("Input error:", ve)
except RandomCoordsApiError as api_err:
    print(f"API error {api_err.status_code} at {api_err.url}: {api_err.message}")
except Exception as e:
    print("Unexpected error:", e)

```

## Typed Responses and Exceptions

All response and error types are available as top-level imports:

```python
from randomcoords import (
    RegionsResponse,
    CountriesResponse,
    RegionCoordinatesResponse,
    CountryCoordinatesResponse,
    RandomCoordsApiError,
)
```

## API Reference

- [REST API docs](https://www.randomcoords.com/docs/rest)

## Issues

If you encounter a bug, please [open an issue](https://github.com/TalhaAwan/randomcoords-python/issues).

## License

MIT © Talha Awan
