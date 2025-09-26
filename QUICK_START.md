# 🚀 YouTube Channel Analysis - 빠른 시작 가이드

## 📋 체크리스트 (5분 완료)

### ✅ 1단계: 프로젝트 다운로드
```bash
git clone https://github.com/CY-HYUN/Youtube-Channel-Anaylsis-Project.git
cd Youtube-Channel-Anaylsis-Project
```

### ✅ 2단계: 간편 실행
```bash
python run_analysis.py
```
> 💡 이 명령어 하나로 패키지 설치부터 분석까지 모든 것이 자동으로 실행됩니다!

---

## 🎯 3가지 실행 방법

### 🟢 방법 1: 초보자용 (추천) ⭐
```bash
python run_analysis.py
```
- ✅ 패키지 자동 설치
- ✅ 대화형 메뉴
- ✅ 오류 처리 포함
- ✅ 결과 자동 표시

### 🟡 방법 2: 고급 사용자용
```bash
# API 키 설정 (Windows)
set YOUTUBE_API_KEY=your_api_key_here

# 분석 실행
python main.py --mode all --channel-id UCuTITJp_8VXjjthWdPdmwKA --max-videos 50
```

### 🟣 방법 3: Jupyter 노트북
```bash
jupyter notebook Youtube_Channel_Anaylsis_Project.ipynb
```

---

## 🔧 문제 해결

### Q: "모듈을 찾을 수 없습니다" 오류
**A:** 다음 명령어로 패키지를 설치하세요:
```bash
pip install -r requirements.txt
```

### Q: API 키 관련 오류
**A:** YouTube Data API 키가 필요합니다:
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 생성 → YouTube Data API v3 활성화
3. API 키 생성
4. 환경변수 설정:
   - Windows: `set YOUTUBE_API_KEY=your_key`
   - Linux/Mac: `export YOUTUBE_API_KEY=your_key`

### Q: 채널 ID를 어떻게 찾나요?
**A:** YouTube 채널 URL에서 확인:
- `https://www.youtube.com/channel/UCuTITJp_8VXjjthWdPdmwKA` → `UCuTITJp_8VXjjthWdPdmwKA`
- `https://www.youtube.com/@username` → 채널 정보에서 채널 ID 확인

---

## 📊 실행 결과 확인

### 생성되는 파일들:
- 📄 `data/raw/` - 수집된 원본 데이터 (CSV)
- 🖼️ `visualizations/` - 생성된 차트 및 그래프
- 📊 터미널에 실시간 분석 결과 표시

### 예상 실행 시간:
- 데이터 수집: 1-2분 (채널 크기에 따라)
- 분석 및 시각화: 30초-1분
- 총 소요시간: 2-3분

---

## 🎉 성공! 다음 단계

분석이 완료되면:

1. **결과 확인**: `visualizations/` 폴더의 차트들 확인
2. **상세 분석**: Jupyter 노트북으로 더 깊은 분석
3. **데이터 활용**: `data/raw/` 폴더의 CSV 파일들 활용

---

## 🆘 도움이 필요하신가요?

- 📧 이슈 제보: [GitHub Issues](https://github.com/CY-HYUN/Youtube-Channel-Anaylsis-Project/issues)
- 📖 상세 문서: `README.md` 확인
- 💡 예시 코드: `notebooks/data_analysis.py` 참조