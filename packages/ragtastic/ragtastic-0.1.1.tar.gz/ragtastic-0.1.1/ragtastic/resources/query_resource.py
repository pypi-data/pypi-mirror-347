from typing import List
from urllib.parse import urljoin

from ragtastic.resources.resource import Resource
from ragtastic.utils.retry import retry_with_backoff
from ragtastic.utils.types import Collection, Query


class QueryResource(Resource):
    @retry_with_backoff()
    def create(self, query: str, collections: List[str | Collection]) -> Query:
        """Runs a query across collections"""
        collection_ids = [
            collection if type(collection) is str else collection.id
            for collection in collections
        ]

        response = self.session.post(
            urljoin(self.base_url, "queries/"),
            json={"query": query, "collection_ids": collection_ids},
            timeout=self.timeout,
        )
        self._handle_response(response)
        return Query(**response.json())
