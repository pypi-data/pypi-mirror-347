from unittest.mock import MagicMock, mock_open, patch
from urllib.parse import urljoin

import pytest
from src.resources.document_resource import DocumentResource
from src.utils.types import Collection, Document


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def document_resource(mock_session):
    base_url = "https://api.test.com/v0/"
    timeout = 10
    with patch.object(
        DocumentResource, "_handle_response", side_effect=lambda r: r.json()
    ) as mock_handle:
        resource = DocumentResource(mock_session, base_url, timeout)
        resource._handle_response_mock = mock_handle
        yield resource


def test_document_create(document_resource, mock_session, mocker):
    """Test creating (uploading) a document."""
    file_path = "dummy/path/to/file.txt"
    collection_id = "col_123"
    description = "Test document"
    batch_id = "batch_abc"
    expected_url = urljoin(document_resource.base_url, "documents/")
    expected_response_payload = {
        "id": "doc_456",
        "description": description,
        "collection": {"id": collection_id},
    }

    mock_response = MagicMock()
    mock_response.json.return_value = expected_response_payload
    mock_session.post.return_value = mock_response

    # Mock open for file reading
    m_open = mock_open(read_data=b"file content")
    mocker.patch("builtins.open", m_open)

    result = document_resource.create(
        file_path=file_path,
        collection=collection_id,
        description=description,
        batch_id=batch_id,
    )

    m_open.assert_called_once_with(file_path, "rb")
    mock_session.post.assert_called_once()
    args, kwargs = mock_session.post.call_args
    assert args[0] == expected_url
    assert kwargs["data"] == {
        "description": description,
        "collection": collection_id,
        "batch": batch_id,
    }
    assert "file" in kwargs["files"]
    assert kwargs["timeout"] == document_resource.timeout

    document_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert result["id"] == "doc_456"


def test_document_create_with_collection_object(
    document_resource, mock_session, mocker
):
    """Test creating a document using a Collection object."""
    file_path = "another/file.pdf"
    collection_obj = Collection(id="col_789", description="My Collection")
    expected_response_payload = {"id": "doc_xyz"}

    mock_response = MagicMock()
    mock_response.json.return_value = expected_response_payload
    mock_session.post.return_value = mock_response
    mocker.patch("builtins.open", mock_open(read_data=b"pdf content"))

    result = document_resource.create(file_path=file_path, collection=collection_obj)

    _, kwargs = mock_session.post.call_args
    assert kwargs["data"]["collection"] == collection_obj.id
    assert result["id"] == "doc_xyz"


def test_document_get_by_id_string(document_resource, mock_session):
    """Test getting a document by its ID string."""
    document_id = "doc_abc"
    expected_url = urljoin(document_resource.base_url, f"documents/{document_id}/")
    expected_payload = {"id": document_id, "description": "Fetched doc"}

    mock_response = MagicMock()
    mock_response.json.return_value = expected_payload
    mock_session.get.return_value = mock_response

    result = document_resource.get(document=document_id)

    mock_session.get.assert_called_once_with(
        expected_url, timeout=document_resource.timeout
    )
    document_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert result["id"] == document_id


def test_document_get_by_document_object(document_resource, mock_session):
    """Test getting a document using a Document object."""
    doc_obj = Document(
        id="doc_def",
        is_processed=True,
        object="document",
        description="Test Doc",
        created_at=123,
        collection=Collection(id="col_1", description="c1"),
    )
    expected_url = urljoin(document_resource.base_url, f"documents/{doc_obj.id}/")
    expected_payload = {"id": doc_obj.id}

    mock_response = MagicMock()
    mock_response.json.return_value = expected_payload
    mock_session.get.return_value = mock_response

    result = document_resource.get(document=doc_obj)
    mock_session.get.assert_called_once_with(
        expected_url, timeout=document_resource.timeout
    )
    assert result["id"] == doc_obj.id


def test_document_delete_by_id_string(document_resource, mock_session):
    """Test deleting a document by its ID string."""
    document_id = "doc_ghi"
    expected_url = urljoin(document_resource.base_url, f"documents/{document_id}/")
    expected_payload = {"message": "deleted"}

    mock_response = MagicMock()
    mock_response.json.return_value = expected_payload
    mock_session.delete.return_value = mock_response

    result = document_resource.delete(document=document_id)

    mock_session.delete.assert_called_once_with(
        expected_url, timeout=document_resource.timeout
    )
    document_resource._handle_response_mock.assert_called_once_with(mock_response)
    assert result["message"] == "deleted"
