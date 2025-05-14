from unittest.mock import MagicMock, patch
from urllib.parse import urljoin

import pytest
from src.resources.batch_resource import BatchResource
from src.utils.types import BatchStatus


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def batch_resource(mock_session):
    base_url = "https://api.test.com/v0/"
    timeout = 10
    with patch.object(
        BatchResource, "_handle_response", side_effect=lambda r: r.json()
    ) as mock_handle:
        resource = BatchResource(mock_session, base_url, timeout)
        resource._handle_response_mock = mock_handle
        yield resource


def test_batch_create(batch_resource, mock_session):
    """Test creating a new document batch."""
    expected_url = urljoin(batch_resource.base_url, "batches/")
    expected_payload = {"id": "batch_123", "object": "batch", "status": "PENDING"}

    mock_response = MagicMock()
    mock_response.json.return_value = expected_payload
    mock_session.post.return_value = mock_response

    result = batch_resource.create()

    mock_session.post.assert_called_once_with(
        expected_url, timeout=batch_resource.timeout
    )
    batch_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert result["id"] == "batch_123"
    assert result["status"] == BatchStatus.PENDING


def test_batch_get(batch_resource, mock_session):
    """Test getting batch status."""
    batch_id = "batch_456"
    expected_url = urljoin(batch_resource.base_url, f"batches/{batch_id}/")
    expected_payload = {"id": batch_id, "object": "batch", "status": "PROCESSING"}

    mock_response = MagicMock()
    mock_response.json.return_value = expected_payload
    mock_session.get.return_value = mock_response

    result = batch_resource.get(batch_id)

    mock_session.get.assert_called_once_with(
        expected_url, timeout=batch_resource.timeout
    )
    batch_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert result["status"] == BatchStatus.PROCESSING


def test_batch_complete(batch_resource, mock_session):
    """Test marking a batch as complete."""
    batch_id = "batch_789"
    expected_url = urljoin(batch_resource.base_url, f"batches/{batch_id}/")
    expected_payload = {"id": batch_id, "object": "batch", "status": "DONE"}

    mock_response = MagicMock()
    mock_response.json.return_value = expected_payload
    mock_session.patch.return_value = mock_response

    result = batch_resource.complete(batch_id)

    mock_session.patch.assert_called_once_with(
        expected_url, timeout=batch_resource.timeout
    )
    batch_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert result["status"] == BatchStatus.DONE


def test_batch_context_manager(batch_resource, mock_session):
    """Test the batch resource as a context manager."""
    created_batch_id = "batch_ctx_create"
    completed_batch_id = created_batch_id  # Should be the same

    # Mock responses for create and complete
    create_response_mock = MagicMock()
    create_response_mock.json.return_value = {
        "id": created_batch_id,
        "status": "PENDING",
    }
    complete_response_mock = MagicMock()
    complete_response_mock.json.return_value = {
        "id": completed_batch_id,
        "status": "DONE",
    }

    # Side effect for session calls: first post (create), then patch (complete)
    mock_session.post.return_value = create_response_mock
    mock_session.patch.return_value = complete_response_mock

    assert batch_resource.batch_id == created_batch_id
    # At this point, __enter__ should have called create()
    mock_session.post.assert_called_once_with(
        urljoin(batch_resource.base_url, "batches/"), timeout=batch_resource.timeout
    )
    # _handle_response should have been called for create
    batch_resource._handle_response_mock.assert_any_call(create_response_mock)

    # After exiting context, __exit__ should have called complete()
    mock_session.patch.assert_called_once_with(
        urljoin(batch_resource.base_url, f"batches/{completed_batch_id}/"),
        timeout=batch_resource.timeout,
    )
    # _handle_response should have been called for complete
    batch_resource._handle_response_mock.assert_any_call(complete_response_mock)
    assert batch_resource._handle_response_mock.call_count == 2
