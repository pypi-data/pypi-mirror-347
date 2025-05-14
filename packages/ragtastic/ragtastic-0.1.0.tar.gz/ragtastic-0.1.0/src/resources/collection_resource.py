from typing import Optional
from urllib.parse import urljoin

from resources.resource import Resource

from utils.retry import retry_with_backoff
from utils.types import Collection


class CollectionResource(Resource):
    @retry_with_backoff()
    def create(self, description: Optional[str] = "") -> Collection:
        """Creates a collection that can hold documents"""
        response = self.session.post(
            urljoin(self.base_url, "collections/"),
            json={"description": description},
            timeout=self.timeout,
        )
        return self._handle_response(response)

    @retry_with_backoff()
    def delete(self, collection: str | Collection) -> dict:
        """Deletes a collection along with all the documents in them"""
        collection_id = collection if type(collection) is str else collection.id
        response = self.session.delete(
            urljoin(self.base_url, f"collections/{collection_id}/"),
            timeout=self.timeout,
        )
        return self._handle_response(response)
