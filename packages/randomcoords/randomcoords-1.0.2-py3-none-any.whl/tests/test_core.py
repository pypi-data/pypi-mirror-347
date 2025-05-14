import pytest
from randomcoords import RandomCoords, RandomCoordsApiError
from unittest.mock import patch, MagicMock
import urllib.error
import os
from typing import cast
from http.client import HTTPMessage
from io import BytesIO

from dotenv import load_dotenv

load_dotenv()

if not os.getenv("API_TOKEN"):
    raise RuntimeError("API_TOKEN environment variable is not set.")

api_token = cast(str, os.getenv("API_TOKEN"))

err_msg_api_token = [
    "Invalid 'apiToken': must be a non-empty string without spaces.",
    "Invalid 'apiToken': must be between 10 and 700 characters.",
]

err_msg_region = [
    "Invalid 'region': must be a non-empty string without spaces.",
    "Invalid 'region': must be between 3 and 30 characters.",
]

err_msg_country = [
    "Invalid 'country': must be a non-empty string without spaces.",
    "Invalid 'country': must be between 3 and 30 characters.",
]

err_msg_limit = "Invalid 'limit': must be an integer between 1 and 100."


def test_get_regions() -> None:
    client = RandomCoords({"api_token": api_token})
    response = client.get_regions()
    assert response["type"] == "regions"
    assert response["results"] > 0
    first = response["data"][0]
    assert first["id"]
    assert first["name"]


def test_get_countries() -> None:
    client = RandomCoords({"api_token": api_token})
    response = client.get_countries()
    assert response["type"] == "countries"
    assert response["results"] > 0
    first = response["data"][0]
    assert first["id"]
    assert first["iso2"]
    assert first["name"]


def test_get_region_coordinates() -> None:
    client = RandomCoords({"api_token": api_token})
    response = client.get_region_coordinates("asia", {"limit": 10})
    assert response["id"] == "asia"
    assert response["name"]
    assert response["type"] == "region"
    assert response["results"] == 10
    first = response["data"][0]
    assert first["id"]
    assert first["country"]
    assert first["city"]
    assert first["iso2"]
    assert len(first["coordinates"]) == 2


def test_get_country_coordinates() -> None:
    client = RandomCoords({"api_token": api_token})
    response = client.get_country_coordinates("united-states", {"limit": 10})
    assert response["id"] == "united-states"
    assert response["name"]
    assert response["type"] == "country"
    assert len(response["regions"]) > 0
    assert response["iso2"]
    assert response["results"] == 10
    first = response["data"][0]
    assert first["city"]
    assert first["state"]
    assert len(first["coordinates"]) == 2


def test_token_missing() -> None:
    with pytest.raises(ValueError, match=err_msg_api_token[0]):
        RandomCoords({})


def test_token_empty() -> None:
    with pytest.raises(ValueError, match=err_msg_api_token[0]):
        RandomCoords({"api_token": ""})


def test_token_non_string() -> None:
    with pytest.raises(ValueError, match=err_msg_api_token[0]):
        RandomCoords({"api_token": 789})  # type: ignore[typeddict-item]


def test_token_with_spaces() -> None:
    with pytest.raises(ValueError, match=err_msg_api_token[0]):
        RandomCoords({"api_token": "abcdef ghijkl mno"})


def test_token_less_than_minimum_length() -> None:
    with pytest.raises(ValueError, match=err_msg_api_token[1]):
        RandomCoords({"api_token": "abcde"})


def test_token_exceeds_maximum_length() -> None:
    with pytest.raises(ValueError, match=err_msg_api_token[1]):
        RandomCoords({"api_token": "a" * 701})


def test_identifier_empty_string() -> None:
    client = RandomCoords({"api_token": api_token})
    with pytest.raises(ValueError, match=err_msg_region[0]):
        client.get_region_coordinates("")

    with pytest.raises(ValueError, match=err_msg_country[0]):
        client.get_country_coordinates("")


def test_identifier_with_spaces() -> None:
    client = RandomCoords({"api_token": api_token})
    with pytest.raises(ValueError, match=err_msg_region[0]):
        client.get_region_coordinates("united states")

    with pytest.raises(ValueError, match=err_msg_country[0]):
        client.get_country_coordinates("united states")


def test_identifier_non_string() -> None:
    client = RandomCoords({"api_token": api_token})
    with pytest.raises(ValueError, match=err_msg_region[0]):
        client.get_region_coordinates({"id": 7})  # type: ignore[arg-type]

    with pytest.raises(ValueError, match=err_msg_country[0]):
        client.get_country_coordinates({"id": 7})  # type: ignore[arg-type]


def test_identifier_exceeds_max_length() -> None:
    client = RandomCoords({"api_token": api_token})
    long_str = "some-very-long-string-123456789-xyz"
    with pytest.raises(ValueError, match=err_msg_region[1]):
        client.get_region_coordinates(long_str)

    with pytest.raises(ValueError, match=err_msg_country[1]):
        client.get_country_coordinates(long_str)


def test_identifier_less_than_min_length() -> None:
    client = RandomCoords({"api_token": api_token})
    with pytest.raises(ValueError, match=err_msg_region[1]):
        client.get_region_coordinates("a")

    with pytest.raises(ValueError, match=err_msg_country[1]):
        client.get_country_coordinates("a")


def test_unauthorized_401() -> None:
    client = RandomCoords({"api_token": "invalid-token"})
    with pytest.raises(RandomCoordsApiError) as exc_info:
        client.get_regions()

    err = exc_info.value
    assert err.status_code == 401
    assert "invalid" in err.message.lower()


def test_not_found_404() -> None:
    client = RandomCoords({"api_token": api_token})
    with pytest.raises(RandomCoordsApiError) as exc_info:
        client.get_region_coordinates("nonexistent-region")

    err = exc_info.value
    assert err.status_code == 404
    assert "nonexistent-region" in err.message


@patch("urllib.request.urlopen")
def test_server_error_500(mock_urlopen: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.read.return_value = b"<html><body>Something went wrong somewhere</body></html>"
    mock_response.headers.get.return_value = "text/html"
    mock_response.__enter__.side_effect = urllib.error.HTTPError(
        url="https://api.randomcoords.com/...",
        code=500,
        msg="Internal Server Error",
        hdrs=HTTPMessage(),
        fp=BytesIO(b"Internal error"),
    )
    mock_urlopen.return_value = mock_response

    client = RandomCoords({"api_token": api_token})
    with pytest.raises(RandomCoordsApiError) as exc_info:
        client.get_regions()

    err = exc_info.value
    assert err.status_code == 500
    assert err.message == "Something went wrong."
    mock_urlopen.assert_called()


@patch("urllib.request.urlopen")
def test_server_error_429(mock_urlopen: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.read.return_value = b"<html><body>Too many requests</body></html>"
    mock_response.headers.get.return_value = "text/html"
    mock_response.__enter__.side_effect = urllib.error.HTTPError(
        url="https://api.randomcoords.com/...",
        code=429,
        msg="Too many requests",
        hdrs=HTTPMessage(),
        fp=BytesIO(b"Too many requests"),
    )
    mock_urlopen.return_value = mock_response

    client = RandomCoords({"api_token": api_token})
    with pytest.raises(RandomCoordsApiError) as exc_info:
        client.get_regions()

    err = exc_info.value
    assert err.status_code == 429
    assert err.message == "Too many requests. Wait and try again."
    mock_urlopen.assert_called()


@patch("urllib.request.urlopen")
def test_invalid_json_response(mock_urlopen: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"id": 1, "name": "a",'
    mock_response.headers.get.return_value = "application/json"
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response

    client = RandomCoords({"api_token": api_token})
    with pytest.raises(ValueError) as exc_info:
        client.get_regions()

    assert str(exc_info.value) == "Invalid JSON response."
    mock_urlopen.assert_called()


def test_limit_less_than_min() -> None:
    client = RandomCoords({"api_token": api_token})
    with pytest.raises(ValueError, match=err_msg_limit):
        client.get_region_coordinates("abc", {"limit": 0})

    with pytest.raises(ValueError, match=err_msg_limit):
        client.get_country_coordinates("abc", {"limit": 0})


def test_limit_exceeds_max() -> None:
    client = RandomCoords({"api_token": api_token})
    with pytest.raises(ValueError, match=err_msg_limit):
        client.get_region_coordinates("abc", {"limit": 1000})

    with pytest.raises(ValueError, match=err_msg_limit):
        client.get_country_coordinates("abc", {"limit": 1000})


def test_limit_non_number() -> None:
    client = RandomCoords({"api_token": api_token})
    with pytest.raises(ValueError, match=err_msg_limit):
        client.get_region_coordinates("abc", {"limit": "1"})  # type: ignore[typeddict-item]

    with pytest.raises(ValueError, match=err_msg_limit):
        client.get_country_coordinates("abc", {"limit": "1"})  # type: ignore[typeddict-item]


def test_limit_decimal() -> None:
    client = RandomCoords({"api_token": api_token})
    with pytest.raises(ValueError, match=err_msg_limit):
        client.get_region_coordinates("abc", {"limit": 3.14})  # type: ignore[typeddict-item]

    with pytest.raises(ValueError, match=err_msg_limit):
        client.get_country_coordinates("abc", {"limit": 3.14})  # type: ignore[typeddict-item]
