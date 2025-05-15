from typing import Optional, Union
from urllib.parse import urljoin

from ragtastic.resources.resource import Resource
from ragtastic.utils.retry import retry_with_backoff
from ragtastic.utils.types import Collection


class CollectionResource(Resource):
    @retry_with_backoff()
    def create(self, description: Optional[str] = "") -> Collection:
        """Creates a collection that can hold documents"""
        response = self.session.post(
            urljoin(self.base_url, "collections/"),
            json={"description": description},
            timeout=self.timeout,
        )

        self._handle_response(response)
        return Collection(**response.json())

    @retry_with_backoff()
    def delete(self, collection: Union[str, Collection]) -> dict:
        """Deletes a collection along with all the documents in them"""
        collection_id = collection if type(collection) is str else collection.id
        response = self.session.delete(
            urljoin(self.base_url, f"collections/{collection_id}/"),
            timeout=self.timeout,
        )
        self._handle_response(response)
        return response
