"""RateLimiter 테스트"""
import pytest
from src.opendart_mcp.rate_limiter import RateLimiter, RateLimitExceeded


class TestRateLimiter:
    """RateLimiter 테스트"""

    def test_allows_requests_within_limit(self):
        """한도 내 요청은 허용"""
        limiter = RateLimiter(max_requests=3)

        limiter.acquire()
        limiter.acquire()
        limiter.acquire()

        assert limiter.remaining == 0

    def test_throws_when_limit_exceeded(self):
        """한도 초과 시 예외 발생"""
        limiter = RateLimiter(max_requests=2)

        limiter.acquire()
        limiter.acquire()

        with pytest.raises(RateLimitExceeded):
            limiter.acquire()

    def test_tracks_remaining_requests(self):
        """남은 요청 수 추적"""
        limiter = RateLimiter(max_requests=5)

        assert limiter.remaining == 5

        limiter.acquire()
        assert limiter.remaining == 4

        limiter.acquire()
        assert limiter.remaining == 3

    def test_default_limit_is_20000(self):
        """기본 한도는 20,000"""
        limiter = RateLimiter()
        assert limiter.max_requests == 20000
