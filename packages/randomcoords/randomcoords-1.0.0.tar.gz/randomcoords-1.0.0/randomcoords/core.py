import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, cast

from .types import (
    RegionsResponse,
    CountriesResponse,
    RegionCoordinatesResponse,
    CountryCoordinatesResponse,
    Config,
    CoordinatesOptions,
)

fallback_api_err_messages = {
    403: "Forbidden: Check API token formatting and headers.",
    429: "Too many requests. Wait and try again.",
    500: "Something went wrong.",
}

BASE_URL = "https://api.randomcoords.com/v1/"


class RandomCoordsApiError(Exception):
    def __init__(self, message: str, status_code: int, url: str):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.url = url


class RandomCoords:
    def __init__(self, config: Config):
        base_url = config.get("base_url", BASE_URL)
        api_token = config.get("api_token")
        self._validate_string(api_token, "apiToken", 10, 700)
        self.api_token: str = cast(str, api_token)
        self.base_url = base_url.rstrip("/") + "/"

    def _validate_string(
        self, value: Optional[str], label: str, min_len: int = 3, max_len: int = 30
    ) -> None:
        if not isinstance(value, str) or not value.strip() or " " in value:
            raise ValueError(f"Invalid '{label}': must be a non-empty string without spaces.")
        if len(value) < min_len or len(value) > max_len:
            raise ValueError(
                f"Invalid '{label}': must be between {min_len} and {max_len} characters."
            )

    def _validate_limit(self, limit: Optional[int], min_val: int = 1, max_val: int = 100) -> int:
        value = limit if limit is not None else 1
        if not isinstance(value, int) or not (min_val <= value <= max_val):
            raise ValueError(
                f"Invalid 'limit': must be an integer between {min_val} and {max_val}."
            )
        return value

    def _make_request(self, path: str) -> Any:
        url = f"{self.base_url}{path}"

        req = urllib.request.Request(url)
        req.add_header("x-api-token", self.api_token)
        req.add_header("User-Agent", "randomcoords-python/1.0")

        try:
            with urllib.request.urlopen(req) as response:
                content_type = response.headers.get("Content-Type", "application/json")
                body = response.read()
                if "application/json" in content_type:
                    try:
                        return json.loads(body)
                    except json.JSONDecodeError:
                        raise ValueError("Invalid JSON response.")

                raise ValueError("Unexpected content type in response.", response.status, url)

        except urllib.error.HTTPError as e:
            body = e.read()
            message = ""
            try:
                parsed = json.loads(body)
                message = parsed.get("message", "")
            except Exception:
                pass

            raise RandomCoordsApiError(
                message or fallback_api_err_messages.get(e.code, "Unexpected error occurred."),
                e.code,
                url,
            )

    def get_regions(self) -> RegionsResponse:
        return cast(RegionsResponse, self._make_request("coordinates/regions"))

    def get_region_coordinates(
        self, region: str, options: Optional[CoordinatesOptions] = None
    ) -> RegionCoordinatesResponse:
        self._validate_string(region, "region")
        limit = options.get("limit") if options else None
        limit_val = self._validate_limit(limit)
        return cast(
            RegionCoordinatesResponse,
            self._make_request(f"coordinates/regions/{region}?limit={limit_val}"),
        )

    def get_countries(self) -> CountriesResponse:
        return cast(CountriesResponse, self._make_request("coordinates/countries"))

    def get_country_coordinates(
        self, country: str, options: Optional[CoordinatesOptions] = None
    ) -> CountryCoordinatesResponse:
        self._validate_string(country, "country")
        limit = options.get("limit") if options else None
        limit_val = self._validate_limit(limit)
        return cast(
            CountryCoordinatesResponse,
            self._make_request(f"coordinates/countries/{country}?limit={limit_val}"),
        )
