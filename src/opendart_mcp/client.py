"""OpenDART API 클라이언트"""
from typing import Optional
import httpx


class OpenDartClient:
    """OpenDART API 클라이언트

    Args:
        api_key: OpenDART API 인증키 (40자리)
        base_url: API 기본 URL
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://opendart.fss.or.kr/api",
    ):
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.base_url = base_url
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def client(self) -> httpx.AsyncClient:
        """HTTP 클라이언트 (lazy initialization)"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                params={"crtfc_key": self.api_key},
            )
        return self._client

    async def close(self):
        """클라이언트 종료"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
