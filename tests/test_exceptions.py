"""OpenDART 예외 처리 테스트"""
import pytest
from src.opendart_mcp.exceptions import (
    OpenDartException,
    InvalidKeyError,
    AccessDeniedError,
    DataNotFoundError,
    RateLimitExceededError,
    InvalidParameterError,
    SystemError,
)


class TestOpenDartException:
    """예외 처리 테스트"""

    def test_from_error_code_010_invalid_key(self):
        """에러 코드 010 -> InvalidKeyError"""
        exc = OpenDartException.from_error_code("010", "등록되지 않은 인증키")
        assert isinstance(exc, InvalidKeyError)
        assert exc.code == "010"

    def test_from_error_code_011_invalid_key(self):
        """에러 코드 011 -> InvalidKeyError"""
        exc = OpenDartException.from_error_code("011", "유효하지 않은 인증키")
        assert isinstance(exc, InvalidKeyError)

    def test_from_error_code_012_access_denied(self):
        """에러 코드 012 -> AccessDeniedError"""
        exc = OpenDartException.from_error_code("012", "접근 권한 없음")
        assert isinstance(exc, AccessDeniedError)

    def test_from_error_code_013_data_not_found(self):
        """에러 코드 013 -> DataNotFoundError"""
        exc = OpenDartException.from_error_code("013", "조회된 데이터 없음")
        assert isinstance(exc, DataNotFoundError)

    def test_from_error_code_020_rate_limit(self):
        """에러 코드 020 -> RateLimitExceededError"""
        exc = OpenDartException.from_error_code("020", "요청 한도 초과")
        assert isinstance(exc, RateLimitExceededError)

    def test_from_error_code_100_invalid_param(self):
        """에러 코드 100 -> InvalidParameterError"""
        exc = OpenDartException.from_error_code("100", "부적절한 값")
        assert isinstance(exc, InvalidParameterError)

    def test_from_error_code_800_system_error(self):
        """에러 코드 800 -> SystemError"""
        exc = OpenDartException.from_error_code("800", "시스템 오류")
        assert isinstance(exc, SystemError)

    def test_from_error_code_unknown(self):
        """알 수 없는 에러 코드 -> OpenDartException"""
        exc = OpenDartException.from_error_code("999", "알 수 없는 오류")
        assert isinstance(exc, OpenDartException)
        assert exc.code == "999"

    def test_friendly_message(self):
        """사용자 친화적 메시지 제공"""
        exc = OpenDartException.from_error_code("010", "등록되지 않은 인증키")
        assert "인증키" in exc.friendly_message
