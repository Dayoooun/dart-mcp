"""DS001 공시정보 API 테스트"""
import pytest
from pydantic import ValidationError
from src.opendart_mcp.models.ds001 import (
    DisclosureListResponse,
    DisclosureItem,
    CompanyResponse,
)
from src.opendart_mcp.api.disclosure import DisclosureAPI


class TestDisclosureListResponse:
    """공시검색 응답 모델 테스트"""

    def test_parses_valid_response(self):
        """유효한 응답 파싱"""
        data = {
            "status": "000",
            "message": "정상",
            "page_no": 1,
            "page_count": 10,
            "total_count": 100,
            "total_page": 10,
            "list": [
                {
                    "corp_code": "00126380",
                    "corp_name": "삼성전자",
                    "stock_code": "005930",
                    "corp_cls": "Y",
                    "report_nm": "분기보고서",
                    "rcept_no": "20240515000001",
                    "flr_nm": "삼성전자",
                    "rcept_dt": "20240515",
                    "rm": "",
                }
            ],
        }

        response = DisclosureListResponse(**data)

        assert response.status == "000"
        assert response.total_count == 100
        assert len(response.list) == 1
        assert response.list[0].corp_name == "삼성전자"

    def test_handles_empty_list(self):
        """빈 목록 처리"""
        data = {
            "status": "013",
            "message": "조회된 데이터가 없습니다",
            "page_no": 1,
            "page_count": 10,
            "total_count": 0,
            "total_page": 0,
            "list": [],
        }

        response = DisclosureListResponse(**data)
        assert response.list == []


class TestCompanyResponse:
    """기업개황 응답 모델 테스트"""

    def test_parses_valid_response(self):
        """유효한 응답 파싱"""
        data = {
            "status": "000",
            "message": "정상",
            "corp_code": "00126380",
            "corp_name": "삼성전자",
            "corp_name_eng": "SAMSUNG ELECTRONICS",
            "stock_name": "삼성전자",
            "stock_code": "005930",
            "ceo_nm": "한종희, 경계현",
            "corp_cls": "Y",
            "jurir_no": "1301110006246",
            "bizr_no": "1248100998",
            "adres": "경기도 수원시 영통구 삼성로 129",
            "hm_url": "www.samsung.com",
            "ir_url": "",
            "phn_no": "031-200-1114",
            "fax_no": "031-200-7538",
            "induty_code": "264",
            "est_dt": "19690113",
            "acc_mt": "12",
        }

        response = CompanyResponse(**data)

        assert response.corp_name == "삼성전자"
        assert response.ceo_nm == "한종희, 경계현"
        assert response.corp_cls == "Y"


class TestDisclosureAPI:
    """공시정보 API 테스트"""

    def test_search_requires_at_least_one_param(self):
        """최소 하나의 검색 조건 필요"""
        api = DisclosureAPI(api_key="test_key")

        with pytest.raises(ValueError, match="검색 조건"):
            api.validate_search_params()

    def test_search_accepts_corp_code(self):
        """corp_code 파라미터 허용"""
        api = DisclosureAPI(api_key="test_key")

        # Should not raise
        api.validate_search_params(corp_code="00126380")

    def test_search_accepts_date_range(self):
        """날짜 범위 파라미터 허용"""
        api = DisclosureAPI(api_key="test_key")

        # Should not raise
        api.validate_search_params(bgn_de="20240101", end_de="20240131")
