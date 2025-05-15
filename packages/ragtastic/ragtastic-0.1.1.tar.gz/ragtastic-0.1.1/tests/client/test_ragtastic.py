from unittest.mock import patch

import pytest
from src.ragtastic.ragtastic import Ragtastic
from src.resources.batch_resource import BatchResource
from src.resources.collection_resource import CollectionResource
from src.resources.document_resource import DocumentResource
from src.resources.query_resource import QueryResource
from src.utils.exceptions import ArgumentException


@patch("client.ragtastic.requests.Session")
def test_ragtastic_client_initialization_with_api_key(MockSession):
    """Test Ragtastic client initialization with a provided API key."""
    api_key = "test_api_key_123"
    mock_session_instance = MockSession.return_value

    # Default timeout defined in Ragtastic.__init__
    default_timeout = 30

    client = Ragtastic(api_key=api_key)  # Uses default timeout

    assert client.api_key == api_key
    assert client.base_url == "https://useragtastic.com/v0"
    assert client.timeout == default_timeout
    MockSession.assert_called_once()
    mock_session_instance.headers.update.assert_called_once_with(
        {"Authorization": f"Api-Key {api_key}"}
    )

    assert isinstance(client.collection, CollectionResource)
    assert isinstance(client.document, DocumentResource)
    assert isinstance(client.query, QueryResource)
    assert isinstance(client.batch, BatchResource)


@patch("client.ragtastic.requests.Session")
def test_ragtastic_client_initialization_with_custom_timeout(MockSession):
    """Test Ragtastic client initialization with a custom timeout."""
    api_key = "test_api_key_456"
    custom_timeout = 60
    mock_session_instance = MockSession.return_value

    client = Ragtastic(api_key=api_key, timeout=custom_timeout)

    assert client.api_key == api_key
    assert client.timeout == custom_timeout
    MockSession.assert_called_once()
    mock_session_instance.headers.update.assert_called_once_with(
        {"Authorization": f"Api-Key {api_key}"}
    )


@patch("client.ragtastic.requests.Session")
def test_ragtastic_client_initialization_no_api_key_raises_error(MockSession):
    """Test Ragtastic client raises ArgumentException if no API key is provided."""
    with pytest.raises(ArgumentException, match="No API Key provided"):
        Ragtastic(api_key=None)  # type: ignore

    with pytest.raises(ArgumentException, match="No API Key provided"):
        Ragtastic(api_key="")

    MockSession.assert_not_called()


@patch("client.ragtastic.CollectionResource")
@patch("client.ragtastic.DocumentResource")
@patch("client.ragtastic.QueryResource")
@patch("client.ragtastic.BatchResource")
@patch("client.ragtastic.requests.Session")
def test_ragtastic_client_resource_initialization(
    MockSession, MockBatch, MockQuery, MockDocument, MockCollection
):
    """Test that resource attributes are initialized correctly with mocks."""
    api_key = "test_key"
    custom_timeout = 45
    mock_session_instance = MockSession.return_value

    client = Ragtastic(api_key=api_key, timeout=custom_timeout)

    base_url = "https://api.useragtastic.com/v0"

    MockCollection.assert_called_once_with(
        mock_session_instance, base_url, custom_timeout
    )
    MockDocument.assert_called_once_with(
        mock_session_instance, base_url, custom_timeout
    )
    MockQuery.assert_called_once_with(mock_session_instance, base_url, custom_timeout)
    MockBatch.assert_called_once_with(mock_session_instance, base_url, custom_timeout)

    assert client.collection == MockCollection.return_value
    assert client.document == MockDocument.return_value
    assert client.query == MockQuery.return_value
    assert client.batch == MockBatch.return_value
