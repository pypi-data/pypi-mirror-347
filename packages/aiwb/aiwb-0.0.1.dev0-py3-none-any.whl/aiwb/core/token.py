import os
import json
import time
from datetime import datetime, timedelta
from dateutil.tz import tzutc
import requests
from http import HTTPStatus
import http.client

import logging
from aiwb.utils import CACHE_DIR, can_launch_browser, open_page_in_browser

# TODO: remove this after fixing the over number headers issue in backend.
http.client._MAXHEADERS = 1000

logger = logging.getLogger(__name__)


def _utc_now():
    return datetime.now(tzutc())


class AIWBTokenProvider:
    METHOD = "aiwb"

    def __init__(self, session=None, cloud="aws", time_fetcher=_utc_now):
        self._session = session if session else requests.Session()
        self._now = time_fetcher
        self._cache_dir = CACHE_DIR
        self._cloud = cloud
        self._oidc_url = os.getenv(
            "AIWB_URL",
            f"https://ai.{self._cloud}.renesasworkbench.com",
        )

    @property
    def _client_id(self):
        return os.getenv(
            "AIWB_OIDC_CLIENT_ID",
            "aiwb_workbench",
        )

    @property
    def _cache_key(self):
        return os.path.join(self._cache_dir, "token.json")

    def _save_token(self, res):
        try:
            file_content = json.dumps(res)
        except (TypeError, ValueError):
            logger.exception(
                "Value cannot be cached, must be JSON serializable: %s", res
            )
            raise
        if not os.path.isdir(self._cache_dir):
            os.makedirs(self._cache_dir)
        with os.fdopen(
            os.open(self._cache_key, os.O_WRONLY | os.O_CREAT, 0o600), "w"
        ) as f:
            f.truncate()
            f.write(file_content)

    def _wait_for_token(self, device_code):
        now = _utc_now()
        while True:
            if now < _utc_now() - timedelta(seconds=180):
                print("timeout for waiting device token...")
                return
            logger.debug("waiting for device token...")
            data = {
                "client_id": self._client_id,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            }
            res = requests.post(
                f"{self._oidc_url}/api/auth/token", json=data, timeout=300
            )
            if res.status_code == HTTPStatus.OK:
                logger.debug("successfully retrieve device token.")
                self._save_token(res.json())
                return res.json()
            elif res.status_code == HTTPStatus.UNAUTHORIZED:
                logger.debug(
                    "fail to get device token, error %s.", res.json().get("error")
                )
            elif res.status_code in (
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.INTERNAL_SERVER_ERROR,
            ):
                logger.debug("workbench service is unavailable.")
            time.sleep(3)

    def revoke_token(self, token=None):
        if token is None:
            token = self.load_token().get("access_token")
        data = {"client_id": self._client_id, "token": token}
        response = self._session.post(
            f"{self._oidc_url}/api/auth/revoke_token", json=data
        )
        if response.status_code == HTTPStatus.OK:
            with os.fdopen(
                os.open(self._cache_key, os.O_WRONLY | os.O_CREAT, 0o600), "w"
            ) as f:
                f.truncate()
            return True
        return False

    def user_info(self):
        response = self._session.get(f"{self._oidc_url}/api/auth/userinfo")
        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            return {}

    def generate_token(self):
        data = {"client_id": self._client_id, "scopes": "openid email profile"}
        response = self._session.post(
            f"{self._oidc_url}/api/auth/device/code", json=data
        )
        if response.status_code == HTTPStatus.OK:
            res = response.json()
            device_code = res.get("device_code")
            user_code = res.get("user_code")
            url = f"{self._oidc_url}/device-activate?user-code={user_code}"
            print(
                "Attempting to automatically open the workbench authorization page in your default browser."
            )
            print(
                f"If the browser does not popup, you can open the following URL: {url}"
            )
            if can_launch_browser():
                open_page_in_browser(url)
            return self._wait_for_token(device_code)
        # TODO: raise exception below
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            print("fail to get device token, error %s.", response.get("error"))
        elif response.status_code in (
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.INTERNAL_SERVER_ERROR,
        ):
            print("workbench service is unavailable.")
        else:
            print("unknown error.")
        return None

    def load_token(self):
        if os.path.isdir(self._cache_dir):
            f = open(self._cache_key, encoding="utf-8")
            try:
                token = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                return {}
            if token:
                return token
            f.close()
        return {}
