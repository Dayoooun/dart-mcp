"""DS001 공시정보 모델"""
from typing import List, Optional
from pydantic import BaseModel, Field


class DisclosureItem(BaseModel):
    """공시 항목"""

    corp_code: str = Field(..., description="고유번호")
    corp_name: str = Field(..., description="회사명")
    stock_code: Optional[str] = Field(None, description="종목코드")
    corp_cls: str = Field(..., description="법인구분 (Y/K/N/E)")
    report_nm: str = Field(..., description="보고서명")
    rcept_no: str = Field(..., description="접수번호")
    flr_nm: str = Field(..., description="공시제출인명")
    rcept_dt: str = Field(..., description="접수일자")
    rm: Optional[str] = Field(None, description="비고")


class DisclosureListResponse(BaseModel):
    """공시검색 응답"""

    status: str = Field(..., description="응답 상태코드")
    message: str = Field(..., description="응답 메시지")
    page_no: int = Field(..., description="현재 페이지")
    page_count: int = Field(..., description="페이지당 건수")
    total_count: int = Field(..., description="총 건수")
    total_page: int = Field(..., description="총 페이지 수")
    list: List[DisclosureItem] = Field(default_factory=list, description="공시 목록")


class CompanyResponse(BaseModel):
    """기업개황 응답"""

    status: str = Field(..., description="응답 상태코드")
    message: str = Field(..., description="응답 메시지")
    corp_code: str = Field(..., description="고유번호")
    corp_name: str = Field(..., description="회사명")
    corp_name_eng: Optional[str] = Field(None, description="영문 회사명")
    stock_name: Optional[str] = Field(None, description="종목명")
    stock_code: Optional[str] = Field(None, description="종목코드")
    ceo_nm: str = Field(..., description="대표자명")
    corp_cls: str = Field(..., description="법인구분")
    jurir_no: Optional[str] = Field(None, description="법인등록번호")
    bizr_no: Optional[str] = Field(None, description="사업자등록번호")
    adres: str = Field(..., description="주소")
    hm_url: Optional[str] = Field(None, description="홈페이지 URL")
    ir_url: Optional[str] = Field(None, description="IR 홈페이지")
    phn_no: Optional[str] = Field(None, description="전화번호")
    fax_no: Optional[str] = Field(None, description="팩스번호")
    induty_code: Optional[str] = Field(None, description="업종코드")
    est_dt: Optional[str] = Field(None, description="설립일")
    acc_mt: str = Field(..., description="결산월")


class CorpCode(BaseModel):
    """기업 고유번호"""

    corp_code: str = Field(..., description="고유번호")
    corp_name: str = Field(..., description="회사명")
    stock_code: Optional[str] = Field(None, description="종목코드")
    modify_date: str = Field(..., description="최종변경일")

    @property
    def is_listed(self) -> bool:
        """상장 여부"""
        return bool(self.stock_code and self.stock_code.strip())
