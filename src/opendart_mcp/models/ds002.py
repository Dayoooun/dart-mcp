"""DS002 정기보고서 주요정보 모델"""
from typing import List, Optional
from pydantic import BaseModel, Field


class DividendItem(BaseModel):
    """배당에 관한 사항 항목"""

    rcept_no: str = Field(..., description="접수번호")
    corp_cls: str = Field(..., description="법인구분")
    corp_code: str = Field(..., description="고유번호")
    corp_name: str = Field(..., description="회사명")
    se: str = Field(..., description="구분")
    thstrm: Optional[str] = Field(None, description="당기")
    frmtrm: Optional[str] = Field(None, description="전기")
    lwfr: Optional[str] = Field(None, description="전전기")


class DividendResponse(BaseModel):
    """배당에 관한 사항 응답"""

    status: str = Field(..., description="응답 상태코드")
    message: str = Field(..., description="응답 메시지")
    list: List[DividendItem] = Field(default_factory=list, description="배당 목록")


class CapitalChangeItem(BaseModel):
    """증자(감자) 현황 항목"""

    rcept_no: str = Field(..., description="접수번호")
    corp_cls: str = Field(..., description="법인구분")
    corp_code: str = Field(..., description="고유번호")
    corp_name: str = Field(..., description="회사명")
    isu_dcrs_de: Optional[str] = Field(None, description="주식발행(감소)일자")
    isu_dcrs_stle: Optional[str] = Field(None, description="발행(감소)형태")
    isu_dcrs_stock_knd: Optional[str] = Field(None, description="발행(감소)주식의 종류")
    isu_dcrs_qy: Optional[str] = Field(None, description="발행(감소)수량")
    isu_dcrs_mstvdv_fval_amount: Optional[str] = Field(None, description="발행(감소)주당 액면가액")
    isu_dcrs_mstvdv_amount: Optional[str] = Field(None, description="발행(감소)주당 가액")


class CapitalChangeResponse(BaseModel):
    """증자(감자) 현황 응답"""

    status: str = Field(..., description="응답 상태코드")
    message: str = Field(..., description="응답 메시지")
    list: List[CapitalChangeItem] = Field(default_factory=list, description="증자(감자) 목록")


class TreasuryStockItem(BaseModel):
    """자기주식 취득 및 처분 현황 항목"""

    rcept_no: str = Field(..., description="접수번호")
    corp_cls: str = Field(..., description="법인구분")
    corp_code: str = Field(..., description="고유번호")
    corp_name: str = Field(..., description="회사명")
    acqs_mth1: Optional[str] = Field(None, description="취득방법 대분류")
    acqs_mth2: Optional[str] = Field(None, description="취득방법 중분류")
    acqs_mth3: Optional[str] = Field(None, description="취득방법 소분류")
    stock_knd: Optional[str] = Field(None, description="주식 종류")
    bsis_qy: Optional[str] = Field(None, description="기초 수량")
    change_qy_acqs: Optional[str] = Field(None, description="변동수량 취득")
    change_qy_dsps: Optional[str] = Field(None, description="변동수량 처분")
    change_qy_incnr: Optional[str] = Field(None, description="변동수량 소각")
    trmend_qy: Optional[str] = Field(None, description="기말 수량")
    rm: Optional[str] = Field(None, description="비고")


class TreasuryStockResponse(BaseModel):
    """자기주식 취득 및 처분 현황 응답"""

    status: str = Field(..., description="응답 상태코드")
    message: str = Field(..., description="응답 메시지")
    list: List[TreasuryStockItem] = Field(default_factory=list, description="자기주식 목록")


class ExecutiveItem(BaseModel):
    """임원 현황 항목"""

    rcept_no: str = Field(..., description="접수번호")
    corp_cls: str = Field(..., description="법인구분")
    corp_code: str = Field(..., description="고유번호")
    corp_name: str = Field(..., description="회사명")
    nm: str = Field(..., description="성명")
    sexdstn: Optional[str] = Field(None, description="성별")
    birth_ym: Optional[str] = Field(None, description="출생년월")
    ofcps: Optional[str] = Field(None, description="직위")
    rgist_exctv_at: Optional[str] = Field(None, description="등기임원 여부")
    fte_at: Optional[str] = Field(None, description="상근 여부")
    chrg_job: Optional[str] = Field(None, description="담당업무")
    main_career: Optional[str] = Field(None, description="주요경력")
    mxmm_shrholdr_relate: Optional[str] = Field(None, description="최대주주와의 관계")
    hffc_pd: Optional[str] = Field(None, description="재직기간")
    tenure_end_on: Optional[str] = Field(None, description="임기만료일")


class ExecutiveResponse(BaseModel):
    """임원 현황 응답"""

    status: str = Field(..., description="응답 상태코드")
    message: str = Field(..., description="응답 메시지")
    list: List[ExecutiveItem] = Field(default_factory=list, description="임원 목록")


class EmployeeItem(BaseModel):
    """직원 현황 항목"""

    rcept_no: str = Field(..., description="접수번호")
    corp_cls: str = Field(..., description="법인구분")
    corp_code: str = Field(..., description="고유번호")
    corp_name: str = Field(..., description="회사명")
    fo_bbm: Optional[str] = Field(None, description="사업부문")
    sexdstn: Optional[str] = Field(None, description="성별")
    reform_bfe_emp_co_rgllbr: Optional[str] = Field(None, description="개정 전 정규직 수")
    reform_bfe_emp_co_cnttk: Optional[str] = Field(None, description="개정 전 계약직 수")
    reform_bfe_emp_co_etc: Optional[str] = Field(None, description="개정 전 기타 수")
    rgllbr_co: Optional[str] = Field(None, description="정규직 수")
    rgllbr_abacpt_labrr_co: Optional[str] = Field(None, description="정규직 단시간근로자 수")
    cnttk_co: Optional[str] = Field(None, description="계약직 수")
    cnttk_abacpt_labrr_co: Optional[str] = Field(None, description="계약직 단시간근로자 수")
    sm: Optional[str] = Field(None, description="합계")
    avrg_cnwk_sdytrn: Optional[str] = Field(None, description="평균근속연수")
    fyer_salary_totamt: Optional[str] = Field(None, description="연간급여 총액")
    jan_salary_am: Optional[str] = Field(None, description="1인평균 급여액")
    rm: Optional[str] = Field(None, description="비고")


class EmployeeResponse(BaseModel):
    """직원 현황 응답"""

    status: str = Field(..., description="응답 상태코드")
    message: str = Field(..., description="응답 메시지")
    list: List[EmployeeItem] = Field(default_factory=list, description="직원 목록")


class LargestShareholderItem(BaseModel):
    """최대주주 현황 항목"""

    rcept_no: str = Field(..., description="접수번호")
    corp_cls: str = Field(..., description="법인구분")
    corp_code: str = Field(..., description="고유번호")
    corp_name: str = Field(..., description="회사명")
    nm: str = Field(..., description="성명")
    relate: Optional[str] = Field(None, description="관계")
    stock_knd: Optional[str] = Field(None, description="주식 종류")
    bsis_posesn_stock_co: Optional[str] = Field(None, description="기초 소유주식수")
    bsis_posesn_stock_qota_rt: Optional[str] = Field(None, description="기초 소유주식 지분율")
    trmend_posesn_stock_co: Optional[str] = Field(None, description="기말 소유주식수")
    trmend_posesn_stock_qota_rt: Optional[str] = Field(None, description="기말 소유주식 지분율")
    rm: Optional[str] = Field(None, description="비고")


class LargestShareholderResponse(BaseModel):
    """최대주주 현황 응답"""

    status: str = Field(..., description="응답 상태코드")
    message: str = Field(..., description="응답 메시지")
    list: List[LargestShareholderItem] = Field(default_factory=list, description="최대주주 목록")
