
# YouTube Channel Analysis Project

본 프로젝트는 YouTube 채널 데이터를 분석하여 채널 성과와 사용자 참여도를 심층적으로 이해하고, 데이터 기반으로 의사결정을 지원하기 위해 설계되었습니다. Python을 활용하여 데이터 처리, 분석 및 시각화를 수행하며, 분석 결과는 주요 성과를 시각적으로 표현합니다.

---

## 🌟 프로젝트 배경 및 목적

YouTube는 개인 창작자와 기업 모두에게 중요한 플랫폼으로, 데이터 분석을 통해 다음과 같은 목표를 달성할 수 있습니다:

1. **데이터 중심의 의사결정 지원**: 데이터를 기반으로 성과를 평가하고 개선 방향을 제시.
2. **사용자 참여도 분석**: 댓글, 좋아요, 조회수 패턴을 분석하여 사용자 반응을 이해.
3. **자동화된 데이터 분석 제공**: 재사용 가능한 데이터 처리 및 분석 워크플로우 제공.

---

## 📂 프로젝트 개요

### 주요 질문
- 어떤 콘텐츠가 가장 높은 조회수와 반응을 얻고 있는가?
- 사용자들이 댓글에서 자주 사용하는 키워드는 무엇인가?
- 특정 기간 동안 채널의 구독자 증가율은 어떻게 변화했는가?
- 분석 결과를 통해 채널의 성과를 개선하기 위해 어떤 전략이 필요한가?

---

## 📋 주요 기능 및 모듈

### 데이터 전처리
- **결측치 및 이상치 처리**: NaN 및 불완전한 데이터를 제거.
- **텍스트 정제 및 처리**: 댓글과 제목에서 불필요한 단어를 제거하고 키워드를 추출.
- **날짜 및 시간 처리**: 업로드 날짜를 분석 가능한 형식으로 변환.

### 데이터 분석
- **구독자 성장률 분석**: 구독자의 월별 성장률을 계산 및 시각화.
- **조회수-반응 상관관계 분석**: 조회수와 좋아요, 댓글 간의 상관관계를 분석.
- **사용자 행동 분석**: 댓글 길이, 빈도, 참여도와 같은 사용자 행동 패턴 평가.

### 데이터 시각화
- **막대 그래프**: 동영상별 조회수와 좋아요를 비교.
- **히트맵**: 시간대별 사용자 활동 패턴을 표현.
- **워드 클라우드**: 댓글과 제목에서 자주 사용되는 단어를 시각적으로 나타냄.

---

## 📊 분석 결과 예시

### 1️⃣ 성과 분석
- **구독자 성장률**: 월별 구독자 수 변화를 시각화하여 성장 추이를 파악.
- **조회수-반응 상관관계**: 조회수와 좋아요/댓글 수 사이의 상관관계를 그래프로 표현.

### 2️⃣ 워드 클라우드 예시
- 자주 사용되는 키워드를 워드 클라우드로 시각화:
  - 예시: "재미있다", "유익하다", "다시 보고 싶다"와 같은 단어.

### 3️⃣ 사용자 참여도 분석
- 댓글과 좋아요 비율을 통해 사용자 참여도를 계산:
  - 예시: 특정 동영상의 평균 댓글 비율이 5%인 반면, 좋아요 비율은 20%.

---

## 🛠️ 기술 스택

- **Python**: 데이터 처리 및 분석.
- **Jupyter Notebook**: 대화형 데이터 분석 환경 제공.
- **주요 라이브러리**:
  - 데이터 처리: `pandas`, `numpy`
  - 시각화: `matplotlib`, `seaborn`, `wordcloud`
  - 기타: `collections`, `os`, `re`, `tabulate`

---

## 📊 데이터셋

- **데이터 출처**: YouTube API 또는 CSV 데이터.
- **데이터 컬럼**:
  - 동영상 ID, 제목, 업로드 날짜, 조회수, 좋아요 수, 댓글 수 등.

> **참고**: 실행 전 데이터셋을 `datasets/` 디렉토리에 저장하거나 YouTube API를 활용해 데이터를 가져와야 합니다.

---

## 🛠️ 설치 및 실행 방법

### 시스템 요구사항
- Python 3.8 이상
- Jupyter Notebook 설치

### 설치 단계
1. 프로젝트를 클론하거나 다운로드:
   ```bash
   git clone https://github.com/your-repo/Youtube_Channel_Analysis_Project.git
   cd Youtube_Channel_Analysis_Project
   ```
2. 의존성 설치:
   ```bash
   pip install -r requirements.txt
   ```
3. Jupyter Notebook 실행:
   ```bash
   jupyter notebook Youtube_Channel_Analysis_Project.ipynb
   ```

---

## 🚀 향후 계획

1. **머신러닝 모델 적용**:
   - 동영상 성공 여부 예측 모델 개발.
   - 구독자 성장률 예측을 위한 회귀 분석.
2. **실시간 대시보드 구축**:
   - Streamlit 또는 Dash를 활용한 실시간 데이터 시각화.
3. **다국어 분석 확장**:
   - 다양한 언어로 댓글 분석 지원.

