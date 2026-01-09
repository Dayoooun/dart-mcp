"""E2E 테스트 - 실제 OpenDART API 호출 테스트

이 테스트는 실제 OpenDART API를 호출하므로:
- API 키가 필요합니다
- 네트워크 연결이 필요합니다
- API 호출 제한에 영향을 받을 수 있습니다

실행: pytest tests/test_e2e.py -v
"""
import json
import pytest
from src.opendart_mcp.server import (
    search_disclosures,
    get_company_info,
    get_financial_account,
    get_full_financial_statement,
    get_dividend_info,
    get_executives,
    get_employees,
    get_largest_shareholders,
    get_capital_change,
    get_treasury_stock,
    get_multi_financial_account,
)


# 테스트용 상수
SAMSUNG_CORP_CODE = "00126380"  # 삼성전자
SK_HYNIX_CORP_CODE = "00164779"  # SK하이닉스
TEST_YEAR = "2023"
TEST_REPORT_CODE = "11011"  # 사업보고서


def is_valid_response(result: str) -> bool:
    """응답이 유효한지 확인 (성공 또는 데이터 없음)"""
    if "Error" not in result:
        return True
    # 013: 데이터 없음 - 유효한 응답으로 처리
    if "[013]" in result:
        return True
    return False


def parse_json_response(result: str) -> dict:
    """JSON 응답 파싱"""
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {}


class TestE2ESearchDisclosures:
    """공시 검색 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_search_by_corp_code(self):
        """기업코드로 공시 검색"""
        result = await search_disclosures(corp_code=SAMSUNG_CORP_CODE, page_count=5)
        assert is_valid_response(result), f"Unexpected error: {result}"

        if "Error" not in result:
            data = parse_json_response(result)
            assert data.get("status") == "000", "응답 상태가 정상이어야 함"
            assert "list" in data, "list 필드가 있어야 함"

    @pytest.mark.asyncio
    async def test_search_by_date_range(self):
        """날짜 범위로 공시 검색"""
        result = await search_disclosures(bgn_de="20240101", end_de="20240131", page_count=5)
        assert is_valid_response(result), f"Unexpected error: {result}"

        if "Error" not in result:
            data = parse_json_response(result)
            assert data.get("status") == "000"

    @pytest.mark.asyncio
    async def test_search_with_market_filter(self):
        """시장구분 필터로 공시 검색"""
        result = await search_disclosures(bgn_de="20240101", end_de="20240131", corp_cls="Y", page_count=5)
        assert is_valid_response(result), f"Unexpected error: {result}"


class TestE2ECompanyInfo:
    """기업정보 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_get_samsung_info(self):
        """삼성전자 기업정보 조회"""
        result = await get_company_info(corp_code=SAMSUNG_CORP_CODE)
        assert "Error" not in result, f"Unexpected error: {result}"

        data = parse_json_response(result)
        assert data.get("status") == "000", "응답 상태가 정상이어야 함"
        assert "삼성전자" in data.get("corp_name", ""), "회사명에 삼성전자가 포함되어야 함"
        assert data.get("stock_code") == "005930", "삼성전자 종목코드는 005930"
        assert data.get("corp_cls") == "Y", "삼성전자는 코스피(Y) 종목"

    @pytest.mark.asyncio
    async def test_get_sk_hynix_info(self):
        """SK하이닉스 기업정보 조회"""
        result = await get_company_info(corp_code=SK_HYNIX_CORP_CODE)
        assert "Error" not in result, f"Unexpected error: {result}"

        data = parse_json_response(result)
        assert data.get("status") == "000"
        assert "SK하이닉스" in data.get("corp_name", "") or "하이닉스" in data.get("stock_name", "")


class TestE2EFinancialAccount:
    """재무계정 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_get_samsung_financial_account(self):
        """삼성전자 주요 재무계정 조회"""
        result = await get_financial_account(
            corp_code=SAMSUNG_CORP_CODE,
            bsns_year=TEST_YEAR,
            reprt_code=TEST_REPORT_CODE,
        )
        assert is_valid_response(result), f"Unexpected error: {result}"

        if "Error" not in result:
            data = parse_json_response(result)
            assert data.get("status") == "000"
            assert "list" in data
            # 재무제표에는 자산총계, 부채총계 등이 있어야 함
            if data.get("list"):
                account_names = [item.get("account_nm", "") for item in data["list"]]
                assert len(account_names) > 0, "재무계정 항목이 있어야 함"


class TestE2EFullFinancialStatement:
    """전체 재무제표 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_get_samsung_full_statement_cfs(self):
        """삼성전자 연결재무제표 조회"""
        result = await get_full_financial_statement(
            corp_code=SAMSUNG_CORP_CODE,
            bsns_year=TEST_YEAR,
            reprt_code=TEST_REPORT_CODE,
            fs_div="CFS",  # 연결재무제표
        )
        assert is_valid_response(result), f"Unexpected error: {result}"

        if "Error" not in result:
            data = parse_json_response(result)
            assert data.get("status") == "000"
            assert "list" in data

    @pytest.mark.asyncio
    async def test_get_samsung_full_statement_ofs(self):
        """삼성전자 개별재무제표 조회"""
        result = await get_full_financial_statement(
            corp_code=SAMSUNG_CORP_CODE,
            bsns_year=TEST_YEAR,
            reprt_code=TEST_REPORT_CODE,
            fs_div="OFS",  # 개별재무제표
        )
        assert is_valid_response(result), f"Unexpected error: {result}"


class TestE2EDividendInfo:
    """배당정보 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_get_samsung_dividend(self):
        """삼성전자 배당정보 조회"""
        result = await get_dividend_info(
            corp_code=SAMSUNG_CORP_CODE,
            bsns_year=TEST_YEAR,
            reprt_code=TEST_REPORT_CODE,
        )
        assert is_valid_response(result), f"Unexpected error: {result}"

        if "Error" not in result:
            data = parse_json_response(result)
            assert data.get("status") == "000"
            assert "list" in data


class TestE2EExecutives:
    """임원현황 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_get_samsung_executives(self):
        """삼성전자 임원현황 조회"""
        result = await get_executives(
            corp_code=SAMSUNG_CORP_CODE,
            bsns_year=TEST_YEAR,
            reprt_code=TEST_REPORT_CODE,
        )
        assert is_valid_response(result), f"Unexpected error: {result}"

        if "Error" not in result:
            data = parse_json_response(result)
            assert data.get("status") == "000"
            assert "list" in data
            # 임원 목록이 있어야 함
            if data.get("list"):
                assert len(data["list"]) > 0, "임원 목록이 있어야 함"


class TestE2EEmployees:
    """직원현황 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_get_samsung_employees(self):
        """삼성전자 직원현황 조회"""
        result = await get_employees(
            corp_code=SAMSUNG_CORP_CODE,
            bsns_year=TEST_YEAR,
            reprt_code=TEST_REPORT_CODE,
        )
        assert is_valid_response(result), f"Unexpected error: {result}"

        if "Error" not in result:
            data = parse_json_response(result)
            assert data.get("status") == "000"
            assert "list" in data


class TestE2ELargestShareholders:
    """최대주주 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_get_samsung_shareholders(self):
        """삼성전자 최대주주 조회"""
        result = await get_largest_shareholders(
            corp_code=SAMSUNG_CORP_CODE,
            bsns_year=TEST_YEAR,
            reprt_code=TEST_REPORT_CODE,
        )
        assert is_valid_response(result), f"Unexpected error: {result}"

        if "Error" not in result:
            data = parse_json_response(result)
            assert data.get("status") == "000"
            assert "list" in data


class TestE2ECapitalChange:
    """증자감자 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_get_samsung_capital_change(self):
        """삼성전자 증자감자현황 조회"""
        result = await get_capital_change(
            corp_code=SAMSUNG_CORP_CODE,
            bsns_year=TEST_YEAR,
            reprt_code=TEST_REPORT_CODE,
        )
        assert is_valid_response(result), f"Unexpected error: {result}"


class TestE2ETreasuryStock:
    """자기주식 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_get_samsung_treasury_stock(self):
        """삼성전자 자기주식현황 조회"""
        result = await get_treasury_stock(
            corp_code=SAMSUNG_CORP_CODE,
            bsns_year=TEST_YEAR,
            reprt_code=TEST_REPORT_CODE,
        )
        assert is_valid_response(result), f"Unexpected error: {result}"


class TestE2EMultiFinancialAccount:
    """다중기업 재무계정 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_get_multi_company_financial(self):
        """삼성전자 + SK하이닉스 재무계정 조회"""
        result = await get_multi_financial_account(
            corp_codes=[SAMSUNG_CORP_CODE, SK_HYNIX_CORP_CODE],
            bsns_year=TEST_YEAR,
            reprt_code=TEST_REPORT_CODE,
        )
        assert is_valid_response(result), f"Unexpected error: {result}"

        if "Error" not in result:
            data = parse_json_response(result)
            assert data.get("status") == "000"
            assert "list" in data


class TestE2EErrorHandling:
    """에러 처리 E2E 테스트"""

    @pytest.mark.asyncio
    async def test_invalid_corp_code(self):
        """잘못된 기업코드로 조회시 에러 처리"""
        result = await get_company_info(corp_code="99999999")
        # 에러가 발생해야 하지만, 서버가 크래시 나지 않아야 함
        assert isinstance(result, str), "결과는 문자열이어야 함"

    @pytest.mark.asyncio
    async def test_search_without_params(self):
        """파라미터 없이 검색시 에러 처리"""
        result = await search_disclosures()
        # 검색 조건이 없으면 에러가 발생해야 함
        assert "Error" in result or "status" in result
