"""DS002 정기보고서 주요정보 API 테스트"""
import pytest
from src.opendart_mcp.models.ds002 import (
    DividendItem,
    DividendResponse,
    CapitalChangeItem,
    CapitalChangeResponse,
    TreasuryStockItem,
    TreasuryStockResponse,
    ExecutiveItem,
    ExecutiveResponse,
    EmployeeItem,
    EmployeeResponse,
    LargestShareholderItem,
    LargestShareholderResponse,
)
from src.opendart_mcp.api.report import ReportAPI


class TestDividendResponse:
    """배당에 관한 사항 응답 모델 테스트"""

    def test_parses_valid_response(self):
        """유효한 응답 파싱"""
        data = {
            "status": "000",
            "message": "정상",
            "list": [
                {
                    "rcept_no": "20240515000001",
                    "corp_cls": "Y",
                    "corp_code": "00126380",
                    "corp_name": "삼성전자",
                    "se": "주당 현금배당금(원)",
                    "thstrm": "361",
                    "frmtrm": "361",
                    "lwfr": "354",
                }
            ],
        }

        response = DividendResponse(**data)

        assert response.status == "000"
        assert len(response.list) == 1
        assert response.list[0].corp_name == "삼성전자"
        assert response.list[0].se == "주당 현금배당금(원)"

    def test_handles_empty_list(self):
        """빈 목록 처리"""
        data = {
            "status": "013",
            "message": "조회된 데이터가 없습니다",
            "list": [],
        }

        response = DividendResponse(**data)
        assert response.list == []


class TestCapitalChangeResponse:
    """증자(감자) 현황 응답 모델 테스트"""

    def test_parses_valid_response(self):
        """유효한 응답 파싱"""
        data = {
            "status": "000",
            "message": "정상",
            "list": [
                {
                    "rcept_no": "20240515000001",
                    "corp_cls": "Y",
                    "corp_code": "00126380",
                    "corp_name": "삼성전자",
                    "isu_dcrs_de": "2024.03.15",
                    "isu_dcrs_stle": "유상증자(일반공모)",
                    "isu_dcrs_stock_knd": "보통주",
                    "isu_dcrs_qy": "1,000,000",
                    "isu_dcrs_mstvdv_fval_amount": "5,000",
                    "isu_dcrs_mstvdv_amount": "50,000",
                }
            ],
        }

        response = CapitalChangeResponse(**data)

        assert response.status == "000"
        assert len(response.list) == 1
        assert response.list[0].isu_dcrs_stle == "유상증자(일반공모)"


class TestTreasuryStockResponse:
    """자기주식 취득 및 처분 현황 응답 모델 테스트"""

    def test_parses_valid_response(self):
        """유효한 응답 파싱"""
        data = {
            "status": "000",
            "message": "정상",
            "list": [
                {
                    "rcept_no": "20240515000001",
                    "corp_cls": "Y",
                    "corp_code": "00126380",
                    "corp_name": "삼성전자",
                    "acqs_mth1": "직접취득",
                    "acqs_mth2": "직접취득",
                    "acqs_mth3": "직접취득",
                    "stock_knd": "보통주",
                    "bsis_qy": "1,000,000",
                    "change_qy_acqs": "100,000",
                    "change_qy_dsps": "0",
                    "change_qy_incnr": "0",
                    "trmend_qy": "1,100,000",
                    "rm": "",
                }
            ],
        }

        response = TreasuryStockResponse(**data)

        assert response.status == "000"
        assert len(response.list) == 1
        assert response.list[0].stock_knd == "보통주"


class TestExecutiveResponse:
    """임원 현황 응답 모델 테스트"""

    def test_parses_valid_response(self):
        """유효한 응답 파싱"""
        data = {
            "status": "000",
            "message": "정상",
            "list": [
                {
                    "rcept_no": "20240515000001",
                    "corp_cls": "Y",
                    "corp_code": "00126380",
                    "corp_name": "삼성전자",
                    "nm": "홍길동",
                    "sexdstn": "남",
                    "birth_ym": "1970.01",
                    "ofcps": "대표이사",
                    "rgist_exctv_at": "등기임원",
                    "fte_at": "상근",
                    "chrg_job": "경영총괄",
                    "main_career": "XX대학교 졸업",
                    "mxmm_shrholdr_relate": "-",
                    "hffc_pd": "5년",
                    "tenure_end_on": "2026.03",
                }
            ],
        }

        response = ExecutiveResponse(**data)

        assert response.status == "000"
        assert len(response.list) == 1
        assert response.list[0].nm == "홍길동"
        assert response.list[0].ofcps == "대표이사"


class TestEmployeeResponse:
    """직원 현황 응답 모델 테스트"""

    def test_parses_valid_response(self):
        """유효한 응답 파싱"""
        data = {
            "status": "000",
            "message": "정상",
            "list": [
                {
                    "rcept_no": "20240515000001",
                    "corp_cls": "Y",
                    "corp_code": "00126380",
                    "corp_name": "삼성전자",
                    "fo_bbm": "반도체",
                    "sexdstn": "남",
                    "reform_bfe_emp_co_rgllbr": "50,000",
                    "reform_bfe_emp_co_cnttk": "5,000",
                    "reform_bfe_emp_co_etc": "100",
                    "rgllbr_co": "52,000",
                    "rgllbr_abacpt_labrr_co": "2,000",
                    "cnttk_co": "5,500",
                    "cnttk_abacpt_labrr_co": "500",
                    "sm": "60,000",
                    "avrg_cnwk_sdytrn": "8.5",
                    "fyer_salary_totamt": "5,000,000,000",
                    "jan_salary_am": "420,000,000",
                    "rm": "",
                }
            ],
        }

        response = EmployeeResponse(**data)

        assert response.status == "000"
        assert len(response.list) == 1
        assert response.list[0].fo_bbm == "반도체"


class TestLargestShareholderResponse:
    """최대주주 현황 응답 모델 테스트"""

    def test_parses_valid_response(self):
        """유효한 응답 파싱"""
        data = {
            "status": "000",
            "message": "정상",
            "list": [
                {
                    "rcept_no": "20240515000001",
                    "corp_cls": "Y",
                    "corp_code": "00126380",
                    "corp_name": "삼성전자",
                    "nm": "삼성물산(주)",
                    "relate": "최대주주 본인",
                    "stock_knd": "보통주",
                    "bsis_posesn_stock_co": "1,000,000,000",
                    "bsis_posesn_stock_qota_rt": "17.5",
                    "trmend_posesn_stock_co": "1,000,000,000",
                    "trmend_posesn_stock_qota_rt": "17.5",
                    "rm": "",
                }
            ],
        }

        response = LargestShareholderResponse(**data)

        assert response.status == "000"
        assert len(response.list) == 1
        assert response.list[0].nm == "삼성물산(주)"


class TestReportAPI:
    """정기보고서 주요정보 API 테스트"""

    def test_requires_corp_code(self):
        """corp_code 필수"""
        api = ReportAPI(api_key="test_key")

        with pytest.raises(ValueError, match="corp_code"):
            api.validate_params(
                corp_code="",
                bsns_year="2024",
                reprt_code="11013",
            )

    def test_requires_bsns_year(self):
        """bsns_year 필수"""
        api = ReportAPI(api_key="test_key")

        with pytest.raises(ValueError, match="bsns_year"):
            api.validate_params(
                corp_code="00126380",
                bsns_year="",
                reprt_code="11013",
            )

    def test_requires_reprt_code(self):
        """reprt_code 필수"""
        api = ReportAPI(api_key="test_key")

        with pytest.raises(ValueError, match="reprt_code"):
            api.validate_params(
                corp_code="00126380",
                bsns_year="2024",
                reprt_code="",
            )

    def test_accepts_valid_params(self):
        """유효한 파라미터 허용"""
        api = ReportAPI(api_key="test_key")

        # Should not raise
        api.validate_params(
            corp_code="00126380",
            bsns_year="2024",
            reprt_code="11013",
        )
