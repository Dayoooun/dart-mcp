"""OpenDART MCP Server - Korean FSS Electronic Disclosure System API (Streamable HTTP)

MCP Protocol Version: 2025-03-26
Transport: Streamable HTTP (stateless)
"""
import os
import contextlib
from typing import Optional, List

import uvicorn
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount, Route
from starlette.requests import Request
from starlette.responses import JSONResponse

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from .api.disclosure import DisclosureAPI
from .api.financial import FinancialAPI
from .api.report import ReportAPI
from .exceptions import OpenDartException


DEFAULT_API_KEY = "d64dadc7b8236e0ae2e6c3560ef400cc12f2c705"

# 주요 기업 고유번호 (corp_code) 참조
COMPANY_CODES = """주요 기업 고유번호 (corp_code):
- 삼성전자: 00126380
- SK하이닉스: 00164779
- LG전자: 00401731
- 현대자동차: 00164742
- 네이버: 00266961
- 카카오: 00258801
- 삼성SDI: 00126371
- LG화학: 00356361"""

# Transport security 설정 (Remote MCP 서버용 - DNS rebinding 보호 비활성화)
transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False,
)

# FastMCP 서버 생성 (stateless + JSON response)
mcp = FastMCP(
    "OpenDART MCP Server",
    stateless_http=True,
    json_response=True,
    transport_security=transport_security,
)
# MCP 엔드포인트 경로를 루트로 설정 (Mount 경로가 /mcp이므로 최종 경로는 /mcp)
mcp.settings.streamable_http_path = "/"

# API 클라이언트 (lazy initialization)
_api_key: Optional[str] = None
_disclosure_api: Optional[DisclosureAPI] = None
_financial_api: Optional[FinancialAPI] = None
_report_api: Optional[ReportAPI] = None


def get_api_key() -> str:
    """API 키 반환"""
    global _api_key
    if _api_key is None:
        _api_key = os.environ.get("OPENDART_API_KEY", DEFAULT_API_KEY)
    return _api_key


def get_disclosure_api() -> DisclosureAPI:
    """DisclosureAPI 인스턴스 반환"""
    global _disclosure_api
    if _disclosure_api is None:
        _disclosure_api = DisclosureAPI(api_key=get_api_key())
    return _disclosure_api


def get_financial_api() -> FinancialAPI:
    """FinancialAPI 인스턴스 반환"""
    global _financial_api
    if _financial_api is None:
        _financial_api = FinancialAPI(api_key=get_api_key())
    return _financial_api


def get_report_api() -> ReportAPI:
    """ReportAPI 인스턴스 반환"""
    global _report_api
    if _report_api is None:
        _report_api = ReportAPI(api_key=get_api_key())
    return _report_api


# ============================================================================
# Tools
# ============================================================================


@mcp.tool(
    description=f"""한국 상장기업 공시 검색 (Search Korean company disclosures)

검색 조건 중 최소 하나 필수: corp_code, bgn_de, end_de

{COMPANY_CODES}

예시:
- 삼성전자 공시 검색: corp_code="00126380"
- 2024년 1월 공시: bgn_de="20240101", end_de="20240131"
- 코스피 공시만: corp_cls="Y"
"""
)
async def search_disclosures(
    corp_code: Optional[str] = None,
    bgn_de: Optional[str] = None,
    end_de: Optional[str] = None,
    corp_cls: Optional[str] = None,
    page_no: int = 1,
    page_count: int = 10,
) -> str:
    """공시 검색

    Args:
        corp_code: 기업 고유번호 8자리 (예: 00126380=삼성전자)
        bgn_de: 검색 시작일 YYYYMMDD (예: 20240101)
        end_de: 검색 종료일 YYYYMMDD (예: 20240131)
        corp_cls: 시장구분 Y=코스피, K=코스닥, N=코넥스, E=기타
        page_no: 페이지 번호 (기본값: 1)
        page_count: 페이지당 건수 (기본값: 10, 최대: 100)
    """
    try:
        result = await get_disclosure_api().search(
            corp_code=corp_code,
            bgn_de=bgn_de,
            end_de=end_de,
            corp_cls=corp_cls,
            page_no=page_no,
            page_count=page_count,
        )
        return result.model_dump_json(indent=2)
    except OpenDartException as e:
        return f"Error [{e.code}]: {e.message}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(
    description=f"""기업 기본정보 조회 (Get company basic info)

회사명, 대표자, 주소, 업종, 설립일 등 기본 정보 반환

{COMPANY_CODES}

예시: corp_code="00126380" (삼성전자)
"""
)
async def get_company_info(corp_code: str) -> str:
    """기업 기본정보 조회

    Args:
        corp_code: 기업 고유번호 8자리 (예: 00126380=삼성전자)
    """
    try:
        result = await get_disclosure_api().get_company(corp_code=corp_code)
        return result.model_dump_json(indent=2)
    except OpenDartException as e:
        return f"Error [{e.code}]: {e.message}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(
    description=f"""기업 주요 재무계정 조회 (Get key financial accounts)

자산총계, 부채총계, 자본총계, 매출액, 영업이익, 당기순이익 등

{COMPANY_CODES}

보고서 코드 (reprt_code):
- 11011: 사업보고서 (연간)
- 11012: 반기보고서
- 11013: 1분기보고서
- 11014: 3분기보고서

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
"""
)
async def get_financial_account(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    fs_div: Optional[str] = None,
) -> str:
    """기업 주요 재무계정 조회

    Args:
        corp_code: 기업 고유번호 8자리
        bsns_year: 사업연도 YYYY (예: 2023)
        reprt_code: 보고서코드 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기
        fs_div: 재무제표 구분 OFS=개별, CFS=연결 (기본값: 연결)
    """
    try:
        result = await get_financial_api().get_single_account(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
            fs_div=fs_div,
        )
        return result.model_dump_json(indent=2)
    except OpenDartException as e:
        return f"Error [{e.code}]: {e.message}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(
    description=f"""기업 전체 재무제표 조회 (Get full financial statements)

재무상태표, 손익계산서, 현금흐름표 등 전체 재무제표 항목

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
"""
)
async def get_full_financial_statement(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    fs_div: Optional[str] = None,
) -> str:
    """기업 전체 재무제표 조회

    Args:
        corp_code: 기업 고유번호 8자리
        bsns_year: 사업연도 YYYY (예: 2023)
        reprt_code: 보고서코드 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기
        fs_div: 재무제표 구분 OFS=개별, CFS=연결
    """
    try:
        result = await get_financial_api().get_full_statement(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
            fs_div=fs_div,
        )
        return result.model_dump_json(indent=2)
    except OpenDartException as e:
        return f"Error [{e.code}]: {e.message}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(
    description=f"""기업 배당 정보 조회 (Get dividend information)

주당배당금, 배당수익률, 배당성향 등 배당 관련 정보

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
"""
)
async def get_dividend_info(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
) -> str:
    """기업 배당 정보 조회

    Args:
        corp_code: 기업 고유번호 8자리
        bsns_year: 사업연도 YYYY (예: 2023)
        reprt_code: 보고서코드 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기
    """
    try:
        result = await get_report_api().get_dividend(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
        )
        return result.model_dump_json(indent=2)
    except OpenDartException as e:
        return f"Error [{e.code}]: {e.message}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(
    description=f"""기업 임원 현황 조회 (Get executive information)

대표이사, 이사, 감사 등 임원 명단과 경력 정보

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
"""
)
async def get_executives(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
) -> str:
    """기업 임원 현황 조회

    Args:
        corp_code: 기업 고유번호 8자리
        bsns_year: 사업연도 YYYY (예: 2023)
        reprt_code: 보고서코드 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기
    """
    try:
        result = await get_report_api().get_executives(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
        )
        return result.model_dump_json(indent=2)
    except OpenDartException as e:
        return f"Error [{e.code}]: {e.message}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(
    description=f"""기업 직원 현황 조회 (Get employee statistics)

직원수, 평균근속연수, 평균급여 등 직원 통계

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
"""
)
async def get_employees(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
) -> str:
    """기업 직원 현황 조회

    Args:
        corp_code: 기업 고유번호 8자리
        bsns_year: 사업연도 YYYY (예: 2023)
        reprt_code: 보고서코드 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기
    """
    try:
        result = await get_report_api().get_employees(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
        )
        return result.model_dump_json(indent=2)
    except OpenDartException as e:
        return f"Error [{e.code}]: {e.message}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(
    description=f"""기업 최대주주 현황 조회 (Get largest shareholders)

최대주주, 특수관계인 지분율 및 주식 보유 현황

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
"""
)
async def get_largest_shareholders(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
) -> str:
    """기업 최대주주 현황 조회

    Args:
        corp_code: 기업 고유번호 8자리
        bsns_year: 사업연도 YYYY (예: 2023)
        reprt_code: 보고서코드 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기
    """
    try:
        result = await get_report_api().get_largest_shareholders(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
        )
        return result.model_dump_json(indent=2)
    except OpenDartException as e:
        return f"Error [{e.code}]: {e.message}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(
    description=f"""기업 증자(감자) 현황 조회 (Get capital increase/decrease history)

주식발행(감소)일자, 발행(감소)형태, 주식종류, 수량, 액면가액 등

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
"""
)
async def get_capital_change(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
) -> str:
    """기업 증자(감자) 현황 조회

    Args:
        corp_code: 기업 고유번호 8자리
        bsns_year: 사업연도 YYYY (예: 2023)
        reprt_code: 보고서코드 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기
    """
    try:
        result = await get_report_api().get_capital_change(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
        )
        return result.model_dump_json(indent=2)
    except OpenDartException as e:
        return f"Error [{e.code}]: {e.message}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(
    description=f"""기업 자기주식 취득/처분 현황 조회 (Get treasury stock status)

자기주식 취득방법, 주식종류, 기초/기말 수량, 취득/처분/소각 변동 등

{COMPANY_CODES}

예시: corp_code="00126380", bsns_year="2023", reprt_code="11011"
"""
)
async def get_treasury_stock(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
) -> str:
    """기업 자기주식 취득/처분 현황 조회

    Args:
        corp_code: 기업 고유번호 8자리
        bsns_year: 사업연도 YYYY (예: 2023)
        reprt_code: 보고서코드 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기
    """
    try:
        result = await get_report_api().get_treasury_stock(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
        )
        return result.model_dump_json(indent=2)
    except OpenDartException as e:
        return f"Error [{e.code}]: {e.message}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(
    description=f"""다중회사 주요계정 조회 (Get multiple companies' key financial accounts)

여러 기업의 주요 재무계정을 한번에 조회 (최대 100개 기업)

{COMPANY_CODES}

예시: corp_codes=["00126380", "00164779"], bsns_year="2023", reprt_code="11011"
"""
)
async def get_multi_financial_account(
    corp_codes: List[str],
    bsns_year: str,
    reprt_code: str,
    fs_div: Optional[str] = None,
) -> str:
    """다중회사 주요계정 조회

    Args:
        corp_codes: 기업 고유번호 목록 (최대 100개)
        bsns_year: 사업연도 YYYY (예: 2023)
        reprt_code: 보고서코드 11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기
        fs_div: 재무제표 구분 OFS=개별, CFS=연결 (기본값: 연결)
    """
    try:
        result = await get_financial_api().get_multi_account(
            corp_code=corp_codes,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
            fs_div=fs_div,
        )
        return result.model_dump_json(indent=2)
    except OpenDartException as e:
        return f"Error [{e.code}]: {e.message}"
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# Custom HTTP Endpoints
# ============================================================================


async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for load balancers and monitoring"""
    return JSONResponse({
        "status": "healthy",
        "service": "opendart-mcp",
        "version": "0.2.0",
        "protocol_version": "2025-03-26",
        "transport": "streamable-http",
    })


async def info(request: Request) -> JSONResponse:
    """Server information endpoint"""
    return JSONResponse({
        "name": "OpenDART MCP Server",
        "description": "Korean FSS Electronic Disclosure API MCP Server",
        "version": "0.2.0",
        "mcp_protocol_version": "2025-03-26",
        "transport": "streamable-http",
        "stateless": True,
        "tools_count": 11,
        "company_codes": {
            "삼성전자": "00126380",
            "SK하이닉스": "00164779",
            "LG전자": "00401731",
            "현대자동차": "00164742",
            "네이버": "00266961",
            "카카오": "00258801",
            "삼성SDI": "00126371",
            "LG화학": "00356361",
        },
    })


# ============================================================================
# Application Factory
# ============================================================================


def create_app() -> Starlette:
    """Create Starlette application with MCP server mounted"""

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette):
        async with mcp.session_manager.run():
            yield

    # Create Starlette app with routes
    app = Starlette(
        routes=[
            Route("/health", health_check, methods=["GET"]),
            Route("/info", info, methods=["GET"]),
            Mount("/mcp", app=mcp.streamable_http_app()),
        ],
        lifespan=lifespan,
    )

    # Add CORS middleware for browser clients
    app = CORSMiddleware(
        app,
        allow_origins=["*"],
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["Mcp-Session-Id"],
    )

    return app


# Create the ASGI application
app = create_app()


def main():
    """Main entry point - run server with uvicorn"""
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))

    print(f"Starting OpenDART MCP Server...")
    print(f"  Protocol Version: 2025-03-26")
    print(f"  Transport: Streamable HTTP (stateless)")
    print(f"  MCP Endpoint: http://{host}:{port}/mcp")
    print(f"  Health Check: http://{host}:{port}/health")
    print(f"  Server Info: http://{host}:{port}/info")

    uvicorn.run(
        "opendart_mcp.server:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
