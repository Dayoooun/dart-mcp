"""OpenDART API 레이트 리미터"""
from datetime import datetime, timedelta


class RateLimitExceeded(Exception):
    """일일 요청 한도 초과 예외"""

    def __init__(self, message: str = "일일 요청 한도를 초과했습니다"):
        self.message = message
        super().__init__(message)


class RateLimiter:
    """OpenDART API 레이트 리미터

    일일 요청 한도(기본 20,000건)를 관리합니다.

    Args:
        max_requests: 최대 요청 수 (기본: 20,000)
        window: 한도 리셋 주기 (기본: 24시간)
    """

    def __init__(
        self,
        max_requests: int = 20000,
        window: timedelta = timedelta(hours=24),
    ):
        self.max_requests = max_requests
        self.window = window
        self._tokens = max_requests
        self._last_reset = datetime.now()

    @property
    def remaining(self) -> int:
        """남은 요청 수"""
        self._check_reset()
        return self._tokens

    def _check_reset(self):
        """리셋 시간 확인 및 토큰 리필"""
        now = datetime.now()
        if now - self._last_reset >= self.window:
            self._tokens = self.max_requests
            self._last_reset = now

    def acquire(self):
        """요청 토큰 획득

        Raises:
            RateLimitExceeded: 한도 초과 시
        """
        self._check_reset()
        if self._tokens <= 0:
            raise RateLimitExceeded()
        self._tokens -= 1
