from typing import Any, Dict, List, Optional
from pydantic import BaseModel, SecretStr
from herre_next.fakts.registry import GrantType, GrantRegistry
from herre_next.grants.oauth2.base import BaseOauth2Grant
from oauthlib.oauth2.rfc6749.errors import InvalidClientError
from fakts_next import Fakts
from herre_next.models import Token, TokenRequest
import logging


class HerreFakt(BaseModel):
    """A fakt for the herre_next grant"""

    base_url: str
    name: str
    client_id: SecretStr
    client_secret: SecretStr
    grant_type: GrantType
    grant_kwargs: Dict[str, Any] = {}
    scopes: List[str]
    redirect_uri: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    timeout: int = 500
    no_temp: bool = False


class FaktsGrant(BaseOauth2Grant):
    """A grant that uses fakts to configure itself

    Parameters
    ----------
    fakts : Fakts
        The fakts instance to use
    base_url : Optional[str], optional
        The base url to use for the grant, by default None
    grant_registry : GrantRegistry, optional
        The grant registry to use, by default get_default_grant_registry()
    fakts_group : str
        The fakts group to use for the grant


    """

    fakts: Fakts
    """Fakts instance to use"""
    grant_registry: GrantRegistry
    """The grant registry to use"""

    base_url: Optional[str] = None  # type: ignore
    """The base url to use for the grant (overwrites the one from the fakt)"""
    fakts_group: str
    """The fakts group to use for the grant"""
    allow_reconfiguration_on_invalid_client: bool = True
    """Whether to allow reconfiguration on invalid client errors"""

    _configured = False
    _activegrant: Optional["FaktsGrant"] = None
    _old_fakt: Dict[str, Any] = {}

    def configure(self, fakt: HerreFakt) -> None:
        """Configures the grant

        Sets the active grant to the grant specified in the fakt.

        Parameters
        ----------
        fakt : HerreFakt
            The fakt to configure the grant with

        Raises
        ------
        ValueError
            If the grant_type is not supported


        """
        grant_class = self.grant_registry.get_grant_for_type(fakt.grant_type)

        self._activegrant = grant_class(**fakt.model_dump())  # type: ignore

    async def afetch_token(self, request: TokenRequest) -> Token:
        """Fetches the token

        This function will delegete to the active grant.
        If the underlying fakts has changed, it will reconfigure the grant.

        Parameters
        ----------
        request : TokenRequest
            The token request to use

        Returns
        -------
        Token
            The token

        Raises
        ------
        InvalidClientError
            If the client is invalid and allow_reconfiguration_on_invalid_client is False

        """

        if self.fakts.has_changed(self._old_fakt, self.fakts_group):
            self._old_fakt = await self.fakts.aget(self.fakts_group)  # type: ignore
            self.configure(HerreFakt(**self._old_fakt))

        assert self._activegrant is not None, "Grant not configured"

        try:
            return await self._activegrant.afetch_token(request)
        except InvalidClientError as e:
            if self.allow_reconfiguration_on_invalid_client:
                logging.warning(
                    "Invalid client error, trying to reconfigure the grant",
                    exc_info=True,
                )
                await self.fakts.arefresh()
                self._old_fakt = await self.fakts.aget(self.fakts_group)  # type: ignore
                return await self._activegrant.afetch_token(request)
            else:
                raise e
