"""DS002 정기보고서 주요정보 API"""
from typing import Optional
import httpx
from ..models.ds002 import (
    DividendResponse,
    CapitalChangeResponse,
    TreasuryStockResponse,
    ExecutiveResponse,
    EmployeeResponse,
    LargestShareholderResponse,
)
from ..exceptions import OpenDartException


class ReportAPI:
    """DS002 정기보고서 주요정보 API 클라이언트"""

    BASE_URL = "https://opendart.fss.or.kr/api"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL

    def validate_params(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ):
        """파라미터 유효성 검사

        Raises:
            ValueError: 필수 파라미터가 없는 경우
        """
        if not corp_code:
            raise ValueError("corp_code는 필수입니다")
        if not bsns_year:
            raise ValueError("bsns_year는 필수입니다")
        if not reprt_code:
            raise ValueError("reprt_code는 필수입니다")

    def _build_params(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> dict:
        """공통 파라미터 빌드"""
        return {
            "crtfc_key": self.api_key,
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }

    async def _request(self, endpoint: str, params: dict) -> dict:
        """API 요청 공통 처리"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/{endpoint}", params=params)
            data = response.json()

            if data.get("status") != "000":
                raise OpenDartException.from_error_code(
                    data.get("status", "999"),
                    data.get("message", "Unknown error"),
                )

            return data

    async def get_dividend(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> DividendResponse:
        """배당에 관한 사항 API

        Args:
            corp_code: 고유번호
            bsns_year: 사업연도 (YYYY)
            reprt_code: 보고서 코드

        Returns:
            DividendResponse
        """
        self.validate_params(corp_code, bsns_year, reprt_code)
        params = self._build_params(corp_code, bsns_year, reprt_code)
        data = await self._request("alotMatter.json", params)
        return DividendResponse(**data)

    async def get_capital_change(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> CapitalChangeResponse:
        """증자(감자) 현황 API

        Args:
            corp_code: 고유번호
            bsns_year: 사업연도 (YYYY)
            reprt_code: 보고서 코드

        Returns:
            CapitalChangeResponse
        """
        self.validate_params(corp_code, bsns_year, reprt_code)
        params = self._build_params(corp_code, bsns_year, reprt_code)
        data = await self._request("irdsSttus.json", params)
        return CapitalChangeResponse(**data)

    async def get_treasury_stock(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> TreasuryStockResponse:
        """자기주식 취득 및 처분 현황 API

        Args:
            corp_code: 고유번호
            bsns_year: 사업연도 (YYYY)
            reprt_code: 보고서 코드

        Returns:
            TreasuryStockResponse
        """
        self.validate_params(corp_code, bsns_year, reprt_code)
        params = self._build_params(corp_code, bsns_year, reprt_code)
        data = await self._request("tesstkAcqsDspsSttus.json", params)
        return TreasuryStockResponse(**data)

    async def get_executives(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> ExecutiveResponse:
        """임원 현황 API

        Args:
            corp_code: 고유번호
            bsns_year: 사업연도 (YYYY)
            reprt_code: 보고서 코드

        Returns:
            ExecutiveResponse
        """
        self.validate_params(corp_code, bsns_year, reprt_code)
        params = self._build_params(corp_code, bsns_year, reprt_code)
        data = await self._request("exctvSttus.json", params)
        return ExecutiveResponse(**data)

    async def get_employees(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> EmployeeResponse:
        """직원 현황 API

        Args:
            corp_code: 고유번호
            bsns_year: 사업연도 (YYYY)
            reprt_code: 보고서 코드

        Returns:
            EmployeeResponse
        """
        self.validate_params(corp_code, bsns_year, reprt_code)
        params = self._build_params(corp_code, bsns_year, reprt_code)
        data = await self._request("empSttus.json", params)
        return EmployeeResponse(**data)

    async def get_largest_shareholders(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> LargestShareholderResponse:
        """최대주주 현황 API

        Args:
            corp_code: 고유번호
            bsns_year: 사업연도 (YYYY)
            reprt_code: 보고서 코드

        Returns:
            LargestShareholderResponse
        """
        self.validate_params(corp_code, bsns_year, reprt_code)
        params = self._build_params(corp_code, bsns_year, reprt_code)
        data = await self._request("hyslrSttus.json", params)
        return LargestShareholderResponse(**data)
