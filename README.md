# 🎬 YouTube Channel Analysis Project

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained-Yes-green.svg)](https://github.com/CY-HYUN/Youtube-Channel-Anaylsis-Project)

YouTube 채널의 성과와 트렌드를 분석하는 포괄적인 데이터 분석 도구입니다. YouTube Data API v3를 활용하여 채널 데이터를 수집하고, 다양한 지표를 통해 심도 있는 분석과 시각화를 제공합니다.

## ✨ 주요 기능

### 📊 **데이터 수집 & 처리**
- YouTube Data API v3를 통한 자동 데이터 수집
- 채널 정보, 영상 메타데이터, 통계 정보 통합 수집
- 데이터 전처리 및 정제 파이프라인

### 🔍 **고급 분석 기능**
- **성과 분석**: 조회수, 좋아요, 댓글 수 등 핵심 지표 분석
- **참여도 분석**: 사용자 참여율 및 상호작용 패턴 분석
- **트렌드 분석**: 시간별 성과 변화 및 업로드 패턴 분석
- **콘텐츠 분석**: 영상 길이별 성과, 제목 키워드 분석
- **AI 인사이트**: 자동화된 분석 결과 및 개선점 제안

### 📈 **시각화 도구**
- 상위 성과 영상 랭킹 차트
- 시간별 트렌드 그래프
- 참여도 분석 대시보드
- 워드클라우드 및 키워드 분석
- 성과 지표 상관관계 히트맵

### 🛠 **개발자 친화적 기능**
- 모듈화된 코드 구조
- 포괄적인 단위 테스트
- 상세한 문서화 및 사용 예시
- CLI 및 프로그래밍 인터페이스 지원

## 🚀 빠른 시작

### ⚡ 초보자를 위한 원클릭 실행 (추천)
```bash
# 1. 프로젝트 다운로드
git clone https://github.com/CY-HYUN/Youtube-Channel-Anaylsis-Project.git
cd Youtube-Channel-Anaylsis-Project

# 2. 간편 실행기 사용 (패키지 설치 + 분석 실행)
python run_analysis.py
```
> 🎯 **추천**: 처음 사용하시는 분은 `run_analysis.py`를 사용하세요!

### 🔧 고급 사용자를 위한 수동 실행

#### 1. 프로젝트 설치
```bash
git clone https://github.com/CY-HYUN/Youtube-Channel-Anaylsis-Project.git
cd Youtube-Channel-Anaylsis-Project
pip install -r requirements.txt
```

#### 2. YouTube API 키 설정
```bash
# Windows
set YOUTUBE_API_KEY=your_youtube_api_key_here

# Linux/Mac
export YOUTUBE_API_KEY="your_youtube_api_key_here"
```
> 📝 API 키 발급 방법은 [Google Cloud Console](https://console.cloud.google.com/)을 참조하세요.

#### 3. 분석 실행
```bash
# 전체 분석 파이프라인 실행
python main.py --mode all --channel-id UCuTITJp_8VXjjthWdPdmwKA --max-videos 100

# 단계별 실행
python main.py --mode collect --channel-id UCuTITJp_8VXjjthWdPdmwKA
python main.py --mode analyze
python main.py --mode visualize
```

## 📁 프로젝트 구조

```
Youtube-Channel-Analysis-Project/
├── 📊 data/
│   ├── raw/                    # 원본 데이터
│   ├── processed/              # 전처리된 데이터
│   └── sample_data.json        # 샘플 데이터
├── 🔧 src/
│   ├── data_collection/        # 데이터 수집 모듈
│   │   ├── __init__.py
│   │   └── youtube_api.py      # YouTube API 데이터 수집
│   ├── analysis/              # 분석 모듈
│   │   ├── __init__.py
│   │   └── channel_analyzer.py # 채널 분석 로직
│   └── visualization/         # 시각화 모듈
│       ├── __init__.py
│       └── charts.py          # 차트 생성
├── 📓 notebooks/              # 분석 노트북 및 스크립트
│   └── data_analysis.py       # 독립 실행 분석 스크립트
├── 📋 tests/                  # 단위 테스트
├── 📚 docs/                   # 문서화
├── ⚙️  config/                # 설정 파일
├── 🎨 visualizations/         # 생성된 시각화 결과
├── 📓 Youtube_Channel_Analysis_Project.ipynb  # 원본 주피터 노트북
├── 🚀 main.py                 # 메인 실행 파일 (고급 사용자용)
├── ⚡ run_analysis.py         # 간편 실행기 (초보자용)
├── 📋 requirements.txt        # 의존성 목록
└── 📄 README.md
```

### 🎯 핵심 실행 파일
- **`run_analysis.py`**: 초보자용 간편 실행기 (패키지 설치 + 분석 실행)
- **`main.py`**: 고급 사용자용 CLI 도구 (세부 옵션 제어)
- **`notebooks/data_analysis.py`**: Jupyter 없이 독립 실행 가능한 분석 스크립트

## 💻 사용법

### CLI 인터페이스
```bash
# 여러 채널 동시 분석
python main.py --mode all \
    --channel-id UCuTITJp_8VXjjthWdPdmwKA \
    --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw \
    --max-videos 50

# 특정 디렉토리 지정
python main.py --mode all \
    --channel-id UCuTITJp_8VXjjthWdPdmwKA \
    --data-dir custom_data/ \
    --output-dir custom_visualizations/
```

### 프로그래밍 인터페이스
```python
from src.data_collection.youtube_api import YouTubeDataCollector
from src.analysis.channel_analyzer import ChannelAnalyzer
from src.visualization.charts import YouTubeVisualizer

# 데이터 수집
collector = YouTubeDataCollector(api_key)
data = collector.collect_channel_data(channel_id)

# 분석 실행
analyzer = ChannelAnalyzer("channel_info.csv", "videos.csv")
insights = analyzer.generate_insights()

# 시각화 생성
visualizer = YouTubeVisualizer()
visualizer.save_all_charts(videos_df, "output_dir")
```

## 📊 분석 결과 예시

### 채널 요약 정보
```
채널명: Tech Education Hub
구독자 수: 1,200,000명
총 영상 수: 500개
평균 조회수: 100,000회
평균 참여율: 6.8%
```

### AI 생성 인사이트
- 💡 최고 조회수 영상이 평균보다 15배 높아 바이럴 콘텐츠 특성 분석 필요
- 💡 화요일에 가장 많이 업로드하는 패턴을 보입니다
- 💡 20-30분 길이의 영상이 가장 높은 평균 조회수를 기록

## 🧪 테스트

```bash
# 단위 테스트 실행
python -m pytest tests/ -v

# 특정 테스트 실행
python tests/test_analyzer.py
```

## 📚 문서

- 📖 [API 설정 가이드](docs/API_SETUP.md)
- 💡 [사용 예시 및 튜토리얼](docs/USAGE_EXAMPLES.md)

## 🛠 기술 스택

### 핵심 기술
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)

### 데이터 시각화
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat&logo=python&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-388E3C?style=flat&logo=python&logoColor=white)

### API & 데이터
![YouTube](https://img.shields.io/badge/YouTube_Data_API-FF0000?style=flat&logo=youtube&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)

## 🔄 향후 개발 계획

- [ ] **실시간 모니터링 시스템** - 채널 성과 실시간 추적
- [ ] **머신러닝 예측 모델** - 영상 성과 예측 및 최적화 제안
- [ ] **웹 대시보드** - 인터랙티브 분석 대시보드 개발
- [ ] **경쟁사 분석** - 유사 채널 벤치마킹 기능
- [ ] **자동화된 보고서** - 주기적 분석 보고서 생성
- [ ] **A/B 테스트 도구** - 콘텐츠 전략 실험 지원

## 🤝 기여하기

프로젝트에 기여해주시는 모든 분들을 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙋‍♂️ 문의 및 지원

프로젝트 관련 문의사항이나 버그 리포트는 [Issues](https://github.com/CY-HYUN/Youtube-Channel-Anaylsis-Project/issues) 탭을 이용해주세요.

---

⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!

**Made with ❤️ by [CY-HYUN](https://github.com/CY-HYUN)**