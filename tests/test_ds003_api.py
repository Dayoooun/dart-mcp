"""DS003 재무정보 API 테스트"""
import pytest
from pydantic import ValidationError
from src.opendart_mcp.models.ds003 import (
    FinancialAccountItem,
    SingleCompanyAccountResponse,
    MultiCompanyAccountResponse,
    FinancialStatementItem,
    FullFinancialStatementResponse,
)
from src.opendart_mcp.api.financial import FinancialAPI


class TestSingleCompanyAccountResponse:
    """단일회사 주요계정 응답 모델 테스트"""

    def test_parses_valid_response(self):
        """유효한 응답 파싱"""
        data = {
            "status": "000",
            "message": "정상",
            "list": [
                {
                    "rcept_no": "20240515000001",
                    "bsns_year": "2024",
                    "corp_code": "00126380",
                    "stock_code": "005930",
                    "reprt_code": "11013",
                    "account_nm": "자산총계",
                    "fs_div": "OFS",
                    "fs_nm": "재무제표",
                    "sj_div": "BS",
                    "sj_nm": "재무상태표",
                    "thstrm_nm": "제55기",
                    "thstrm_dt": "2024.03.31 현재",
                    "thstrm_amount": "478,231,123,456",
                    "frmtrm_nm": "제54기",
                    "frmtrm_dt": "2023.12.31 현재",
                    "frmtrm_amount": "455,123,456,789",
                    "bfefrmtrm_nm": "제53기",
                    "bfefrmtrm_dt": "2022.12.31 현재",
                    "bfefrmtrm_amount": "426,789,123,456",
                    "ord": "1",
                }
            ],
        }

        response = SingleCompanyAccountResponse(**data)

        assert response.status == "000"
        assert len(response.list) == 1
        assert response.list[0].account_nm == "자산총계"
        assert response.list[0].thstrm_amount == "478,231,123,456"

    def test_handles_empty_list(self):
        """빈 목록 처리"""
        data = {
            "status": "013",
            "message": "조회된 데이터가 없습니다",
            "list": [],
        }

        response = SingleCompanyAccountResponse(**data)
        assert response.list == []


class TestMultiCompanyAccountResponse:
    """다중회사 주요계정 응답 모델 테스트"""

    def test_parses_valid_response(self):
        """유효한 응답 파싱"""
        data = {
            "status": "000",
            "message": "정상",
            "list": [
                {
                    "rcept_no": "20240315000123",
                    "corp_code": "00126380",
                    "corp_name": "삼성전자",
                    "stock_code": "005930",
                    "bsns_year": "2024",
                    "reprt_code": "11013",
                    "account_nm": "자산총계",
                    "fs_div": "OFS",
                    "fs_nm": "재무제표",
                    "sj_div": "BS",
                    "sj_nm": "재무상태표",
                    "thstrm_nm": "제55기",
                    "thstrm_amount": "478,231,123,456",
                }
            ],
        }

        response = MultiCompanyAccountResponse(**data)

        assert response.status == "000"
        assert len(response.list) == 1
        assert response.list[0].corp_name == "삼성전자"


class TestFullFinancialStatementResponse:
    """단일회사 전체 재무제표 응답 모델 테스트"""

    def test_parses_valid_response(self):
        """유효한 응답 파싱"""
        data = {
            "status": "000",
            "message": "정상",
            "list": [
                {
                    "rcept_no": "20240515000001",
                    "reprt_code": "11013",
                    "bsns_year": "2024",
                    "corp_code": "00126380",
                    "sj_div": "BS",
                    "sj_nm": "재무상태표",
                    "account_id": "dart_CurrentAssets",
                    "account_nm": "유동자산",
                    "account_detail": "-",
                    "thstrm_nm": "제55기",
                    "thstrm_amount": "123,456,789,000",
                    "frmtrm_nm": "제54기",
                    "frmtrm_amount": "112,345,678,000",
                    "bfefrmtrm_nm": "제53기",
                    "bfefrmtrm_amount": "101,234,567,000",
                    "ord": "1",
                }
            ],
        }

        response = FullFinancialStatementResponse(**data)

        assert response.status == "000"
        assert len(response.list) == 1
        assert response.list[0].account_nm == "유동자산"
        assert response.list[0].sj_nm == "재무상태표"


class TestFinancialAPI:
    """재무정보 API 테스트"""

    def test_requires_corp_code_for_single_account(self):
        """단일회사 조회 시 corp_code 필수"""
        api = FinancialAPI(api_key="test_key")

        with pytest.raises(ValueError, match="corp_code"):
            api.validate_single_account_params(
                corp_code="",
                bsns_year="2024",
                reprt_code="11013",
            )

    def test_requires_bsns_year(self):
        """사업연도 필수"""
        api = FinancialAPI(api_key="test_key")

        with pytest.raises(ValueError, match="bsns_year"):
            api.validate_single_account_params(
                corp_code="00126380",
                bsns_year="",
                reprt_code="11013",
            )

    def test_requires_reprt_code(self):
        """보고서 코드 필수"""
        api = FinancialAPI(api_key="test_key")

        with pytest.raises(ValueError, match="reprt_code"):
            api.validate_single_account_params(
                corp_code="00126380",
                bsns_year="2024",
                reprt_code="",
            )

    def test_accepts_valid_params(self):
        """유효한 파라미터 허용"""
        api = FinancialAPI(api_key="test_key")

        # Should not raise
        api.validate_single_account_params(
            corp_code="00126380",
            bsns_year="2024",
            reprt_code="11013",
        )

    def test_requires_corp_codes_for_multi_account(self):
        """다중회사 조회 시 corp_code 목록 필수"""
        api = FinancialAPI(api_key="test_key")

        with pytest.raises(ValueError, match="corp_code"):
            api.validate_multi_account_params(
                corp_code=[],
                bsns_year="2024",
                reprt_code="11013",
            )
