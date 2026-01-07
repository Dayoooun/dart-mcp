"""MCP 서버 테스트"""
import pytest
from src.opendart_mcp.server import create_server


class TestMCPServer:
    """MCP 서버 테스트"""

    def test_server_created(self):
        """서버 생성"""
        server = create_server()
        assert server is not None

    def test_server_has_name(self):
        """서버 이름 확인"""
        server = create_server()
        assert server.name == "opendart-mcp"

    def test_server_has_request_handlers(self):
        """서버 요청 핸들러 등록 확인"""
        server = create_server()
        # MCP 서버는 요청 핸들러가 등록되어 있어야 함
        assert server.request_handlers is not None
        assert len(server.request_handlers) > 0
