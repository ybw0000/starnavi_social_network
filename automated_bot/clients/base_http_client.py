import logging
import urllib.parse
from typing import AnyStr

import httpx
from pydantic import AnyUrl

from automated_bot.utils.exceptions import HTTPClientException

logger = logging.getLogger(__name__)


class BaseHTTPClient:
    EXC_CLASS = HTTPClientException
    BASE_URL: AnyUrl

    def build_full_path(self, endpoint: str) -> str:
        return urllib.parse.urljoin(str(self.BASE_URL), endpoint)  # type: ignore

    async def _request(self, method, endpoint, **kwargs):
        url = self.build_full_path(endpoint)

        self._log_request(method, url, **kwargs)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, **kwargs)
        except httpx.HTTPError as err:
            raise self.EXC_CLASS(url=url, status_code=500, response_text=str(err))

        self._log_response(response)
        self._check_response(response)

        return response

    async def get(self, endpoint, **kwargs):
        return await self._request(method="GET", endpoint=endpoint, **kwargs)

    async def post(self, endpoint, **kwargs):
        return await self._request(method="POST", endpoint=endpoint, **kwargs)

    async def patch(self, endpoint, **kwargs):
        return await self._request(method="PATCH", endpoint=endpoint, **kwargs)

    @staticmethod
    def _log_request(method, url, **kwargs):
        logger.info(
            msg={
                "message": f"Internal {method} request to {url}",
                "kwargs": kwargs,
            }
        )

    @staticmethod
    def _log_response(response: httpx.Response):
        logger.info(
            msg={
                "message": f"Internal response from {response.url}",
                "kwargs": response.text,
            }
        )

    def _check_response(self, response: httpx.Response):
        if response.is_error:
            raise self.EXC_CLASS(
                status_code=response.status_code,
                response_text=response.text,
                url=str(response.url),
            )
