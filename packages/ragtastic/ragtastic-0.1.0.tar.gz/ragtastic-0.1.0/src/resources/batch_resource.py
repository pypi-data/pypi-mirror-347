from urllib.parse import urljoin

from resources.resource import Resource

from utils.retry import retry_with_backoff
from utils.types import DocumentBatch


class BatchResource(Resource):
    def __enter__(self):
        batch = self.create()
        self.batch_id = batch["id"]

    def __exit__(self, type, value, traceback):
        return self.complete(self.batch_id)

    @retry_with_backoff()
    def create(self) -> DocumentBatch:
        """Create a new document batch"""
        response = self.session.post(
            urljoin(self.base_url, "batches/"), timeout=self.timeout
        )
        return self._handle_response(response)

    @retry_with_backoff()
    def get(self, batch_id: str) -> DocumentBatch:
        """Get batch status"""
        response = self.session.get(
            urljoin(self.base_url, f"batches/{batch_id}/"), timeout=self.timeout
        )
        return self._handle_response(response)

    @retry_with_backoff()
    def complete(self, batch_id: str) -> DocumentBatch:
        """Mark a batch as complete and trigger processing"""
        response = self.session.patch(
            urljoin(self.base_url, f"batches/{batch_id}/"), timeout=self.timeout
        )
        return self._handle_response(response)
