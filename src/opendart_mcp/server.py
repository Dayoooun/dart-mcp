"""OpenDART MCP Server - Korean FSS Electronic Disclosure System API"""
import os
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .api.disclosure import DisclosureAPI
from .api.financial import FinancialAPI
from .api.report import ReportAPI


DEFAULT_API_KEY = "d64dadc7b8236e0ae2e6c3560ef400cc12f2c705"

# 주요 기업 고유번호 (corp_code) 참조
COMPANY_CODES = """
주요 기업 고유번호 (corp_code):
- 삼성전자: 00126380
- SK하이닉스: 00164779
- LG전자: 00401731
- 현대자동차: 00164742
- 네이버: 00266961
- 카카오: 00258801
- 삼성SDI: 00126371
- LG화학: 00356361
"""


def create_server() -> Server:
    """MCP 서버 생성"""
    server = Server("opendart-mcp")

    api_key = os.environ.get("OPENDART_API_KEY", DEFAULT_API_KEY)

    # API 클라이언트 생성
    disclosure_api = DisclosureAPI(api_key=api_key) if api_key else None
    financial_api = FinancialAPI(api_key=api_key) if api_key else None
    report_api = ReportAPI(api_key=api_key) if api_key else None

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """사용 가능한 도구 목록 반환"""
        return [
            Tool(
                name="search_disclosures",
                description=f"""한국 상장기업 공시 검색 (Search Korean company disclosures)

검색 조건 중 최소 하나 필수: corp_code, bgn_de, end_de

{COMPANY_CODES}

예시:
- 삼성전자 공시 검색: corp_code="00126380"
- 2024년 1월 공시: bgn_de="20240101", end_de="20240131"
- 코스피 공시만: corp_cls="Y"
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "corp_code": {
                            "type": "string",
                            "description": "기업 고유번호 8자리 (예: 00126380=삼성전자)",
                        },
                        "bgn_de": {
                            "type": "string",
                            "description": "검색 시작일 YYYYMMDD (예: 20240101)",
                        },
                        "end_de": {
                            "type": "string",
                            "description": "검색 종료일 YYYYMMDD (예: 20240131)",
                        },
                        "corp_cls": {
                            "type": "string",
                            "description": "시장구분: Y=코스피, K=코스닥, N=코넥스, E=기타",
                            "enum": ["Y", "K", "N", "E"],
                        },
                        "page_no": {
                            "type": "integer",
                            "description": "페이지 번호 (기본값: 1)",
                            "default": 1,
                        },
                        "page_count": {
                            "type": "integer",
                            "description": "페이지당 건수 (기본값: 10, 최대: 100)",
                            "default": 10,
                        },
                    },
                },
            ),
            Tool(
                name="get_company_info",
                description=f"""기업 기본정보 조회 (Get company basic info)

회사명, 대표자, 주소, 업종, 설립일 등 기본 정보 반환

{COMPANY_CODES}

예시: corp_code="00126380" (삼성전자)
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "corp_code": {
                            "type": "string",
                            "description": "기업 고유번호 8자리 (예: 00126380=삼성전자)",
                        },
                    },
                    "required": ["corp_code"],
                },
            ),
            Tool(
                name="get_financial_account",
                description=f"""기업 주요 재무계정 조회 (Get key financial accounts)

자산총계, 부채총계, 자본총계, 매출액, 영업이익, 당기순이익 등

{COMPANY_CODES}

보고서 코드 (reprt_code):
- 11011: 사업보고서 (연간)
- 11012: 반기보고서
- 11013: 1분기보고서
- 11014: 3분기보고서

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "corp_code": {
                            "type": "string",
                            "description": "기업 고유번호 8자리",
                        },
                        "bsns_year": {
                            "type": "string",
                            "description": "사업연도 YYYY (예: 2023)",
                        },
                        "reprt_code": {
                            "type": "string",
                            "description": "보고서코드: 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기",
                            "enum": ["11011", "11012", "11013", "11014"],
                        },
                        "fs_div": {
                            "type": "string",
                            "description": "재무제표 구분: OFS=개별, CFS=연결 (기본값: 연결)",
                            "enum": ["OFS", "CFS"],
                        },
                    },
                    "required": ["corp_code", "bsns_year", "reprt_code"],
                },
            ),
            Tool(
                name="get_full_financial_statement",
                description=f"""기업 전체 재무제표 조회 (Get full financial statements)

재무상태표, 손익계산서, 현금흐름표 등 전체 재무제표 항목

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "corp_code": {
                            "type": "string",
                            "description": "기업 고유번호 8자리",
                        },
                        "bsns_year": {
                            "type": "string",
                            "description": "사업연도 YYYY (예: 2023)",
                        },
                        "reprt_code": {
                            "type": "string",
                            "description": "보고서코드: 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기",
                            "enum": ["11011", "11012", "11013", "11014"],
                        },
                        "fs_div": {
                            "type": "string",
                            "description": "재무제표 구분: OFS=개별, CFS=연결",
                            "enum": ["OFS", "CFS"],
                        },
                    },
                    "required": ["corp_code", "bsns_year", "reprt_code"],
                },
            ),
            Tool(
                name="get_dividend_info",
                description=f"""기업 배당 정보 조회 (Get dividend information)

주당배당금, 배당수익률, 배당성향 등 배당 관련 정보

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "corp_code": {
                            "type": "string",
                            "description": "기업 고유번호 8자리",
                        },
                        "bsns_year": {
                            "type": "string",
                            "description": "사업연도 YYYY (예: 2023)",
                        },
                        "reprt_code": {
                            "type": "string",
                            "description": "보고서코드: 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기",
                            "enum": ["11011", "11012", "11013", "11014"],
                        },
                    },
                    "required": ["corp_code", "bsns_year", "reprt_code"],
                },
            ),
            Tool(
                name="get_executives",
                description=f"""기업 임원 현황 조회 (Get executive information)

대표이사, 이사, 감사 등 임원 명단과 경력 정보

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "corp_code": {
                            "type": "string",
                            "description": "기업 고유번호 8자리",
                        },
                        "bsns_year": {
                            "type": "string",
                            "description": "사업연도 YYYY (예: 2023)",
                        },
                        "reprt_code": {
                            "type": "string",
                            "description": "보고서코드: 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기",
                            "enum": ["11011", "11012", "11013", "11014"],
                        },
                    },
                    "required": ["corp_code", "bsns_year", "reprt_code"],
                },
            ),
            Tool(
                name="get_employees",
                description=f"""기업 직원 현황 조회 (Get employee statistics)

직원수, 평균근속연수, 평균급여 등 직원 통계

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "corp_code": {
                            "type": "string",
                            "description": "기업 고유번호 8자리",
                        },
                        "bsns_year": {
                            "type": "string",
                            "description": "사업연도 YYYY (예: 2023)",
                        },
                        "reprt_code": {
                            "type": "string",
                            "description": "보고서코드: 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기",
                            "enum": ["11011", "11012", "11013", "11014"],
                        },
                    },
                    "required": ["corp_code", "bsns_year", "reprt_code"],
                },
            ),
            Tool(
                name="get_largest_shareholders",
                description=f"""기업 최대주주 현황 조회 (Get largest shareholders)

최대주주, 특수관계인 지분율 및 주식 보유 현황

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "corp_code": {
                            "type": "string",
                            "description": "기업 고유번호 8자리",
                        },
                        "bsns_year": {
                            "type": "string",
                            "description": "사업연도 YYYY (예: 2023)",
                        },
                        "reprt_code": {
                            "type": "string",
                            "description": "보고서코드: 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기",
                            "enum": ["11011", "11012", "11013", "11014"],
                        },
                    },
                    "required": ["corp_code", "bsns_year", "reprt_code"],
                },
            ),
            Tool(
                name="get_capital_change",
                description=f"""기업 증자(감자) 현황 조회 (Get capital increase/decrease history)

주식발행(감소)일자, 발행(감소)형태, 주식종류, 수량, 액면가액 등

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "corp_code": {
                            "type": "string",
                            "description": "기업 고유번호 8자리",
                        },
                        "bsns_year": {
                            "type": "string",
                            "description": "사업연도 YYYY (예: 2023)",
                        },
                        "reprt_code": {
                            "type": "string",
                            "description": "보고서코드: 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기",
                            "enum": ["11011", "11012", "11013", "11014"],
                        },
                    },
                    "required": ["corp_code", "bsns_year", "reprt_code"],
                },
            ),
            Tool(
                name="get_treasury_stock",
                description=f"""기업 자기주식 취득/처분 현황 조회 (Get treasury stock status)

자기주식 취득방법, 주식종류, 기초/기말 수량, 취득/처분/소각 변동 등

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "corp_code": {
                            "type": "string",
                            "description": "기업 고유번호 8자리",
                        },
                        "bsns_year": {
                            "type": "string",
                            "description": "사업연도 YYYY (예: 2023)",
                        },
                        "reprt_code": {
                            "type": "string",
                            "description": "보고서코드: 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기",
                            "enum": ["11011", "11012", "11013", "11014"],
                        },
                    },
                    "required": ["corp_code", "bsns_year", "reprt_code"],
                },
            ),
            Tool(
                name="get_multi_financial_account",
                description=f"""다중회사 주요계정 조회 (Get multiple companies' key financial accounts)

여러 기업의 주요 재무계정을 한번에 조회 (최대 100개 기업)

{COMPANY_CODES}

예시: corp_code=["00126380", "00164779"], bsns_year="2023", reprt_code="11011"
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "corp_code": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "기업 고유번호 목록 (최대 100개)",
                        },
                        "bsns_year": {
                            "type": "string",
                            "description": "사업연도 YYYY (예: 2023)",
                        },
                        "reprt_code": {
                            "type": "string",
                            "description": "보고서코드: 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기",
                            "enum": ["11011", "11012", "11013", "11014"],
                        },
                        "fs_div": {
                            "type": "string",
                            "description": "재무제표 구분: OFS=개별, CFS=연결 (기본값: 연결)",
                            "enum": ["OFS", "CFS"],
                        },
                    },
                    "required": ["corp_code", "bsns_year", "reprt_code"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """도구 실행"""
        if not api_key:
            return [TextContent(type="text", text="Error: API 키가 설정되지 않았습니다")]

        try:
            if name == "search_disclosures":
                result = await disclosure_api.search(
                    corp_code=arguments.get("corp_code"),
                    bgn_de=arguments.get("bgn_de"),
                    end_de=arguments.get("end_de"),
                    corp_cls=arguments.get("corp_cls"),
                    page_no=arguments.get("page_no", 1),
                    page_count=arguments.get("page_count", 10),
                )
                return [TextContent(type="text", text=result.model_dump_json(indent=2))]

            elif name == "get_company_info":
                result = await disclosure_api.get_company(
                    corp_code=arguments["corp_code"],
                )
                return [TextContent(type="text", text=result.model_dump_json(indent=2))]

            elif name == "get_financial_account":
                result = await financial_api.get_single_account(
                    corp_code=arguments["corp_code"],
                    bsns_year=arguments["bsns_year"],
                    reprt_code=arguments["reprt_code"],
                    fs_div=arguments.get("fs_div"),
                )
                return [TextContent(type="text", text=result.model_dump_json(indent=2))]

            elif name == "get_full_financial_statement":
                result = await financial_api.get_full_statement(
                    corp_code=arguments["corp_code"],
                    bsns_year=arguments["bsns_year"],
                    reprt_code=arguments["reprt_code"],
                    fs_div=arguments.get("fs_div"),
                )
                return [TextContent(type="text", text=result.model_dump_json(indent=2))]

            elif name == "get_dividend_info":
                result = await report_api.get_dividend(
                    corp_code=arguments["corp_code"],
                    bsns_year=arguments["bsns_year"],
                    reprt_code=arguments["reprt_code"],
                )
                return [TextContent(type="text", text=result.model_dump_json(indent=2))]

            elif name == "get_executives":
                result = await report_api.get_executives(
                    corp_code=arguments["corp_code"],
                    bsns_year=arguments["bsns_year"],
                    reprt_code=arguments["reprt_code"],
                )
                return [TextContent(type="text", text=result.model_dump_json(indent=2))]

            elif name == "get_employees":
                result = await report_api.get_employees(
                    corp_code=arguments["corp_code"],
                    bsns_year=arguments["bsns_year"],
                    reprt_code=arguments["reprt_code"],
                )
                return [TextContent(type="text", text=result.model_dump_json(indent=2))]

            elif name == "get_largest_shareholders":
                result = await report_api.get_largest_shareholders(
                    corp_code=arguments["corp_code"],
                    bsns_year=arguments["bsns_year"],
                    reprt_code=arguments["reprt_code"],
                )
                return [TextContent(type="text", text=result.model_dump_json(indent=2))]

            elif name == "get_capital_change":
                result = await report_api.get_capital_change(
                    corp_code=arguments["corp_code"],
                    bsns_year=arguments["bsns_year"],
                    reprt_code=arguments["reprt_code"],
                )
                return [TextContent(type="text", text=result.model_dump_json(indent=2))]

            elif name == "get_treasury_stock":
                result = await report_api.get_treasury_stock(
                    corp_code=arguments["corp_code"],
                    bsns_year=arguments["bsns_year"],
                    reprt_code=arguments["reprt_code"],
                )
                return [TextContent(type="text", text=result.model_dump_json(indent=2))]

            elif name == "get_multi_financial_account":
                result = await financial_api.get_multi_account(
                    corp_code=arguments["corp_code"],
                    bsns_year=arguments["bsns_year"],
                    reprt_code=arguments["reprt_code"],
                    fs_div=arguments.get("fs_div"),
                )
                return [TextContent(type="text", text=result.model_dump_json(indent=2))]

            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    return server


async def _async_main():
    """비동기 메인 함수"""
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    """메인 함수 (엔트리포인트)"""
    import asyncio
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
