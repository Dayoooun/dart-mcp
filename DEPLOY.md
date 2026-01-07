# Vercel 배포 가이드 🚀

이 문서는 OpenDART MCP 서버를 Vercel에 배포하는 방법을 설명합니다.

## 1. 사전 준비

### OpenDART API 키 발급

1. [OpenDART](https://opendart.fss.or.kr/) 접속
2. 회원가입 후 로그인
3. 인증키 신청 → API 키 발급
4. 발급받은 키 복사해두기

## 2. Vercel 배포

### 방법 A: Vercel CLI 사용

```bash
# Vercel CLI 설치
npm i -g vercel

# 로그인
vercel login

# 프로젝트 디렉토리에서 배포
cd dart-mcp
vercel

# 환경변수 설정
vercel env add OPENDART_API_KEY
# 프롬프트에서 API 키 입력

# 프로덕션 배포
vercel --prod
```

### 방법 B: GitHub 연동

1. 이 프로젝트를 GitHub에 푸시
2. [Vercel](https://vercel.com)에 로그인
3. "New Project" 클릭
4. GitHub 리포지토리 선택
5. 환경변수 설정:
   - Name: `OPENDART_API_KEY`
   - Value: `발급받은 API 키`
6. Deploy 클릭

## 3. 환경변수 관리

### Vercel Secret 사용 (권장)

```bash
# Secret 생성
vercel secrets add opendart-api-key "your_actual_api_key"

# vercel.json에서 참조
# "OPENDART_API_KEY": "@opendart-api-key"
```

### Vercel 대시보드에서 설정

1. Vercel Dashboard → 프로젝트 선택
2. Settings → Environment Variables
3. `OPENDART_API_KEY` 추가

## 4. 배포 확인

배포가 완료되면 다음 엔드포인트에 접속해 확인:

```
https://your-project.vercel.app/         # API 정보
https://your-project.vercel.app/health   # 헬스 체크
https://your-project.vercel.app/sse      # MCP 엔드포인트
```

## 5. MCP 클라이언트 연결

### Cursor IDE

`~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "opendart": {
      "url": "https://your-project.vercel.app/sse"
    }
  }
}
```

### Claude Desktop

`claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "opendart": {
      "url": "https://your-project.vercel.app/sse"
    }
  }
}
```

## 6. 테스트

### cURL로 직접 테스트

```bash
# API 정보 확인
curl https://your-project.vercel.app/

# 도구 목록 조회
curl -X POST https://your-project.vercel.app/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# 삼성전자 정보 조회
curl -X POST https://your-project.vercel.app/sse \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/call",
    "params":{
      "name":"get_company_info",
      "arguments":{"corp_code":"00126380"}
    }
  }'
```

## 7. 트러블슈팅

### 500 에러 발생 시

1. Vercel Logs 확인 (Dashboard → Deployments → Logs)
2. 환경변수 `OPENDART_API_KEY` 설정 확인
3. API 키가 유효한지 확인

### 타임아웃 발생 시

- Vercel Serverless 함수는 기본 10초 타임아웃
- 복잡한 쿼리는 시간이 걸릴 수 있음
- Pro 플랜에서 타임아웃 연장 가능

### CORS 에러 시

- `vercel.json`에 CORS 헤더가 이미 설정되어 있음
- 브라우저에서 직접 호출 시 문제없어야 함

## 8. 업데이트 배포

```bash
# 코드 수정 후
git add .
git commit -m "Update server"
git push origin main

# GitHub 연동 시 자동 배포됨
# 또는 수동 배포
vercel --prod
```

---

## 📝 참고 사항

- Vercel Hobby 플랜: 무료, 월 100GB 대역폭
- 서버리스 함수 실행 시간: 10초 (Pro: 60초)
- 동시 실행: 1000개

자세한 내용은 [Vercel 문서](https://vercel.com/docs)를 참조하세요.

