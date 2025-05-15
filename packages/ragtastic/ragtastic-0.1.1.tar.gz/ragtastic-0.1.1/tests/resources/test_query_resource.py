from unittest.mock import MagicMock, patch
from urllib.parse import urljoin

import pytest
from src.resources.query_resource import QueryResource
from src.utils.types import Collection


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def query_resource(mock_session):
    base_url = "https://api.test.com/v0/"
    timeout = 10
    with patch.object(
        QueryResource, "_handle_response", side_effect=lambda r: r.json()
    ) as mock_handle:
        resource = QueryResource(mock_session, base_url, timeout)
        resource._handle_response_mock = mock_handle
        yield resource


def test_query_create_with_string_ids(query_resource, mock_session):
    """Test creating a query with collection IDs as strings."""
    query_text = "What is the meaning of life?"
    collection_ids = ["col_123", "col_456"]
    expected_url = urljoin(query_resource.base_url, "queries/")
    expected_response_payload = {
        "id": "q_789",
        "query": query_text,
        "collections": [{"id": c} for c in collection_ids],
        "response": {
            "id": "qr_abc",
            "response": "42",
            "is_hallucinating": False,
            "is_lazy": False,
        },
        "object": "query",
        "selected_snippets": [],
    }

    mock_response = MagicMock()
    mock_response.json.return_value = expected_response_payload
    mock_session.post.return_value = mock_response

    result = query_resource.create(query=query_text, collections=collection_ids)

    mock_session.post.assert_called_once_with(
        expected_url,
        json={"query": query_text, "collection_ids": collection_ids},
        timeout=query_resource.timeout,
    )
    query_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert result["id"] == "q_789"
    assert result["query"] == query_text


def test_query_create_with_collection_objects(query_resource, mock_session):
    """Test creating a query with Collection objects."""
    query_text = "Tell me a joke."
    collections_data = [
        {"id": "col_abc", "description": "Jokes Collection"},
        {"id": "col_def", "description": "Fun Facts Collection"},
    ]
    collection_objects = [Collection(**data) for data in collections_data]
    expected_collection_ids = [c.id for c in collection_objects]

    expected_url = urljoin(query_resource.base_url, "queries/")
    expected_response_payload = {
        "id": "q_xyz",
        "query": query_text,
        "collections": [{"id": c} for c in expected_collection_ids],
        "response": {
            "id": "qr_def",
            "response": "Why did the chicken cross the road?",
            "is_hallucinating": False,
            "is_lazy": False,
        },
        "object": "query",
        "selected_snippets": [],
    }

    mock_response = MagicMock()
    mock_response.json.return_value = expected_response_payload
    mock_session.post.return_value = mock_response

    result = query_resource.create(query=query_text, collections=collection_objects)

    mock_session.post.assert_called_once_with(
        expected_url,
        json={"query": query_text, "collection_ids": expected_collection_ids},
        timeout=query_resource.timeout,
    )
    query_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert result["id"] == "q_xyz"
    assert len(result["collections"]) == len(expected_collection_ids)
