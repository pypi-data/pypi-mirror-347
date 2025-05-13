import logging
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

logger = logging.getLogger(__name__)


class BaseHttpClient:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}

    def get(self, path: str, params: Optional[Dict[str, str]]) -> Optional[Any]:
        logger.debug(f"called BaseHttpClient.get({path}, {params})")
        url = f"{self.base_url}/{path}"
        if params:
            url = f"{url}?{urlencode(params)}"

        try:
            logger.debug(f"sending request to {url}")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_error:
            logger.error(f"Error occurred making GET request to {url}: {http_error}")
        except requests.RequestException as request_exception:
            logger.error(
                f"ERROR: Error occurred making GET request to {url}: {request_exception}"
            )

    def post(self, path: str, body: Optional[Any]) -> requests.Response:
        raise NotImplementedError()
