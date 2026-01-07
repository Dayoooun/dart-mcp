"""DS003 재무정보 모델"""
from typing import List, Optional
from pydantic import BaseModel, Field


class FinancialAccountItem(BaseModel):
    """단일회사 주요계정 항목"""

    rcept_no: str = Field(..., description="접수번호")
    bsns_year: str = Field(..., description="사업연도")
    corp_code: str = Field(..., description="고유번호")
    stock_code: Optional[str] = Field(None, description="종목코드")
    reprt_code: str = Field(..., description="보고서 코드")
    account_nm: str = Field(..., description="계정명")
    fs_div: str = Field(..., description="개별/연결구분 (OFS/CFS)")
    fs_nm: str = Field(..., description="개별/연결명")
    sj_div: str = Field(..., description="재무제표구분 (BS/IS/CIS/CF/SCE)")
    sj_nm: str = Field(..., description="재무제표명")
    thstrm_nm: str = Field(..., description="당기명")
    thstrm_dt: Optional[str] = Field(None, description="당기일자")
    thstrm_amount: Optional[str] = Field(None, description="당기금액")
    frmtrm_nm: Optional[str] = Field(None, description="전기명")
    frmtrm_dt: Optional[str] = Field(None, description="전기일자")
    frmtrm_amount: Optional[str] = Field(None, description="전기금액")
    bfefrmtrm_nm: Optional[str] = Field(None, description="전전기명")
    bfefrmtrm_dt: Optional[str] = Field(None, description="전전기일자")
    bfefrmtrm_amount: Optional[str] = Field(None, description="전전기금액")
    ord: Optional[str] = Field(None, description="계정과목 정렬순서")


class SingleCompanyAccountResponse(BaseModel):
    """단일회사 주요계정 응답"""

    status: str = Field(..., description="응답 상태코드")
    message: str = Field(..., description="응답 메시지")
    list: List[FinancialAccountItem] = Field(default_factory=list, description="계정 목록")


class MultiCompanyAccountItem(BaseModel):
    """다중회사 주요계정 항목"""

    rcept_no: str = Field(..., description="접수번호")
    corp_code: str = Field(..., description="고유번호")
    corp_name: Optional[str] = Field(None, description="회사명")
    stock_code: Optional[str] = Field(None, description="종목코드")
    bsns_year: str = Field(..., description="사업연도")
    reprt_code: str = Field(..., description="보고서 코드")
    account_nm: str = Field(..., description="계정명")
    fs_div: str = Field(..., description="개별/연결구분")
    fs_nm: str = Field(..., description="개별/연결명")
    sj_div: str = Field(..., description="재무제표구분")
    sj_nm: str = Field(..., description="재무제표명")
    thstrm_nm: str = Field(..., description="당기명")
    thstrm_dt: Optional[str] = Field(None, description="당기일자")
    thstrm_amount: Optional[str] = Field(None, description="당기금액")
    frmtrm_nm: Optional[str] = Field(None, description="전기명")
    frmtrm_dt: Optional[str] = Field(None, description="전기일자")
    frmtrm_amount: Optional[str] = Field(None, description="전기금액")
    bfefrmtrm_nm: Optional[str] = Field(None, description="전전기명")
    bfefrmtrm_dt: Optional[str] = Field(None, description="전전기일자")
    bfefrmtrm_amount: Optional[str] = Field(None, description="전전기금액")
    ord: Optional[str] = Field(None, description="계정과목 정렬순서")
    currency: Optional[str] = Field(None, description="통화 단위")


class MultiCompanyAccountResponse(BaseModel):
    """다중회사 주요계정 응답"""

    status: str = Field(..., description="응답 상태코드")
    message: str = Field(..., description="응답 메시지")
    list: List[MultiCompanyAccountItem] = Field(default_factory=list, description="계정 목록")


class FinancialStatementItem(BaseModel):
    """재무제표 항목"""

    rcept_no: str = Field(..., description="접수번호")
    reprt_code: str = Field(..., description="보고서 코드")
    bsns_year: str = Field(..., description="사업연도")
    corp_code: str = Field(..., description="고유번호")
    sj_div: str = Field(..., description="재무제표구분")
    sj_nm: str = Field(..., description="재무제표명")
    account_id: Optional[str] = Field(None, description="계정ID")
    account_nm: str = Field(..., description="계정명")
    account_detail: Optional[str] = Field(None, description="계정상세")
    thstrm_nm: str = Field(..., description="당기명")
    thstrm_amount: Optional[str] = Field(None, description="당기금액")
    frmtrm_nm: Optional[str] = Field(None, description="전기명")
    frmtrm_amount: Optional[str] = Field(None, description="전기금액")
    bfefrmtrm_nm: Optional[str] = Field(None, description="전전기명")
    bfefrmtrm_amount: Optional[str] = Field(None, description="전전기금액")
    ord: Optional[str] = Field(None, description="계정과목 정렬순서")


class FullFinancialStatementResponse(BaseModel):
    """단일회사 전체 재무제표 응답"""

    status: str = Field(..., description="응답 상태코드")
    message: str = Field(..., description="응답 메시지")
    list: List[FinancialStatementItem] = Field(default_factory=list, description="재무제표 목록")
