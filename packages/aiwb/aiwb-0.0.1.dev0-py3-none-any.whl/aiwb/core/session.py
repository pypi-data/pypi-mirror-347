import requests
import os
import sys

import logging
from urllib.parse import urlparse
from .token import AIWBTokenProvider
from .model import ServiceModel

logger = logging.getLogger(__name__)


class Session:
    """
    A session stores configuration state and allows you to create service
    clients and resources.

    :param access_key: AIWB personal access key ID
    :param cloud_type: AIWB Cloud type
    :param tenant: AIWB tenant name
    :param token_provider: AIWB auth provider
    """

    def __init__(
        self,
        access_key: str | None = None,
        cloud: str | None = "aws",
        tenant: str | None = None,
        token_provider: str = "aiwb",
        log_level: str = "info",
    ):
        """
        Create a new Session object.
        """
        self._access_key = access_key
        self._cloud = cloud
        self._token_provider = token_provider
        self._tenant = tenant
        self._session = requests.Session()
        if self._access_key:
            # AIWB Personal access key
            auth_token = f"{self._access_key}"
        else:
            # OIDC Device flow
            token = self.load_auth_token()
            # for AIWB Service, using id token
            auth_token = f"{token.get('id_token')}"
        self._log_level = log_level
        _url = urlparse(
            os.getenv(
                "AIWB_URL",
                f"https://ai.{self._cloud}.renesasworkbench.com",
            )
        )
        if _url.port:
            self._domain = f"{_url.hostname}:{_url.port}"
        elif _url.scheme == "https":
            self._domain = f"{_url.hostname}:443"
        elif _url.scheme == "http":
            self._domain = f"{_url.hostname}:80"
        else:
            self._domain = _url.hostname
        self._session.cookies.set("access-token", auth_token, domain=self._domain)

    @property
    def token_provider(self):
        if self._token_provider == "aiwb":
            return AIWBTokenProvider

    def generate_auth_token(self):
        provider = self.token_provider(self._session, self._cloud)
        return provider.generate_token()
    
    def revoke_auth_token(self, token=None):
        provider = self.token_provider(self._session, self._cloud)
        return provider.revoke_token(token)
    
    def load_auth_token(self):
        provider = self.token_provider(self._session, self._cloud)
        return provider.load_token()
    
    def user_info(self):
        if self._access_key:
            # TODO: get user info for personal access key
            return {}
        else:
            # get oauth2 user info
            token = self.load_auth_token()
            session = requests.Session()
            session.headers.update({"Authorization": f"Bearer {token.get('access_token')}"})
            provider = self.token_provider(session, self._cloud)
            return provider.user_info()

    def _get_service_model(self, domain):
        for cls in ServiceModel.__subclasses__():
            if cls.is_registrar_for(domain):
                return cls(domain, self)
        raise ValueError

    def client(self, service_name=None):
        if self._access_key:
            # AIWB Personal access key
            auth_token = f"{self._access_key}"
        else:
            # OIDC Device flow
            token = self.load_auth_token()
            # for AIWB Service, using id token
            auth_token = f"{token.get('id_token')}"
        service_model = None
        for cls in ServiceModel.__subclasses__():
            if cls.is_service(service_name):
                service_model = cls
        self._session.cookies.set("access-token", auth_token)
        if service_model is not None:
            return service_model(session=self._session)
