import requests

from .logger import logger
from .token import AIWBTokenProvider


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
    ):
        """
        Create a new Session object.
        """
        self._auth_token = access_key
        self._cloud = cloud
        self._token_provider = token_provider
        self._tenant = tenant
        self._session = requests.Session()

    @property
    def token_provider(self):
        if self._token_provider == "aiwb":
            return AIWBTokenProvider

    def get_auth_token(self):
        if self._auth_token is None:
            provider = self.token_provider(self._session, self._cloud)
            self._auth_token = provider.load_token()
        return self._auth_token

    def client(self, service_name=None):
        auth_token = self.get_auth_token()
        logger.info(f"token {auth_token}")
