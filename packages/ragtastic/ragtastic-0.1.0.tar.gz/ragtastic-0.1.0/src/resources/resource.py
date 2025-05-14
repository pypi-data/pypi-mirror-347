import requests

from utils.exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)


class Resource:
    def __init__(self, session, base_url, timeout):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout

    def _handle_response(self, response: requests.Response) -> dict:
        """Handle API response and raise appropriate exceptions"""
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        elif response.status_code == 400:
            raise ValidationError(response.json().get("error", "Validation failed"))
        elif not response.ok:
            raise APIError(
                f"API request failed: {response.text}", status_code=response.status_code
            )

        return response.json()
