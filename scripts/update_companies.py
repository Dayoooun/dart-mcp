"""OpenDART 기업 목록 업데이트 스크립트

corpCode.xml을 다운로드하여 companies.json으로 변환합니다.
월 1회 정도 실행하여 최신 기업 목록을 유지하세요.

사용법:
    python scripts/update_companies.py
"""
import urllib.request
import zipfile
import io
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

API_KEY = "d64dadc7b8236e0ae2e6c3560ef400cc12f2c705"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "api", "companies.json")


def download_corp_code():
    """corpCode.xml 다운로드 (ZIP 형태)"""
    url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={API_KEY}"
    print(f"Downloading from {url}...")
    
    response = urllib.request.urlopen(url, timeout=60)
    data = response.read()
    print(f"Downloaded {len(data):,} bytes")
    
    return data


def parse_corp_code(zip_data):
    """ZIP 파일에서 XML 파싱하여 기업 목록 추출"""
    companies = []
    
    with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
        # ZIP 내 파일 목록
        file_list = zf.namelist()
        print(f"ZIP contains: {file_list}")
        
        # CORPCODE.xml 읽기
        xml_filename = file_list[0]  # 보통 CORPCODE.xml
        with zf.open(xml_filename) as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            for corp in root.findall('.//list'):
                corp_code = corp.findtext('corp_code', '')
                corp_name = corp.findtext('corp_name', '')
                stock_code = corp.findtext('stock_code', '')
                modify_date = corp.findtext('modify_date', '')
                
                # 기업 코드와 이름이 있는 경우만 추가
                if corp_code and corp_name:
                    company = {
                        "c": corp_code,      # corp_code (압축)
                        "n": corp_name,      # corp_name (압축)
                    }
                    # 상장 기업만 stock_code 추가 (용량 절약)
                    if stock_code and stock_code.strip():
                        company["s"] = stock_code.strip()
                    
                    companies.append(company)
    
    print(f"Parsed {len(companies):,} companies")
    return companies


def save_companies(companies):
    """JSON 파일로 저장"""
    output = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(companies),
        "companies": companies
    }
    
    # 디렉토리 생성
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # JSON 저장 (압축된 형태)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, separators=(',', ':'))
    
    file_size = os.path.getsize(OUTPUT_PATH)
    print(f"Saved to {OUTPUT_PATH}")
    print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")


def main():
    print("=" * 50)
    print("OpenDART 기업 목록 업데이트")
    print("=" * 50)
    
    # 1. 다운로드
    zip_data = download_corp_code()
    
    # 2. 파싱
    companies = parse_corp_code(zip_data)
    
    # 3. 저장
    save_companies(companies)
    
    # 4. 통계
    listed = sum(1 for c in companies if 's' in c)
    print(f"\n통계:")
    print(f"  - 전체 기업: {len(companies):,}개")
    print(f"  - 상장 기업: {listed:,}개")
    print(f"  - 비상장 기업: {len(companies) - listed:,}개")
    
    print("\n✅ 완료! api/companies.json이 업데이트되었습니다.")
    print("git add/commit/push 후 Vercel에 재배포하세요.")


if __name__ == "__main__":
    main()

