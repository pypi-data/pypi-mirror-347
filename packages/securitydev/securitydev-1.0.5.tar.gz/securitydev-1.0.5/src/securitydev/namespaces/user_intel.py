import httpx

from src.securitydev.models.user_intel import EmailIntelResponse
from src.securitydev.namespaces.base import BaseNamespace


class UserIntelNamespace(BaseNamespace):
    """
    Namespace for accessing User Intelligence API endpoints.
    """

    def __init__(self, client: httpx.Client):
        super().__init__(client)
        self._sync_client = client

    def email(self, email_address: str) -> EmailIntelResponse:
        """
        (Sync) Get intelligence data for an email, including whether it's from a disposable provider.

        Args:
            email_address (str): The email address to analyze

        Returns:
            EmailIntelResponse: Intelligence data about the email

        Raises:
            APIError: If the API request fails
        """
        url = f"/v1/user-intel/email/{email_address}"
        try:
            response = self._sync_client.get(url)
            response.raise_for_status()
            return EmailIntelResponse.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            raise self._handle_api_error(e) from None


class AsyncUserIntelNamespace(BaseNamespace):
    """
    Namespace for asynchronously accessing User Intelligence API endpoints.
    """

    def __init__(self, client: httpx.AsyncClient):
        super().__init__(client)
        self._async_client = client

    async def email(self, email_address: str) -> EmailIntelResponse:
        """
        (Async) Get intelligence data for an email, including whether it's from a disposable provider.

        Args:
            email_address (str): The email address to analyze

        Returns:
            EmailIntelResponse: Intelligence data about the email

        Raises:
            APIError: If the API request fails
        """
        url = f"/v1/user-intel/email/{email_address}"
        try:
            response = await self._async_client.get(url)
            response.raise_for_status()
            return EmailIntelResponse.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            raise self._handle_api_error(e) from None