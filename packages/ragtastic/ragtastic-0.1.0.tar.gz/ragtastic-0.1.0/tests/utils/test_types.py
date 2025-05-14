import pytest
from pydantic import ValidationError as PydanticValidationError
from src.utils.types import (
    BatchStatus,
    Collection,
    Document,
    DocumentBatch,
    Query,
    QueryResponse,
)


def test_collection_type():
    """Test Collection Pydantic model."""
    data = {"id": "col_123", "description": "Test Collection"}
    collection = Collection(**data)
    assert collection.id == "col_123"
    assert collection.description == "Test Collection"

    with pytest.raises(PydanticValidationError):
        Collection(id="col_123")  # Missing description


def test_document_type():
    """Test Document Pydantic model."""
    collection_data = {"id": "col_abc", "description": "Parent Collection"}
    data = {
        "id": "doc_456",
        "is_processed": True,
        "object": "document",
        "description": "Test Document",
        "created_at": 1678886400,
        "collection": collection_data,
    }
    document = Document(**data)
    assert document.id == "doc_456"
    assert document.is_processed is True
    assert document.collection.id == "col_abc"

    with pytest.raises(PydanticValidationError):
        Document(
            id="doc_123", is_processed=False, object="document", description="Test"
        )  # Missing fields


def test_query_response_type():
    """Test QueryResponse Pydantic model."""
    data = {
        "id": "qr_789",
        "response": "This is the answer.",
        "is_hallucinating": False,
        "is_lazy": True,
    }
    query_response = QueryResponse(**data)
    assert query_response.id == "qr_789"
    assert query_response.response == "This is the answer."

    with pytest.raises(PydanticValidationError):
        QueryResponse(id="qr_123")  # Missing fields


def test_query_type():
    """Test Query Pydantic model."""
    collection_data = {"id": "col_xyz", "description": "Query Collection"}
    query_response_data = {
        "id": "qr_abc",
        "response": "Answer to query.",
        "is_hallucinating": False,
        "is_lazy": False,
    }
    data = {
        "id": "q_123",
        "object": "query",
        "query": "What is RAG?",
        "collections": [collection_data],
        "response": query_response_data,
        "selected_snippets": ["snippet1", "snippet2"],
    }
    query = Query(**data)
    assert query.id == "q_123"
    assert query.query == "What is RAG?"
    assert len(query.collections) == 1
    assert query.collections[0].id == "col_xyz"
    assert query.response.id == "qr_abc"

    with pytest.raises(PydanticValidationError):
        Query(id="q_123", object="query")  # Missing fields


def test_batch_status_enum():
    """Test BatchStatus enum."""
    assert BatchStatus.PENDING == "PENDING"
    assert BatchStatus.PROCESSING == "PROCESSING"
    assert BatchStatus.DONE == "DONE"
    assert BatchStatus.ERROR == "ERROR"
    assert len(BatchStatus) == 4


def test_document_batch_type():
    """Test DocumentBatch Pydantic model."""
    data = {"id": "batch_def", "object": "batch", "status": "PENDING"}
    doc_batch = DocumentBatch(**data)
    assert doc_batch.id == "batch_def"
    assert doc_batch.status == BatchStatus.PENDING

    data_done = {"id": "batch_ghi", "object": "batch", "status": BatchStatus.DONE}
    doc_batch_done = DocumentBatch(**data_done)
    assert doc_batch_done.status == BatchStatus.DONE

    with pytest.raises(PydanticValidationError):
        DocumentBatch(id="batch_123", object="batch", status="INVALID_STATUS")

    with pytest.raises(PydanticValidationError):
        DocumentBatch(id="batch_123")  # Missing fields
