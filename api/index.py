"""OpenDART MCP Server - Vercel Serverless Function
한국 금융감독원 전자공시시스템(DART) API를 MCP로 제공합니다.
"""
from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse


# API 키 설정 (공용)
API_KEY = "d64dadc7b8236e0ae2e6c3560ef400cc12f2c705"
BASE_URL = "https://opendart.fss.or.kr/api"

# AI 컨텍스트용 상세 안내
USAGE_GUIDE = """
## 📌 사용 가이드

### corp_code(기업 고유번호)를 모를 때
1. `find_company` 도구로 기업명 검색 → corp_code 획득
2. 획득한 corp_code로 다른 API 호출

### 주요 기업 고유번호 (자주 사용)
- 삼성전자: 00126380
- SK하이닉스: 00164779  
- LG전자: 00401731
- 현대자동차: 00164742
- 네이버: 00266961
- 카카오: 00258801
- 삼성SDI: 00126371
- LG화학: 00356361
- 셀트리온: 00421045
- 포스코홀딩스: 00126186

### reprt_code (보고서 종류)
- 11011: 사업보고서 (연간, 가장 상세)
- 11012: 반기보고서
- 11013: 1분기보고서
- 11014: 3분기보고서

### fs_div (재무제표 구분)
- CFS: 연결재무제표 (자회사 포함, 일반적으로 사용)
- OFS: 개별재무제표 (해당 법인만)

### corp_cls (시장 구분)
- Y: 유가증권시장 (코스피 대기업)
- K: 코스닥시장 (중소/벤처)
- N: 코넥스시장 (초기기업)
- E: 기타 (비상장 등)
"""

FIND_COMPANY_DESC = """기업명으로 corp_code(기업 고유번호) 검색

⚠️ 중요: corp_code를 모르는 기업 조회 시 이 도구를 먼저 사용하세요!

### 사용 예시
- "인산가" → corp_code 획득 → 재무제표 조회
- "오르비텍" → corp_code 획득 → 임원 현황 조회

### 검색 팁
- 정확한 기업명 또는 일부만 입력 가능
- 전체 114,000+ 기업 데이터에서 즉시 검색 (매우 빠름!)
- 상장기업이 우선 정렬되어 반환됩니다
- 검색 결과에서 corp_code, corp_name, stock_code(종목코드) 확인

### 주요 기업은 직접 사용 가능
- 삼성전자: 00126380
- SK하이닉스: 00164779
- LG전자: 00401731
- 현대자동차: 00164742
- 네이버: 00266961
- 카카오: 00258801
"""

SEARCH_DISCLOSURES_DESC = """한국 상장기업 공시 검색

### 용도
- 최근 공시 내역 확인
- 특정 기업의 공시 이력 조회
- 특정 기간의 공시 검색

### 파라미터
- corp_code: 기업 고유번호 (선택, 없으면 전체 검색)
- bgn_de/end_de: 검색 기간 YYYYMMDD (선택)
- corp_cls: Y(코스피), K(코스닥), N(코넥스), E(기타)

### 💡 corp_code를 모르면?
→ find_company 도구를 먼저 사용하세요!
""" + USAGE_GUIDE

GET_COMPANY_INFO_DESC = """기업 기본정보 조회 (회사명, 대표자, 업종, 주소 등)

### 반환 정보
- corp_name: 회사명
- ceo_nm: 대표자명
- induty_code: 업종코드
- adres: 주소
- hm_url: 홈페이지
- est_dt: 설립일
- acc_mt: 결산월

### 💡 corp_code를 모르면?
→ find_company 도구를 먼저 사용하세요!
""" + USAGE_GUIDE

GET_FINANCIAL_ACCOUNT_DESC = """기업 주요 재무계정 조회 (매출, 영업이익, 자산 등 핵심 지표)

### 반환 정보
- 매출액, 영업이익, 당기순이익
- 자산총계, 부채총계, 자본총계
- 당기/전기/전전기 비교 데이터

### 파라미터
- corp_code: 기업 고유번호 (필수)
- bsns_year: 사업연도 예: "2023" (필수)
- reprt_code: 11011(사업보고서), 11012(반기), 11013(1분기), 11014(3분기)
- fs_div: CFS(연결), OFS(개별) - 선택, 기본값 연결+개별 모두

### 💡 corp_code를 모르면?
→ find_company 도구를 먼저 사용하세요!
""" + USAGE_GUIDE

GET_FULL_FINANCIAL_DESC = """기업 전체 재무제표 상세 조회 (BS, IS, CF 전체 계정)

### 반환 정보 (매우 상세)
- 재무상태표(BS): 자산/부채/자본 전체 항목
- 손익계산서(IS): 수익/비용 전체 항목
- 현금흐름표(CF): 영업/투자/재무활동
- 포괄손익계산서(CIS)
- 자본변동표(SCE)

### 파라미터
- corp_code: 기업 고유번호 (필수)
- bsns_year: 사업연도 예: "2023" (필수)
- reprt_code: 11011(사업보고서), 11012(반기), 11013(1분기), 11014(3분기) (필수)
- fs_div: CFS(연결) 또는 OFS(개별) (필수!)

### 💡 corp_code를 모르면?
→ find_company 도구를 먼저 사용하세요!
""" + USAGE_GUIDE

GET_DIVIDEND_DESC = """기업 배당 정보 조회

### 반환 정보
- 주당 현금배당금
- 배당수익률
- 배당성향
- 현금배당 총액

### 💡 corp_code를 모르면?
→ find_company 도구를 먼저 사용하세요!
""" + USAGE_GUIDE

GET_EXECUTIVES_DESC = """기업 임원 현황 조회

### 반환 정보
- 임원명, 직위
- 등기여부, 상근여부
- 담당업무
- 주요경력

### 💡 corp_code를 모르면?
→ find_company 도구를 먼저 사용하세요!
""" + USAGE_GUIDE

GET_EMPLOYEES_DESC = """기업 직원 현황 조회 (인원, 평균급여, 근속연수)

### 반환 정보
- 직원 수 (정규직/계약직)
- 평균 근속연수
- 연간 급여 총액
- 1인 평균 급여

### ⚠️ 주의
- 사업보고서(11011)에만 상세 정보 포함
- 분기보고서는 데이터 없을 수 있음

### 💡 corp_code를 모르면?
→ find_company 도구를 먼저 사용하세요!
""" + USAGE_GUIDE

GET_SHAREHOLDERS_DESC = """기업 최대주주 현황 조회

### 반환 정보
- 최대주주명
- 보유 주식수
- 지분율 (%)
- 변동 내역

### 💡 corp_code를 모르면?
→ find_company 도구를 먼저 사용하세요!
""" + USAGE_GUIDE


def call_dart_api(endpoint: str, params: dict) -> dict:
    """OpenDART API 호출"""
    params["crtfc_key"] = API_KEY
    query = urllib.parse.urlencode(params)
    url = f"{BASE_URL}/{endpoint}?{query}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_tools():
    """사용 가능한 도구 목록"""
    return [
        # 🔍 기업 검색 (가장 먼저!)
        {
            "name": "find_company",
            "description": FIND_COMPANY_DESC,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색할 기업명 (예: '인산가', '오르비텍', '셀트리온')"
                    },
                },
                "required": ["query"],
            },
        },
        # 📋 공시 검색
        {
            "name": "search_disclosures",
            "description": SEARCH_DISCLOSURES_DESC,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "corp_code": {"type": "string", "description": "기업 고유번호 8자리 (find_company로 검색)"},
                    "bgn_de": {"type": "string", "description": "검색 시작일 YYYYMMDD"},
                    "end_de": {"type": "string", "description": "검색 종료일 YYYYMMDD"},
                    "corp_cls": {"type": "string", "enum": ["Y", "K", "N", "E"], "description": "Y=코스피, K=코스닥, N=코넥스, E=기타"},
                    "page_no": {"type": "integer", "default": 1},
                    "page_count": {"type": "integer", "default": 10},
                },
            },
        },
        # 🏢 기업 정보
        {
            "name": "get_company_info",
            "description": GET_COMPANY_INFO_DESC,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "corp_code": {"type": "string", "description": "기업 고유번호 (find_company로 검색)"},
                },
                "required": ["corp_code"],
            },
        },
        # 💰 주요 재무계정
        {
            "name": "get_financial_account",
            "description": GET_FINANCIAL_ACCOUNT_DESC,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "corp_code": {"type": "string", "description": "기업 고유번호 (find_company로 검색)"},
                    "bsns_year": {"type": "string", "description": "사업연도 (예: 2023)"},
                    "reprt_code": {
                        "type": "string",
                        "enum": ["11011", "11012", "11013", "11014"],
                        "description": "11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기"
                    },
                    "fs_div": {
                        "type": "string",
                        "enum": ["OFS", "CFS"],
                        "description": "CFS=연결(권장), OFS=개별"
                    },
                },
                "required": ["corp_code", "bsns_year", "reprt_code"],
            },
        },
        # 📊 전체 재무제표
        {
            "name": "get_full_financial_statement",
            "description": GET_FULL_FINANCIAL_DESC,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "corp_code": {"type": "string", "description": "기업 고유번호 (find_company로 검색)"},
                    "bsns_year": {"type": "string", "description": "사업연도 (예: 2023)"},
                    "reprt_code": {
                        "type": "string",
                        "enum": ["11011", "11012", "11013", "11014"],
                        "description": "11011=사업보고서, 11012=반기, 11013=1분기, 11014=3분기"
                    },
                    "fs_div": {
                        "type": "string",
                        "enum": ["OFS", "CFS"],
                        "description": "CFS=연결(권장), OFS=개별 (필수!)"
                    },
                },
                "required": ["corp_code", "bsns_year", "reprt_code", "fs_div"],
            },
        },
        # 💵 배당 정보
        {
            "name": "get_dividend_info",
            "description": GET_DIVIDEND_DESC,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "corp_code": {"type": "string", "description": "기업 고유번호 (find_company로 검색)"},
                    "bsns_year": {"type": "string", "description": "사업연도 (예: 2023)"},
                    "reprt_code": {
                        "type": "string",
                        "enum": ["11011", "11012", "11013", "11014"],
                        "description": "11011=사업보고서(권장)"
                    },
                },
                "required": ["corp_code", "bsns_year", "reprt_code"],
            },
        },
        # 👔 임원 현황
        {
            "name": "get_executives",
            "description": GET_EXECUTIVES_DESC,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "corp_code": {"type": "string", "description": "기업 고유번호 (find_company로 검색)"},
                    "bsns_year": {"type": "string", "description": "사업연도 (예: 2023)"},
                    "reprt_code": {
                        "type": "string",
                        "enum": ["11011", "11012", "11013", "11014"],
                        "description": "11011=사업보고서(권장)"
                    },
                },
                "required": ["corp_code", "bsns_year", "reprt_code"],
            },
        },
        # 👥 직원 현황
        {
            "name": "get_employees",
            "description": GET_EMPLOYEES_DESC,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "corp_code": {"type": "string", "description": "기업 고유번호 (find_company로 검색)"},
                    "bsns_year": {"type": "string", "description": "사업연도 (예: 2023)"},
                    "reprt_code": {
                        "type": "string",
                        "enum": ["11011", "11012", "11013", "11014"],
                        "description": "11011=사업보고서(상세정보)"
                    },
                },
                "required": ["corp_code", "bsns_year", "reprt_code"],
            },
        },
        # 📈 최대주주
        {
            "name": "get_largest_shareholders",
            "description": GET_SHAREHOLDERS_DESC,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "corp_code": {"type": "string", "description": "기업 고유번호 (find_company로 검색)"},
                    "bsns_year": {"type": "string", "description": "사업연도 (예: 2023)"},
                    "reprt_code": {
                        "type": "string",
                        "enum": ["11011", "11012", "11013", "11014"],
                        "description": "11011=사업보고서(권장)"
                    },
                },
                "required": ["corp_code", "bsns_year", "reprt_code"],
            },
        },
    ]


# 기업 목록 캐시 (메모리에 로드)
_companies_cache = None

def load_companies():
    """companies.json 로드 (캐싱)"""
    global _companies_cache
    if _companies_cache is not None:
        return _companies_cache
    
    try:
        import os
        json_path = os.path.join(os.path.dirname(__file__), "companies.json")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            _companies_cache = data.get("companies", [])
            return _companies_cache
    except Exception as e:
        print(f"Error loading companies.json: {e}")
        return []


# 한글-영문 기업명 매핑 (주요 기업)
COMPANY_NAME_ALIASES = {
    # 한글 → 영문
    "네이버": ["NAVER", "네이버"],
    "엘지": ["LG", "엘지"],
    "에스케이": ["SK", "에스케이"],
    "케이티": ["KT", "케이티"],
    "포스코": ["POSCO", "포스코"],
    "현대": ["HYUNDAI", "현대"],
    "기아": ["KIA", "기아"],
    "쿠팡": ["COUPANG", "쿠팡"],
    # 영문 → 한글
    "naver": ["NAVER", "네이버"],
    "lg": ["LG", "엘지"],
    "sk": ["SK", "에스케이"],
    "kt": ["KT", "케이티"],
    "posco": ["POSCO", "포스코"],
    "samsung": ["삼성", "SAMSUNG"],
    "hyundai": ["현대", "HYUNDAI"],
    "kia": ["기아", "KIA"],
}


def find_company_by_name(query: str) -> dict:
    """기업명으로 검색하여 corp_code 찾기
    
    114,000+ 전체 기업 데이터에서 검색합니다.
    한글/영문 모두 검색하여 상장기업을 우선으로 정렬합니다.
    """
    companies = load_companies()
    
    if not companies:
        return {
            "status": "error",
            "message": "기업 데이터를 로드할 수 없습니다."
        }
    
    query_lower = query.lower()
    
    # 검색어 확장 (한글-영문 매핑)
    search_terms = [query_lower]
    if query_lower in COMPANY_NAME_ALIASES:
        search_terms.extend([t.lower() for t in COMPANY_NAME_ALIASES[query_lower]])
    
    found = {}  # 중복 제거용 dict
    
    # 검색 (부분 일치, 여러 검색어)
    for c in companies:
        corp_name = c.get("n", "")
        corp_name_lower = corp_name.lower()
        
        for term in search_terms:
            if term in corp_name_lower:
                corp_code = c.get("c", "")
                if corp_code not in found:
                    found[corp_code] = {
                        "corp_code": corp_code,
                        "corp_name": corp_name,
                        "stock_code": c.get("s", ""),  # 상장기업만 있음
                    }
                break
    
    if not found:
        return {
            "status": "not_found",
            "message": f"'{query}' 기업을 찾을 수 없습니다.",
            "tip": "정확한 기업명을 입력해주세요. 예: '삼성전자', '현대자동차', 'NAVER'"
        }
    
    # 리스트로 변환 후 상장기업 우선 정렬
    found_list = list(found.values())
    found_list.sort(key=lambda x: (0 if x.get("stock_code") else 1, x.get("corp_name", "")))
    
    # 최대 20개만 반환
    found_list = found_list[:20]
    
    return {
        "status": "000",
        "message": f"'{query}' 검색 결과: {len(found_list)}개 기업 발견",
        "companies": found_list,
        "usage_tip": "위 corp_code를 사용하여 get_company_info, get_financial_account 등을 호출하세요."
    }


def call_tool(name: str, arguments: dict) -> dict:
    """도구 실행"""
    try:
        # 🔍 기업 검색
        if name == "find_company":
            return find_company_by_name(arguments["query"])
        
        # 📋 공시 검색
        elif name == "search_disclosures":
            params = {}
            if arguments.get("corp_code"):
                params["corp_code"] = arguments["corp_code"]
            if arguments.get("bgn_de"):
                params["bgn_de"] = arguments["bgn_de"]
            if arguments.get("end_de"):
                params["end_de"] = arguments["end_de"]
            if arguments.get("corp_cls"):
                params["corp_cls"] = arguments["corp_cls"]
            params["page_no"] = arguments.get("page_no", 1)
            params["page_count"] = arguments.get("page_count", 10)
            return call_dart_api("list.json", params)
        
        # 🏢 기업 정보
        elif name == "get_company_info":
            return call_dart_api("company.json", {"corp_code": arguments["corp_code"]})
        
        # 💰 주요 재무계정
        elif name == "get_financial_account":
            params = {
                "corp_code": arguments["corp_code"],
                "bsns_year": arguments["bsns_year"],
                "reprt_code": arguments["reprt_code"],
            }
            if arguments.get("fs_div"):
                params["fs_div"] = arguments["fs_div"]
            return call_dart_api("fnlttSinglAcnt.json", params)
        
        # 📊 전체 재무제표
        elif name == "get_full_financial_statement":
            params = {
                "corp_code": arguments["corp_code"],
                "bsns_year": arguments["bsns_year"],
                "reprt_code": arguments["reprt_code"],
            }
            if arguments.get("fs_div"):
                params["fs_div"] = arguments["fs_div"]
            return call_dart_api("fnlttSinglAcntAll.json", params)
        
        # 💵 배당 정보
        elif name == "get_dividend_info":
            return call_dart_api("alotMatter.json", {
                "corp_code": arguments["corp_code"],
                "bsns_year": arguments["bsns_year"],
                "reprt_code": arguments["reprt_code"],
            })
        
        # 👔 임원 현황
        elif name == "get_executives":
            return call_dart_api("exctvSttus.json", {
                "corp_code": arguments["corp_code"],
                "bsns_year": arguments["bsns_year"],
                "reprt_code": arguments["reprt_code"],
            })
        
        # 👥 직원 현황
        elif name == "get_employees":
            return call_dart_api("empSttus.json", {
                "corp_code": arguments["corp_code"],
                "bsns_year": arguments["bsns_year"],
                "reprt_code": arguments["reprt_code"],
            })
        
        # 📈 최대주주
        elif name == "get_largest_shareholders":
            return call_dart_api("hyslrSttus.json", {
                "corp_code": arguments["corp_code"],
                "bsns_year": arguments["bsns_year"],
                "reprt_code": arguments["reprt_code"],
            })
        
        else:
            return {"error": f"알 수 없는 도구: {name}"}
            
    except Exception as e:
        return {"error": str(e)}


def handle_mcp_message(message: dict) -> dict:
    """MCP 메시지 처리"""
    method = message.get("method", "")
    msg_id = message.get("id")
    params = message.get("params", {})

    response = {"jsonrpc": "2.0", "id": msg_id}

    try:
        if method == "initialize":
            response["result"] = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "opendart-mcp", "version": "0.2.0"},
            }
        elif method == "tools/list":
            response["result"] = {"tools": get_tools()}
        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            result = call_tool(tool_name, arguments)
            response["result"] = {
                "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
            }
        elif method == "notifications/initialized":
            return {}
        else:
            response["error"] = {"code": -32601, "message": f"Method not found: {method}"}
    except Exception as e:
        response["error"] = {"code": -32603, "message": str(e)}

    return response


class handler(BaseHTTPRequestHandler):
    """Vercel Serverless Function Handler"""
    
    def do_GET(self):
        """GET 요청 처리"""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        response = {
            "name": "OpenDART MCP Server",
            "version": "0.2.0",
            "description": "한국 금융감독원 전자공시시스템(DART) API MCP 서버",
            "tools": [t["name"] for t in get_tools()],
            "quick_start": {
                "1_find_company": "find_company로 기업명 검색 → corp_code 획득",
                "2_get_info": "corp_code로 재무정보, 임원, 배당 등 조회",
            },
            "major_companies": {
                "삼성전자": "00126380",
                "SK하이닉스": "00164779",
                "네이버": "00266961",
                "카카오": "00258801",
            }
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def do_POST(self):
        """POST 요청 처리 (MCP 메시지)"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            message = json.loads(body)
            response = handle_mcp_message(message)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        """CORS 프리플라이트"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
