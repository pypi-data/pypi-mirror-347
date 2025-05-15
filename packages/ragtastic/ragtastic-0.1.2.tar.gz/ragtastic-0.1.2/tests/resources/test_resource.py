from unittest.mock import MagicMock

import pytest
import requests  # For requests.exceptions.JSONDecodeError
from src.resources.resource import Resource
from src.utils.exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)


@pytest.fixture
def mock_requests_response():
    def _mock_response(status_code, json_data=None, text_data=""):
        response = MagicMock(spec=requests.Response)
        response.status_code = status_code
        response.ok = 200 <= status_code < 300
        if json_data is not None:
            response.json.return_value = json_data
        else:
            response.json.side_effect = requests.exceptions.JSONDecodeError(
                "msg", "doc", 0
            )
        response.text = text_data
        return response

    return _mock_response


@pytest.fixture
def resource_instance():
    mock_session = MagicMock()
    base_url = "https://api.test.com/v0/"
    timeout = 15
    return Resource(mock_session, base_url, timeout)


def test_resource_initialization(resource_instance):
    """Test Resource class initialization."""
    assert resource_instance.session is not None
    assert resource_instance.base_url == "https://api.test.com/v0/"
    assert resource_instance.timeout == 15


def test_handle_response_success(resource_instance, mock_requests_response):
    """Test _handle_response with a successful (2xx) response."""
    response_data = {"key": "value"}
    mock_response = mock_requests_response(200, json_data=response_data)
    result = resource_instance._handle_response(mock_response)
    assert result == response_data
    mock_response.json.assert_called_once()


def test_handle_response_rate_limit_error(resource_instance, mock_requests_response):
    """Test _handle_response with a 429 RateLimitError."""
    mock_response = mock_requests_response(429)
    with pytest.raises(RateLimitError, match="Rate limit exceeded"):
        resource_instance._handle_response(mock_response)


def test_handle_response_authentication_error(
    resource_instance, mock_requests_response
):
    """Test _handle_response with a 401 AuthenticationError."""
    mock_response = mock_requests_response(401)
    with pytest.raises(AuthenticationError, match="Invalid API key"):
        resource_instance._handle_response(mock_response)


def test_handle_response_validation_error_with_detail(
    resource_instance, mock_requests_response
):
    """Test _handle_response with a 400 ValidationError and error detail."""
    error_detail = {"error": "Specific validation message"}
    mock_response = mock_requests_response(400, json_data=error_detail)
    with pytest.raises(ValidationError, match="Specific validation message"):
        resource_instance._handle_response(mock_response)
    mock_response.json.assert_called_once()


def test_handle_response_validation_error_no_detail(
    resource_instance, mock_requests_response
):
    """Test _handle_response with a 400 ValidationError and no 'error' key in JSON."""
    mock_response = mock_requests_response(
        400, json_data={"detail": "Some other detail"}
    )
    with pytest.raises(ValidationError, match="Validation failed"):  # Default message
        resource_instance._handle_response(mock_response)
    mock_response.json.assert_called_once()


def test_handle_response_validation_error_not_json(
    resource_instance, mock_requests_response
):
    """Test _handle_response with a 400 ValidationError and non-JSON response."""
    mock_response = mock_requests_response(
        400, text_data="Not JSON"
    )  # .json() will raise error
    with pytest.raises(ValidationError, match="Validation failed"):  # Default message
        resource_instance._handle_response(mock_response)
    mock_response.json.assert_called_once()  # It's called, but raises an error


def test_handle_response_generic_api_error(resource_instance, mock_requests_response):
    """Test _handle_response with a generic APIError (e.g., 500)."""
    response_text = "Internal Server Error"
    mock_response = mock_requests_response(503, text_data=response_text)
    with pytest.raises(
        APIError, match=f"API request failed: {response_text}"
    ) as exc_info:
        resource_instance._handle_response(mock_response)
    assert exc_info.value.status_code == 503
