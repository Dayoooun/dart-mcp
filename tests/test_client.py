"""OpenDartClient 테스트"""
import pytest
from src.opendart_mcp.client import OpenDartClient


class TestOpenDartClient:
    """OpenDartClient 기본 테스트"""

    def test_requires_api_key(self):
        """API 키 없이 생성 시 에러"""
        with pytest.raises(ValueError, match="API key"):
            OpenDartClient(api_key="")

    def test_stores_api_key(self):
        """API 키가 저장됨"""
        client = OpenDartClient(api_key="test_api_key_12345")
        assert client.api_key == "test_api_key_12345"

    def test_uses_correct_base_url(self):
        """기본 URL이 올바름"""
        client = OpenDartClient(api_key="test_key")
        assert client.base_url == "https://opendart.fss.or.kr/api"

    def test_custom_base_url(self):
        """커스텀 URL 설정 가능"""
        client = OpenDartClient(api_key="test_key", base_url="http://localhost:8000")
        assert client.base_url == "http://localhost:8000"
