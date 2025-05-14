import requests
from resources.batch_resource import BatchResource
from resources.collection_resource import CollectionResource
from resources.document_resource import DocumentResource
from resources.query_resource import QueryResource

from utils.exceptions import (
    ArgumentException,
)


class Ragtastic:
    def __init__(
        self,
        api_key: str,
        timeout: int = 30,  # Add a default timeout parameter
    ):
        """
        Initialize the Ragtastic API client

        Args:
            api_key: API key for authentication - This either needs to be provided or put in the RAGTASTIC_API_KEY environment variable
            timeout: Default timeout for HTTP requests in seconds.
        """
        self.base_url = "https://api.useragtastic.com/v0"
        self.timeout = timeout  # Define self.timeout

        if not api_key:
            raise ArgumentException(
                "No API Key provided and we couldn't find one in the RAGTASTIC_API_KEY environment variable. (Hint: You can set your API Key using 'client = ragtastic.RagtasticClient(<API_KEY>))' or just add it to the RAGTASTIC_API_KEY environment variable. You can generate an API key from the Ragtastic dashboard at www.ragtastic.com/api)"
            )

        self.api_key = api_key
        self.session = requests.Session()

        self.session.headers.update({"Authorization": f"Api-Key {api_key}"})

        self.collection = CollectionResource(self.session, self.base_url, self.timeout)
        self.document = DocumentResource(self.session, self.base_url, self.timeout)
        self.query = QueryResource(self.session, self.base_url, self.timeout)
        self.batch = BatchResource(self.session, self.base_url, self.timeout)
