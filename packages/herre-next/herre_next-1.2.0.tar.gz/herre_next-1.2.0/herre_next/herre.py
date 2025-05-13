import asyncio
from typing import Any, Optional, Type, TypeVar
from herre_next.errors import HerreError, NoHerreFound
from herre_next.grants.base import BaseGrant
import os
import logging
from herre_next.models import Token, TokenRequest
import contextvars
from koil.composition import KoiledModel
from koil.helpers import unkoil
from herre_next.fetcher.models import UserFetcher
from pydantic import BaseModel

current_herre_next: contextvars.ContextVar[Optional["Herre"]] = contextvars.ContextVar(
    "current_herre_next", default=None
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


class Herre(KoiledModel):
    """Herre is a client for Token authentication.

    It provides a unified, composable interface for token based authentication based on grant.
    A grant is a class that is able to retrieve a token. Importantly grants do not have to
    directly call the token endpoint. They can also use a cache or other means to retrieve the
    token.

    Herre is a context manager. This allows it both to provide itself as a singleton and handle
    the asynchronous interface of the grant. As well as providing a lock to ensure that only one
    request is happening at a time.

    Example:
        ```python
        from herre_next import Herre,
        from herre_next.grants.oauth2.client_credentials import ClientCredentialsGrant

        herre_next = Herre(
            grant=ClientCredentialsGrant(
                client_id="my_client_id",
                client_secret="my_client
                base_url="https://my_token_url",
            )
        )

        with herre_next:
            token = herre_next.get_token()
        ```

        or aync

        ```python
        from herre_next import Herre,
        from herre_next.grants.oauth2.client_credentials import ClientCredentialsGrant

        herre_next = Herre(
            grant=ClientCredentialsGrant(
                client_id="my_client_id",
                client_secret="my_client
                base_url="https://my_token_url",
            )
        )

        async with herre_next:
            token = await herre_next.get_token()
        ```

    """

    grant: BaseGrant
    fetcher: Optional[UserFetcher] = None
    max_retries: int = 1
    allow_insecure: bool = False
    scope_delimiter: str = " "
    auto_login: bool = True

    login_on_enter: bool = False
    logout_on_exit: bool = False
    entered: bool = False

    no_temp: bool = False

    _lock: Optional[asyncio.Lock] = None
    _token: Optional[Token] = None

    @property
    def token(self) -> Token:
        "The current token"
        assert self._lock is not None, (
            "Please enter the context first to access this variable"
        )
        assert self._token is not None, "No token fetched"
        return self._token

    async def aget_token(self) -> str:
        """Get an access token

        Will return an access token if it is already available or
        try to login depending on auto_login. The checking and potential retrieving will happen
        in a lock ensuring that not multiple requests are happening at the same time.

        Args:
            auto_login (bool, optional): Should we allow an automatic login. Defaults to True.

        Returns:
            str:  The access token
        """
        assert self._lock is not None, (
            "We were not initialized. Please enter the context first"
        )

        async with self._lock:
            if not self._token or not self._token.access_token:
                await self.arequest_from_grant(TokenRequest())

        assert self._token is not None, "We should have a token by now"
        return self._token.access_token

    async def arefresh_token(self) -> str:
        """Refresh the token

        Will cause the linked grant to refresh the token. Depending
        on the link logic, this might cause another login.

        """
        assert self._lock is not None, (
            "We were not initialized. Please enter the context first"
        )

        async with self._lock:
            await self.arequest_from_grant(TokenRequest(is_refresh=True))
            assert self._token is not None, "We should have a token by now"
            return self._token.access_token

    async def arequest_from_grant(self, request: TokenRequest) -> Token:
        """Request a token from the grant

        You should not need to call this method directly. It is used internally
        to request a token from the grant, and will not directly acquire a lock
        (so multiple requests can happen at the same time, which is often not what
        you want).

        Parameters
        ----------
        request : TokenRequest
            The token request (contains context and whether it is a refresh request)

        Returns
        -------
        Token
            The token (with access_token, refresh_token, etc.)
        """
        potential_token = await self.grant.afetch_token(request)
        self._token = potential_token
        return self._token

    def get_token(self) -> str:
        """Get an access token

        Will return an access token if it is already available or
        try to login depending on auto_login. The checking and potential retrieving will happen
        in a lock ensuring that not multiple requests are happening at the same time.
        """
        return unkoil(self.aget_token)

    async def aget_user(self) -> BaseModel:  # TODO: Should be generic
        """Get the current user

        Will return the current user if a fetcher is available
        """
        assert self._lock is not None, (
            "We were not initialized. Please enter the context first"
        )
        assert self.fetcher is not None, "We have no fetcher available"
        if not self._token:
            raise HerreError("No token available")
        async with self._lock:
            if not self._token or not self._token.access_token:
                await self.arequest_from_grant(TokenRequest())

        assert self._token is not None, "We should have a token by now"
        return await self.fetcher.afetch_user(self._token)

    async def __aenter__(self) -> "Herre":
        """Enters the context and logs in if needed"""
        if self.allow_insecure:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        current_herre_next.set(self)
        self.entered = True
        self._lock = asyncio.Lock()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        traceback: Optional[Any],
    ) -> None:
        """Exits the context and logs out if needed"""
        if self.allow_insecure:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
        current_herre_next.set(None)

    def _repr_html_inline_(self) -> str:
        """Jupyter inline representation"""
        return f"<table><tr><td>auto_login</td><td>{self.auto_login}</td></tr></table>"


def get_current_herre_next() -> Herre:
    """Get the current herre_next instance"""
    herre_next = current_herre_next.get()

    if herre_next is None:
        raise NoHerreFound("No herre_next instance available")

    return herre_next
