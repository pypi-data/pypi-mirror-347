from enum import Enum
from typing import List

from pydantic import BaseModel


class Collection(BaseModel):
    id: str
    description: str


class Document(BaseModel):
    id: str
    is_processed: bool
    object: str
    description: str
    created_at: int
    collection: Collection


class QueryResponse(BaseModel):
    id: str
    response: str
    is_hallucinating: bool
    is_lazy: bool


class Query(BaseModel):
    id: str
    object: str
    query: str
    collections: List[Collection]
    response: QueryResponse
    selected_snippets: List[str]


class BatchStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    ERROR = "ERROR"


class DocumentBatch(BaseModel):
    id: str
    object: str
    status: BatchStatus
