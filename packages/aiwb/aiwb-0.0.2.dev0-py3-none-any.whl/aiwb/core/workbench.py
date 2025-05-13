import logging

from .model import ServiceModel
from .session import Session

from http import HTTPStatus

logger = logging.getLogger(__name__)


class Workbench(ServiceModel):
    def __init__(self, session: Session | None = None):
        self.session = session
        super().__init__()

    @classmethod
    def is_service(cls, service_name):
        return service_name == "workbench"

    def list(self):
        res = self.session.get(f"{self._url}/api/workbench/workbench_list")
        if res.status_code == HTTPStatus.OK:
            return res.json()
        elif res.status_code == HTTPStatus.UNAUTHORIZED:
            print(
                "fail to list workbench, error %s.", res.json().get("error")
            )
        elif res.status_code in (
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.INTERNAL_SERVER_ERROR,
        ):
            logger.debug("workbench service is unavailable.")
        return {}
