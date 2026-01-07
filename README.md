# OpenDART MCP Server 🇰🇷

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployable-black.svg)](https://vercel.com)

한국 금융감독원 전자공시시스템(DART) API를 MCP(Model Context Protocol)로 제공하는 서버입니다.

> **AI 어시스턴트가 한국 상장기업의 공시, 재무정보, 기업정보를 실시간으로 조회할 수 있습니다.**
>
> 📅 **지원 데이터**: 2023년 ~ 2025년 최신 (3분기) 모두 조회 가능!

## ✨ 주요 기능 (14개 도구)

### 🔍 기업 검색
| 기능 | 설명 |
|------|------|
| `find_company` | **기업명으로 corp_code 검색** (114,951개 전체 기업) |

### 📋 공시/기업정보
| 기능 | 설명 |
|------|------|
| `search_disclosures` | 공시 검색 (기간, 기업, 시장 필터링) |
| `get_company_info` | 기업 기본정보 (회사명, 대표자, 업종 등) |

### 💰 재무정보
| 기능 | 설명 |
|------|------|
| `get_financial_account` | 주요 재무계정 (자산, 부채, 매출, 영업이익 등) |
| `get_full_financial_statement` | 전체 재무제표 (BS, IS, CF 등) |
| `get_financial_index` | ⭐ **주요 재무지표** (ROE, ROA, 부채비율, PER, PBR 등) |
| `get_dividend_info` | 배당 정보 |

### 👥 인적정보
| 기능 | 설명 |
|------|------|
| `get_executives` | 임원 현황 |
| `get_employees` | 직원 현황 (평균 급여, 근속연수 등) |

### 📈 지분정보
| 기능 | 설명 |
|------|------|
| `get_largest_shareholders` | 최대주주 현황 |
| `get_major_stock` | ⭐ **대량보유 상황보고** (5%룰 - 5% 이상 주주 변동) |
| `get_executive_stock` | ⭐ **임원·주요주주 지분 변동** |

### 💵 자본/주식정보
| 기능 | 설명 |
|------|------|
| `get_capital_change` | ⭐ **증자/감자 현황** |
| `get_treasury_stock` | ⭐ **자기주식 취득/처분 현황** |

---

## 🚀 빠른 시작

### 방법 1: 배포된 서버 사용 (권장) ⚡

**별도 설정 없이 바로 사용 가능!**

```
https://dart-mcp-self.vercel.app/sse
```

MCP 클라이언트에 위 URL만 추가하면 끝!

### 방법 2: 직접 Vercel 배포

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Dayoooun/dart-mcp)

Fork 후 Vercel에 연결하면 자동 배포됩니다.

### 방법 3: 로컬 실행

```bash
git clone https://github.com/Dayoooun/dart-mcp.git
cd dart-mcp

# 의존성 설치 및 실행
pip install -e .
opendart-mcp
```

---

## ⚙️ MCP 클라이언트 설정

### Cursor IDE

`~/.cursor/mcp.json` 파일에 추가:

```json
{
  "mcpServers": {
    "opendart": {
      "type": "http",
      "url": "https://dart-mcp-self.vercel.app/sse"
    }
  }
}
```

### Claude Desktop

`claude_desktop_config.json`에 추가:

```json
{
  "mcpServers": {
    "opendart": {
      "url": "https://dart-mcp-self.vercel.app/sse"
    }
  }
}
```

### 로컬 실행 시 (stdio)

```json
{
  "mcpServers": {
    "opendart": {
      "command": "opendart-mcp"
    }
  }
}
```

---

## 📖 사용 예시

### 💡 핵심: 기업명으로 검색하기

**corp_code를 몰라도 됩니다!** `find_company`로 검색하세요:

> "인산가라는 회사 재무제표 보여줘"

AI가 자동으로:
1. `find_company("인산가")` → corp_code 획득
2. `get_financial_account(corp_code=...)` → 재무정보 조회

### 기본 사용

```
"삼성전자 기업 정보 알려줘"
"네이버의 2023년 연간 재무제표 보여줘"
"카카오 직원 현황과 평균 급여 알려줘"
```

### 잘 모르는 기업 조회

```
"오르비텍이라는 회사의 직원 현황 알려줘"
"나노씨엠에스 임원 현황 보여줘"
"두산로보틱스 재무정보 조회해줘"
```

### 영문/한글 동시 검색 지원

```
"NAVER 재무정보" → 네이버 찾음
"네이버 재무정보" → NAVER 찾음
"LG 계열사 목록" → LG전자, LG화학, LG에너지솔루션 등 찾음
```

---

## 🏢 주요 기업 고유번호

자주 사용되는 대기업은 corp_code를 직접 사용해도 됩니다:

| 기업명 | corp_code | 종목코드 |
|--------|-----------|----------|
| 삼성전자 | 00126380 | 005930 |
| SK하이닉스 | 00164779 | 000660 |
| LG전자 | 00401731 | 066570 |
| 현대자동차 | 00164742 | 005380 |
| 네이버 | 00266961 | 035420 |
| 카카오 | 00258801 | 035720 |
| 삼성SDI | 00126371 | 006400 |
| LG화학 | 00356361 | 051910 |
| 셀트리온 | 00421045 | 068270 |
| 포스코홀딩스 | 00126186 | 005490 |

**그 외 기업**: `find_company`로 검색하세요! (114,951개 기업 지원)

---

## 📋 API 파라미터 가이드

### 보고서 코드 (reprt_code)

| 코드 | 설명 | 특징 |
|------|------|------|
| 11011 | 사업보고서 (연간) | 가장 상세, 직원현황 포함 |
| 11012 | 반기보고서 | 6개월 실적 |
| 11013 | 1분기보고서 | 3개월 실적 |
| 11014 | 3분기보고서 | 9개월 실적 |

### 재무제표 구분 (fs_div)

| 값 | 설명 |
|----|------|
| CFS | 연결재무제표 (자회사 포함, 일반적으로 사용) |
| OFS | 개별재무제표 (해당 법인만) |

### 시장 구분 (corp_cls)

| 값 | 설명 |
|----|------|
| Y | 유가증권시장 (코스피) |
| K | 코스닥시장 |
| N | 코넥스시장 |
| E | 기타 (비상장 등) |

### 재무지표 분류코드 (idx_cl_code)

`get_financial_index` API에서 사용 **(필수)**:

| 코드 | 설명 | 포함 지표 |
|------|------|----------|
| M210000 | 수익성지표 | ROE, ROA, 영업이익률, 순이익률 등 |
| M220000 | 안정성지표 | 부채비율, 유동비율, 당좌비율 등 |
| M230000 | 성장성지표 | 매출증가율, 영업이익증가율 등 |
| M240000 | 활동성지표 | 총자산회전율, 재고자산회전율 등 |

---

## 🔧 find_company 상세

기업명으로 corp_code를 검색합니다. **114,951개 전체 기업** 데이터에서 즉시 검색!

**특징:**
- 🚀 빠른 검색 (~50ms) - 미리 로드된 데이터 사용
- 🔄 한글/영문 동시 검색 - "네이버" 검색 시 "NAVER"도 찾음
- ⭐ 상장기업 우선 정렬

**요청:**
```json
{
  "query": "네이버"
}
```

**응답:**
```json
{
  "status": "000",
  "companies": [
    {
      "corp_code": "00266961",
      "corp_name": "NAVER",
      "stock_code": "035420"
    },
    {
      "corp_code": "01246715",
      "corp_name": "네이버랩스",
      "stock_code": ""
    }
  ]
}
```

---

## 🛠️ 개발

### 프로젝트 구조

```
dart-mcp/
├── api/
│   ├── index.py          # Vercel 서버리스 함수 (SSE)
│   └── companies.json    # 기업 데이터 (114,951개)
├── scripts/
│   └── update_companies.py  # 기업 데이터 업데이트 스크립트
├── src/opendart_mcp/
│   ├── server.py         # MCP 서버 핵심 로직
│   ├── api/              # API 모듈
│   └── models/           # Pydantic 모델
├── vercel.json           # Vercel 설정
└── pyproject.toml        # 패키지 설정
```

### 로컬 개발

```bash
# uv 사용 (권장)
uv sync
uv run opendart-mcp

# 또는 pip 사용
pip install -e ".[dev]"
opendart-mcp
```

### 기업 데이터 업데이트

`find_company`는 `api/companies.json` 파일을 사용합니다. 새로운 기업이 등록되면 월 1회 정도 업데이트를 권장합니다:

```bash
# 기업 데이터 업데이트 (114,000+ 기업)
python scripts/update_companies.py

# 변경사항 배포
git add api/companies.json
git commit -m "Update companies data"
git push
```

---

## 🤝 기여하기

기여를 환영합니다! 

1. Fork
2. Feature branch 생성 (`git checkout -b feature/amazing-feature`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Pull Request

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능합니다.

---

## 🔗 관련 링크

- [OpenDART 공식 사이트](https://opendart.fss.or.kr/)
- [OpenDART API 문서](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001)
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)

---

## ⭐ Star History

이 프로젝트가 도움이 되셨다면 ⭐ Star를 눌러주세요!
