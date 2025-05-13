import os
from abc import ABCMeta


class ServiceModel(metaclass=ABCMeta):
    def __init__(self):
        self._cloud = os.getenv("AIWB_CLOUD", "aws")
        self._url = os.getenv(
            "AIWB_URL",
            f"https://ai.{self._cloud}.renesasworkbench.com",
        )
