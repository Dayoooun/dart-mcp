"""OpenDART API 예외 클래스"""
from typing import ClassVar


class OpenDartException(Exception):
    """OpenDART API 예외 기본 클래스"""

    code: str
    message: str
    _friendly_message: ClassVar[str] = "알 수 없는 오류가 발생했습니다."

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

    @property
    def friendly_message(self) -> str:
        """사용자 친화적 에러 메시지"""
        return self._friendly_message

    @classmethod
    def from_error_code(cls, code: str, message: str) -> "OpenDartException":
        """에러 코드로부터 적절한 예외 인스턴스 생성"""
        error_map = {
            "010": InvalidKeyError,
            "011": InvalidKeyError,
            "012": AccessDeniedError,
            "013": DataNotFoundError,
            "014": DataNotFoundError,
            "020": RateLimitExceededError,
            "021": RateLimitExceededError,
            "100": InvalidParameterError,
            "800": SystemError,
            "900": SystemError,
            "901": SystemError,
        }
        exception_class = error_map.get(code, OpenDartException)
        return exception_class(code, message)


class InvalidKeyError(OpenDartException):
    """유효하지 않은 API 키 (010, 011)"""

    _friendly_message = "유효하지 않은 API 인증키입니다. 인증키를 확인해주세요."


class AccessDeniedError(OpenDartException):
    """접근 권한 없음 (012)"""

    _friendly_message = "해당 API에 대한 접근 권한이 없습니다."


class DataNotFoundError(OpenDartException):
    """데이터 없음 (013, 014)"""

    _friendly_message = "조회된 데이터가 없습니다."


class RateLimitExceededError(OpenDartException):
    """요청 한도 초과 (020, 021)"""

    _friendly_message = "일일 API 요청 한도를 초과했습니다."


class InvalidParameterError(OpenDartException):
    """잘못된 파라미터 (100)"""

    _friendly_message = "요청 파라미터가 올바르지 않습니다."


class SystemError(OpenDartException):
    """시스템 오류 (800, 900, 901)"""

    _friendly_message = "시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
