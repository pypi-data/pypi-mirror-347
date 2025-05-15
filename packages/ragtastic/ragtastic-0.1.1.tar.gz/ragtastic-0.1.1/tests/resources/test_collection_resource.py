from unittest.mock import MagicMock, patch
from urllib.parse import urljoin

import pytest
from src.resources.collection_resource import CollectionResource
from src.utils.types import Collection


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def collection_resource(mock_session):
    base_url = "https://api.test.com/v0/"
    timeout = 10
    # Patch the _handle_response method for CollectionResource instances
    with patch.object(
        CollectionResource, "_handle_response", side_effect=lambda r: r.json()
    ) as mock_handle:
        resource = CollectionResource(mock_session, base_url, timeout)
        resource._handle_response_mock = mock_handle  # Store mock for assertions
        yield resource


def test_collection_create(collection_resource, mock_session):
    """Test creating a collection."""
    description = "My Test Collection"
    expected_url = urljoin(collection_resource.base_url, "collections/")
    expected_payload = {"id": "col_123", "description": description}

    mock_response = MagicMock()
    mock_response.json.return_value = expected_payload
    mock_session.post.return_value = mock_response

    result = collection_resource.create(description=description)

    mock_session.post.assert_called_once_with(
        expected_url,
        json={"description": description},
        timeout=collection_resource.timeout,
    )
    collection_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert isinstance(
        result, dict
    )  # Because _handle_response is mocked to return r.json()
    assert result["id"] == "col_123"


def test_collection_create_no_description(collection_resource, mock_session):
    """Test creating a collection with default description."""
    expected_url = urljoin(collection_resource.base_url, "collections/")
    expected_payload = {"id": "col_456", "description": ""}

    mock_response = MagicMock()
    mock_response.json.return_value = expected_payload
    mock_session.post.return_value = mock_response

    result = collection_resource.create()  # Default description

    mock_session.post.assert_called_once_with(
        expected_url,
        json={"description": ""},
        timeout=collection_resource.timeout,
    )
    collection_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert result["description"] == ""


def test_collection_delete_by_id_string(collection_resource, mock_session):
    """Test deleting a collection by its ID string."""
    collection_id = "col_789"
    expected_url = urljoin(
        collection_resource.base_url, f"collections/{collection_id}/"
    )
    expected_response_payload = {"message": "deleted"}

    mock_response = MagicMock()
    mock_response.json.return_value = expected_response_payload
    mock_session.delete.return_value = mock_response

    result = collection_resource.delete(collection=collection_id)

    mock_session.delete.assert_called_once_with(
        expected_url, timeout=collection_resource.timeout
    )
    collection_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert result["message"] == "deleted"


def test_collection_delete_by_collection_object(collection_resource, mock_session):
    """Test deleting a collection using a Collection object."""
    collection_obj = Collection(id="col_abc", description="To Be Deleted")
    expected_url = urljoin(
        collection_resource.base_url, f"collections/{collection_obj.id}/"
    )
    expected_response_payload = {"message": "deleted"}

    mock_response = MagicMock()
    mock_response.json.return_value = expected_response_payload
    mock_session.delete.return_value = mock_response

    result = collection_resource.delete(collection=collection_obj)

    mock_session.delete.assert_called_once_with(
        expected_url, timeout=collection_resource.timeout
    )
    collection_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert result["message"] == "deleted"
