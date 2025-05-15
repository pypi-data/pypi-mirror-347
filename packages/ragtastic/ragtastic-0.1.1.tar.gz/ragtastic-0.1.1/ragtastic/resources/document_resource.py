from typing import Optional
from urllib.parse import urljoin

from ragtastic.resources.resource import Resource
from ragtastic.utils.retry import retry_with_backoff
from ragtastic.utils.types import Collection, Document


class DocumentResource(Resource):
    @retry_with_backoff()
    def create(
        self,
        file_path: str,
        collection: str | Collection,
        description: Optional[str] = "",
        batch_id: Optional[str] = None,
    ) -> Document:
        """Upload a document to a collection"""
        data = {
            "description": description,
            "collection": collection if type(collection) is str else collection.id,
        }
        if batch_id:
            data["batch"] = batch_id

        with open(file_path, "rb") as file:
            response = self.session.post(
                urljoin(self.base_url, "documents/"),
                data=data,
                files={"file": file},
                timeout=self.timeout,
            )

        self._handle_response(response)
        return Document(**response.json())

    @retry_with_backoff()
    def get(self, document: str | Document) -> Document:
        """Retrieves the document object. This doesn't retrieve the document itself, just the metadata associated with it"""
        document_id = document if type(document) is str else document.id
        response = self.session.get(
            urljoin(self.base_url, f"documents/{document_id}/"), timeout=self.timeout
        )
        self._handle_response(response)
        return Document(**response.json())

    @retry_with_backoff()
    def delete(self, document: str | Document) -> dict:
        """Delete a document"""
        document_id = document if type(document) is str else document.id
        response = self.session.delete(
            urljoin(self.base_url, f"documents/{document_id}/"), timeout=self.timeout
        )
        self._handle_response(response)
        return response
