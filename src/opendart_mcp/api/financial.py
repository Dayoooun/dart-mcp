"""DS003 재무정보 API"""
from typing import List, Optional
import httpx
from ..models.ds003 import (
    SingleCompanyAccountResponse,
    MultiCompanyAccountResponse,
    FullFinancialStatementResponse,
)
from ..exceptions import OpenDartException


class FinancialAPI:
    """DS003 재무정보 API 클라이언트"""

    BASE_URL = "https://opendart.fss.or.kr/api"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL

    def validate_single_account_params(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ):
        """단일회사 조회 파라미터 유효성 검사

        Raises:
            ValueError: 필수 파라미터가 없는 경우
        """
        if not corp_code:
            raise ValueError("corp_code는 필수입니다")
        if not bsns_year:
            raise ValueError("bsns_year는 필수입니다")
        if not reprt_code:
            raise ValueError("reprt_code는 필수입니다")

    def validate_multi_account_params(
        self,
        corp_code: List[str],
        bsns_year: str,
        reprt_code: str,
    ):
        """다중회사 조회 파라미터 유효성 검사

        Raises:
            ValueError: 필수 파라미터가 없는 경우
        """
        if not corp_code:
            raise ValueError("corp_code 목록은 필수입니다")
        if not bsns_year:
            raise ValueError("bsns_year는 필수입니다")
        if not reprt_code:
            raise ValueError("reprt_code는 필수입니다")

    async def get_single_account(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
        fs_div: Optional[str] = None,
    ) -> SingleCompanyAccountResponse:
        """단일회사 주요계정 API

        Args:
            corp_code: 고유번호
            bsns_year: 사업연도 (YYYY)
            reprt_code: 보고서 코드 (11013:1분기, 11012:반기, 11014:3분기, 11011:사업)
            fs_div: 개별/연결구분 (OFS:재무제표, CFS:연결재무제표)

        Returns:
            SingleCompanyAccountResponse
        """
        self.validate_single_account_params(corp_code, bsns_year, reprt_code)

        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }

        if fs_div:
            params["fs_div"] = fs_div

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/fnlttSinglAcnt.json", params=params)
            data = response.json()

            if data.get("status") != "000":
                raise OpenDartException.from_error_code(
                    data.get("status", "999"),
                    data.get("message", "Unknown error"),
                )

            return SingleCompanyAccountResponse(**data)

    async def get_multi_account(
        self,
        corp_code: List[str],
        bsns_year: str,
        reprt_code: str,
        fs_div: Optional[str] = None,
    ) -> MultiCompanyAccountResponse:
        """다중회사 주요계정 API

        Args:
            corp_code: 고유번호 목록 (최대 100개)
            bsns_year: 사업연도 (YYYY)
            reprt_code: 보고서 코드
            fs_div: 개별/연결구분

        Returns:
            MultiCompanyAccountResponse
        """
        self.validate_multi_account_params(corp_code, bsns_year, reprt_code)

        params = {
            "crtfc_key": self.api_key,
            "corp_code": ",".join(corp_code),
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }

        if fs_div:
            params["fs_div"] = fs_div

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/fnlttMultiAcnt.json", params=params)
            data = response.json()

            if data.get("status") != "000":
                raise OpenDartException.from_error_code(
                    data.get("status", "999"),
                    data.get("message", "Unknown error"),
                )

            return MultiCompanyAccountResponse(**data)

    async def get_full_statement(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
        fs_div: Optional[str] = None,
    ) -> FullFinancialStatementResponse:
        """단일회사 전체 재무제표 API

        Args:
            corp_code: 고유번호
            bsns_year: 사업연도 (YYYY)
            reprt_code: 보고서 코드
            fs_div: 개별/연결구분

        Returns:
            FullFinancialStatementResponse
        """
        self.validate_single_account_params(corp_code, bsns_year, reprt_code)

        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }

        if fs_div:
            params["fs_div"] = fs_div

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/fnlttSinglAcntAll.json", params=params)
            data = response.json()

            if data.get("status") != "000":
                raise OpenDartException.from_error_code(
                    data.get("status", "999"),
                    data.get("message", "Unknown error"),
                )

            return FullFinancialStatementResponse(**data)
