"""MCP 서버 테스트"""
import pytest
from starlette.testclient import TestClient
from src.opendart_mcp.server import app, mcp


class TestMCPServer:
    """MCP 서버 테스트"""

    def test_app_created(self):
        """앱 생성 확인"""
        assert app is not None

    def test_mcp_server_created(self):
        """MCP 서버 생성 확인"""
        assert mcp is not None
        assert mcp.name == "OpenDART MCP Server"

    def test_health_check_endpoint(self):
        """헬스 체크 엔드포인트 테스트"""
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "opendart-mcp"
        assert data["protocol_version"] == "2025-03-26"
        assert data["transport"] == "streamable-http"

    def test_info_endpoint(self):
        """서버 정보 엔드포인트 테스트"""
        client = TestClient(app)
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "OpenDART MCP Server"
        assert data["mcp_protocol_version"] == "2025-03-26"
        assert data["transport"] == "streamable-http"
        assert data["stateless"] is True
        assert data["tools_count"] == 11
        assert "삼성전자" in data["company_codes"]

    def test_mcp_endpoint_exists(self):
        """MCP 엔드포인트 존재 확인"""
        # TestClient에서 lifespan context가 제대로 작동하도록 설정
        with TestClient(app, raise_server_exceptions=False) as client:
            # MCP endpoint should respond (might need proper MCP request format)
            response = client.post(
                "/mcp",
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {},
                        "clientInfo": {
                            "name": "test-client",
                            "version": "1.0.0"
                        }
                    }
                },
                headers={
                    "Accept": "application/json, text/event-stream",
                    "Content-Type": "application/json"
                }
            )
            # Should return 200 with a valid MCP response
            assert response.status_code == 200

    def test_tools_registered(self):
        """도구 등록 확인"""
        # FastMCP에서 도구 목록 확인
        tools = mcp._tool_manager.list_tools()
        tool_names = [t.name for t in tools]

        expected_tools = [
            "search_disclosures",
            "get_company_info",
            "get_financial_account",
            "get_full_financial_statement",
            "get_dividend_info",
            "get_executives",
            "get_employees",
            "get_largest_shareholders",
            "get_capital_change",
            "get_treasury_stock",
            "get_multi_financial_account",
        ]

        for tool in expected_tools:
            assert tool in tool_names, f"Tool '{tool}' not found in registered tools"
