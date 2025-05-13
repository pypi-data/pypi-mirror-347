import logging

from .model import ServiceModel
from .session import Session

logger = logging.getLogger(__name__)


class Auth(ServiceModel):
    def __init__(self, session: Session | None = None):
        self.session = session
        super().__init__()

    @classmethod
    def is_service(cls, service_name):
        return service_name == "auth"

    def login(self):
        self.session.generate_auth_token()

    def logout(self):
        self.session.revoke_auth_token()

    def whoami(self):
        self.session.user_info()
