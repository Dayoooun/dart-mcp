"""DS001 공시정보 API"""
from typing import Optional
import httpx
from ..models.ds001 import DisclosureListResponse, CompanyResponse
from ..exceptions import OpenDartException


class DisclosureAPI:
    """DS001 공시정보 API 클라이언트"""

    BASE_URL = "https://opendart.fss.or.kr/api"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL

    def validate_search_params(
        self,
        corp_code: Optional[str] = None,
        bgn_de: Optional[str] = None,
        end_de: Optional[str] = None,
    ):
        """검색 파라미터 유효성 검사

        Raises:
            ValueError: 검색 조건이 하나도 없는 경우
        """
        if not any([corp_code, bgn_de, end_de]):
            raise ValueError("최소 하나의 검색 조건이 필요합니다 (corp_code, bgn_de, end_de 중 하나)")

    async def search(
        self,
        corp_code: Optional[str] = None,
        bgn_de: Optional[str] = None,
        end_de: Optional[str] = None,
        last_reprt_at: Optional[str] = None,
        pblntf_ty: Optional[str] = None,
        pblntf_detail_ty: Optional[str] = None,
        corp_cls: Optional[str] = None,
        sort: Optional[str] = None,
        sort_mth: Optional[str] = None,
        page_no: int = 1,
        page_count: int = 10,
    ) -> DisclosureListResponse:
        """공시검색 API

        Args:
            corp_code: 고유번호
            bgn_de: 시작일 (YYYYMMDD)
            end_de: 종료일 (YYYYMMDD)
            last_reprt_at: 최종보고서만 (Y/N)
            pblntf_ty: 공시유형
            pblntf_detail_ty: 공시상세유형
            corp_cls: 법인구분
            sort: 정렬 (date/crp/rpt)
            sort_mth: 정렬방식 (asc/desc)
            page_no: 페이지 번호
            page_count: 페이지당 건수

        Returns:
            DisclosureListResponse
        """
        self.validate_search_params(corp_code, bgn_de, end_de)

        params = {
            "crtfc_key": self.api_key,
            "page_no": page_no,
            "page_count": page_count,
        }

        if corp_code:
            params["corp_code"] = corp_code
        if bgn_de:
            params["bgn_de"] = bgn_de
        if end_de:
            params["end_de"] = end_de
        if last_reprt_at:
            params["last_reprt_at"] = last_reprt_at
        if pblntf_ty:
            params["pblntf_ty"] = pblntf_ty
        if pblntf_detail_ty:
            params["pblntf_detail_ty"] = pblntf_detail_ty
        if corp_cls:
            params["corp_cls"] = corp_cls
        if sort:
            params["sort"] = sort
        if sort_mth:
            params["sort_mth"] = sort_mth

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/list.json", params=params)
            data = response.json()

            if data.get("status") != "000":
                raise OpenDartException.from_error_code(
                    data.get("status", "999"),
                    data.get("message", "Unknown error"),
                )

            return DisclosureListResponse(**data)

    async def get_company(self, corp_code: str) -> CompanyResponse:
        """기업개황 API

        Args:
            corp_code: 고유번호

        Returns:
            CompanyResponse
        """
        if not corp_code:
            raise ValueError("corp_code는 필수입니다")

        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/company.json", params=params)
            data = response.json()

            if data.get("status") != "000":
                raise OpenDartException.from_error_code(
                    data.get("status", "999"),
                    data.get("message", "Unknown error"),
                )

            return CompanyResponse(**data)
