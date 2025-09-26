# YouTube Data API v3 설정 가이드

## 개요

이 문서는 YouTube Channel Analysis Project에서 YouTube Data API v3를 사용하기 위한 설정 방법을 설명합니다.

## API 키 발급

### 1. Google Cloud Console 접속
1. [Google Cloud Console](https://console.cloud.google.com/)에 접속
2. Google 계정으로 로그인

### 2. 새 프로젝트 생성 (선택사항)
1. 콘솔 상단의 프로젝트 드롭다운 클릭
2. "새 프로젝트" 선택
3. 프로젝트 이름 입력 (예: "YouTube-Channel-Analysis")
4. "만들기" 클릭

### 3. YouTube Data API v3 활성화
1. 좌측 메뉴에서 "API 및 서비스" > "라이브러리" 클릭
2. "YouTube Data API v3" 검색
3. YouTube Data API v3 선택
4. "사용" 버튼 클릭

### 4. API 키 생성
1. 좌측 메뉴에서 "API 및 서비스" > "사용자 인증 정보" 클릭
2. "사용자 인증 정보 만들기" > "API 키" 클릭
3. API 키가 생성됨 (안전하게 보관 필요)

### 5. API 키 제한 설정 (권장)
1. 생성된 API 키 옆의 편집 버튼 클릭
2. "애플리케이션 제한사항"에서 적절한 제한 설정
3. "API 제한사항"에서 "키 제한" 선택
4. "YouTube Data API v3" 선택
5. "저장" 클릭

## API 키 설정

### 방법 1: 환경변수 사용 (권장)

**Windows:**
```cmd
set YOUTUBE_API_KEY=your_api_key_here
```

**macOS/Linux:**
```bash
export YOUTUBE_API_KEY=your_api_key_here
```

**영구 설정 (macOS/Linux):**
```bash
echo 'export YOUTUBE_API_KEY=your_api_key_here' >> ~/.bashrc
source ~/.bashrc
```

### 방법 2: 설정 파일 사용

`config/api_keys.py` 파일 생성:
```python
# config/api_keys.py
YOUTUBE_API_KEY = "your_api_key_here"
```

⚠️ **주의사항**: 이 파일을 Git에 커밋하지 마세요!

## API 사용량 및 제한사항

### 일일 할당량
- YouTube Data API v3는 일일 10,000 할당량 단위 제공
- 각 API 호출마다 다른 비용 소모

### 주요 API 호출 비용
| API 호출 | 비용 (할당량 단위) |
|---------|-----------------|
| channels.list | 1 |
| videos.list | 1 |
| playlistItems.list | 1 |
| search.list | 100 |

### 할당량 관리 팁
1. **캐싱 활용**: 같은 데이터를 반복 요청하지 않도록 캐싱
2. **배치 처리**: 여러 비디오 ID를 한 번에 조회 (최대 50개)
3. **필요한 필드만 요청**: `part` 매개변수로 필요한 데이터만 선택
4. **적절한 대기시간**: API 호출 간 적절한 지연 시간 설정

## 문제 해결

### 일반적인 오류

**403 Forbidden 오류:**
- API 키가 올바르지 않거나 API가 활성화되지 않음
- 할당량을 초과했을 가능성

**400 Bad Request 오류:**
- 잘못된 매개변수나 요청 형식
- 채널 ID나 비디오 ID 확인 필요

**429 Too Many Requests 오류:**
- API 호출이 너무 빠름
- 요청 간 지연시간 추가 필요

### 디버깅 방법

1. **API 호출 로그 확인**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Google API Explorer 사용**:
   - [Google API Explorer](https://developers.google.com/apis-explorer)에서 API 호출 테스트

3. **할당량 사용량 모니터링**:
   - Google Cloud Console > API 및 서비스 > 할당량에서 확인

## 보안 고려사항

1. **API 키 보안**:
   - API 키를 코드에 하드코딩하지 말 것
   - 환경변수나 별도 설정 파일 사용
   - API 키에 적절한 제한사항 설정

2. **키 순환**:
   - 정기적으로 API 키 갱신
   - 노출된 키는 즉시 삭제 후 재생성

3. **접근 제한**:
   - IP 주소 제한 설정 고려
   - 웹사이트 제한 설정 (웹 애플리케이션의 경우)

## 관련 링크

- [YouTube Data API v3 문서](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)
- [API 할당량 관리](https://developers.google.com/youtube/v3/getting-started#quota)
- [API 키 보안 모범 사례](https://cloud.google.com/docs/authentication/api-keys)