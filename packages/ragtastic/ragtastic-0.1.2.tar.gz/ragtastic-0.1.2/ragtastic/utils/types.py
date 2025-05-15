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


class QueryResult(BaseModel):
    document_id: str
    text: str
    score: float


class Query(BaseModel):
    id: str
    object: str
    collections: List[Collection]
    results: List[QueryResult]


class BatchStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    ERROR = "ERROR"


class DocumentBatch(BaseModel):
    id: str
    object: str
    status: BatchStatus
