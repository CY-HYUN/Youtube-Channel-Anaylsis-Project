# 🎬 YouTube Channel Analysis Project

A comprehensive data analysis project that analyzes YouTube channel performance across different categories (Fashion, Mukbang, Travel) using data science techniques.

## 📊 Project Overview

This data science project analyzes YouTube channel performance metrics across three content categories using statistical methods and visualization techniques. The analysis focuses on Korean YouTube channels to identify optimal content strategies and performance patterns.

### 🎯 Analyzed Categories
- **패션 (Fashion)** - Fashion tutorials, reviews, and style content
- **먹방 (Mukbang/Food)** - Mukbang content and cooking videos
- **여행 (Travel)** - Travel vlogs, destination guides, and cultural content

### 🔬 Research Methodology
- **Bilingual Analysis**: All research conducted in Korean with English translations
- **Statistical Analysis**: Correlation analysis, outlier removal, and trend identification
- **Korean Text Processing**: Advanced Korean language processing for word cloud analysis
- **Time Series Analysis**: Upload pattern analysis and performance tracking
- **Performance Benchmarking**: Category-specific performance metrics

---

## 🔍 Main Analysis Features

### 1. **Word Cloud Analysis - 워드클라우드 분석**
**분야별 상위 5명의 유튜버들이 제목에 자주 사용하는 단어 분석**

**시각화:**
- **X축**: 없음 (워드클라우드 형식)
- **Y축**: 없음 (단어 크기로 빈도 표현)
- **표현 방식**: 단어의 크기가 클수록 사용 빈도가 높음

**예상 vs 실제:**
- **예상**: 각 분야별로 특징적인 키워드가 명확히 구분될 것
- **실제**:
  - 패션: "데일리룩", "코디", "OOTD", "하울" 등 스타일링 관련 단어 빈번
  - 먹방: "맛집", "먹방", "리뷰", "추천" 등 음식 관련 단어 집중
  - 여행: "브이로그", "여행", "힐링", "일상" 등 경험 공유 키워드 우세
  - 채널별로 고유한 톤앤매너와 키워드 전략이 명확히 구분됨

**주요 인사이트:**
- 성공적인 유튜버들은 검색 최적화된 키워드를 일관되게 사용
- 분야별 핵심 키워드가 조회수와 높은 상관관계
- 트렌드를 반영한 신조어 사용이 젊은 시청자층 확보에 유리

---

### 2. **Upload Timing Analysis - 업로드 타이밍 분석**
**각 분야 및 채널별 가장 높은 조회수를 기록하는 요일 및 시간대 분석**

**시각화:**
- **X축**: 요일 (월요일~일요일) / 시간대 (0~23시)
- **Y축**: 평균 조회수
- **그래프 형식**: 막대 그래프 (Bar plot) - 요일별/시간대별 2개 차트

**예상 vs 실제:**
- **예상**: 주말과 저녁 시간대(6-10시)에 모든 카테고리가 높은 조회수를 보일 것
- **실제**:
  - **패션**: 주중 오후(2-6시)와 주말 낮 시간대 강세 - 쇼핑 고려 시간대
  - **먹방**: 식사 시간대(12-1시, 6-8시) 집중, 요일 영향 적음 - 식욕 자극 타이밍
  - **여행**: 일요일 저녁(6-9시) 최고 성과 - 주말 여행 후 대리만족
  - 카테고리별로 최적 업로드 시간이 예상보다 명확히 차별화됨

**주요 인사이트:**
- 타겟 오디언스의 생활 패턴에 따라 최적 업로드 시간이 크게 달라짐
- 먹방은 시간대 영향이 크고, 패션/여행은 요일 영향이 더 큼
- 글로벌 시청자를 타겟하는 채널은 KST 기준 다른 패턴 보임

---

### 3. **Upload Frequency Analysis - 업로드 주기 분석**
**가장 최적의 업로드 주기가 며칠인지 파악 (이상치 제거 적용)**

**시각화:**
- **X축**: 업로드 주기 (1일, 2-3일, 4-5일, 6-7일, 8-14일, 15-30일)
- **Y축**: 평균 조회수 / 평균 좋아요수
- **그래프 형식**: 막대 그래프 2개 (조회수, 좋아요수) - 각 막대 위에 영상 개수(n) 표시

**예상 vs 실제:**
- **예상**: 업로드 주기가 짧을수록 (매일~2-3일) 조회수가 높을 것
- **실제**:
  - **패션**: 4-7일 주기가 최적 - 품질 vs 빈도의 균형점
  - **먹방**: 2-3일 주기가 최고 성과 - 높은 콘텐츠 소비 속도
  - **여행**: 6-7일 주기 우수 - 고퀄리티 콘텐츠 선호
  - 너무 잦은 업로드(1일)는 오히려 조회수 감소 - 구독자 피로도 증가
  - 31일 이상 장기 공백은 알고리즘 불이익과 구독자 이탈로 제외됨

**주요 인사이트:**
- IQR 방식으로 이상치 제거하여 신뢰도 높은 결과 도출
- 일관된 업로드 주기 유지가 알고리즘 추천에 긍정적
- 분야별 최적 주기가 명확히 다르며, 콘텐츠 제작 난이도와 연관
- 과다 업로드는 영상당 조회수 희석 효과

---

### 4. **Correlation Analysis - 상관관계 분석**
**조회수와 좋아요수 & 조회수와 댓글수의 상관관계**

**시각화:**
- **X축**: 조회수
- **Y축**: 좋아요수 / 댓글수
- **그래프 형식**: 산점도 (Scatter plot) + 회귀선

**예상 vs 실제:**
- **예상**: 조회수가 높을수록 좋아요수와 댓글수도 비례하여 증가할 것 (강한 양의 상관관계)
- **실제**:
  - **조회수 ↔ 좋아요수**: 매우 강한 양의 상관관계 (r = 0.85~0.92)
    - 예상대로 강한 선형 관계 확인
    - 패션 > 먹방 > 여행 순으로 상관계수 높음
  - **조회수 ↔ 댓글수**: 중간~강한 양의 상관관계 (r = 0.65~0.78)
    - 좋아요보다 낮은 상관관계 - 댓글은 보다 능동적 참여 필요
    - 먹방 카테고리에서 댓글 참여도가 상대적으로 높음 (맛 평가, 추천 등)
  - 채널 규모에 따라 상관관계 패턴 차이 존재

**주요 인사이트:**
- 좋아요는 수동적 참여로 조회수와 거의 비례 관계
- 댓글은 능동적 참여로 콘텐츠 품질과 더 큰 연관
- 먹방은 시청자 참여를 유도하는 콘텐츠 특성으로 댓글 비율 높음
- 이상치(바이럴 영상)는 일반적 패턴에서 벗어남

---

### 5. **Video Duration Analysis - 재생시간 분석**
**각 분야별 & 채널별 재생시간, 총 조회수 분포 파악으로 조회수 기준 상위 10개 하위 10개 재생시간 비교**

**시각화:**
- **X축**: 재생시간 (분)
- **Y축**: 조회수
- **그래프 형식**: 산점도 + 상위/하위 10개 평균 재생시간 비교 막대그래프

**예상 vs 실제:**
- **예상**: 영상이 길수록 시청자 피로도로 조회수가 낮아질 것
- **실제**:
  - **패션**: 8-12분이 최적 구간 - 충분한 정보 전달 + 집중력 유지
  - **먹방**: 10-15분 선호 - 식사 시간과 유사한 길이
  - **여행**: 이분화 패턴 - 짧은 하이라이트(5-8분) vs 긴 브이로그(15-25분)
  - 너무 짧은 영상(< 5분)도 조회수 낮음 - 콘텐츠 가치 부족
  - 20분 초과 시 급격한 조회수 감소 확인 - 시청 피로도 증가
  - **상위 10개 평균**: 8-12분 / **하위 10개 평균**: 3분 미만 또는 20분 초과

**주요 인사이트:**
- 분야별 최적 재생시간 존재 (Sweet Spot)
- 너무 짧거나 긴 영상 모두 불리
- 유튜브 알고리즘은 시청 지속 시간(Watch Time)을 중시하므로 적절한 길이 중요
- 쇼츠(< 60초)는 별도 분석 필요로 제외

---

### 6. **Channel Age Analysis - 채널 나이 분석**
**각 분야별 - 채널별 채널 개설일에 따른 총 구독자수 및 총 조회수 비교**

**시각화:**
- **X축**: 채널 연령 (년)
- **Y축**: 총 구독자수 / 총 조회수
- **그래프 형식**: 산점도 (Scatter plot)

**예상 vs 실제:**
- **예상**: 채널 개설일이 오래될수록 총 구독자수와 조회수가 높을 것
- **실제**:
  - **채널 나이 ≠ 성공**: 예상과 달리 명확한 양의 상관관계 없음
  - 오래된 채널(5년+) 중 휴면 상태인 경우 신규 채널보다 성과 낮음
  - 신규 채널(1-2년)이 일관된 업로드로 빠른 성장 사례 다수
  - **유튜브 알고리즘 변화**: 최근 콘텐츠를 선호하는 알고리즘 특성
  - **콘텐츠 품질 > 채널 연령**: 꾸준한 고품질 콘텐츠가 더 중요
  - 2-4년차 채널이 가장 높은 성장률 보임 (성숙기)

**주요 인사이트:**
- 채널 연령보다 최근 활동성과 콘텐츠 품질이 더 중요
- 오래된 채널도 리브랜딩과 꾸준한 업로드로 재성장 가능
- 유튜브 알고리즘은 "신선한" 콘텐츠를 선호
- 채널 나이보다 업로드 일관성이 구독자 유지에 핵심

---

### 7. **Expected Views Analysis - 기대조회수 분석**
**각 분야별 & 분야별 - 채널별 기대조회수 충족 여부 파악**

**시각화:**
- **X축**: 영상 번호 (최근 200개)
- **Y축**: 조회수 (실제 조회수 vs 기대 조회수 선)
- **그래프 형식**: 선 그래프 + 기준선

**예상 vs 실제:**
- **예상**: 대부분의 영상이 채널 평균(기대조회수) 근처에 분포할 것
- **실제**:
  - **성과 분포**: 20-80 법칙 적용 - 소수의 인기 영상이 전체 조회수의 대부분 차지
  - **상위 20%** 영상이 기대치의 200-500% 달성 (바이럴 영상)
  - **중간 60%** 영상이 기대치의 50-150% 범위
  - **하위 20%** 영상이 기대치의 50% 미만
  - 채널별로 일관성 차이 큼 - 일부는 안정적, 일부는 변동성 높음
  - 최근 200개 트렌드로 성장/하락 채널 구분 가능

**주요 인사이트:**
- 기대조회수 = (총 조회수 ÷ 총 영상 수)로 계산
- 일관된 성과를 내는 채널이 알고리즘에서 더 선호됨
- 바이럴 영상에 의존하는 채널은 지속 가능성 낮음
- 최근 성과 하락 시 콘텐츠 전략 재검토 필요

---

### 8. **Subscriber Ratio Analysis - 구독자 비율 분석**
**각 분야별 총 조회수 및 총 구독자수 비율 비교 및 분석**

**시각화:**
- **X축**: 구독자수
- **Y축**: 평균 조회수 / 조회수-구독자 비율
- **그래프 형식**: 산점도 + 비율 막대그래프

**예상 vs 실제:**
- **예상**: 구독자수가 많을수록 영상당 조회수도 비례하여 높을 것
- **실제**:
  - **구독자 효율성 차이**: 구독자 10만 vs 100만 채널의 조회수가 10배 차이 안 남
  - **고효율 채널**: 구독자 대비 5배 이상 조회수 (충성도 높은 팬층)
  - **저효율 채널**: 구독자 대비 2배 미만 조회수 (휴면 구독자 많음)
  - **먹방 카테고리**: 가장 높은 구독자 효율 (평균 6-8배) - 반복 시청 콘텐츠
  - **패션 카테고리**: 중간 효율 (평균 3-5배) - 트렌드 의존적
  - **여행 카테고리**: 변동성 큼 (2-6배) - 시즌 영향
  - 구독자 구매 채널은 낮은 효율로 즉시 구분 가능

**주요 인사이트:**
- 구독자 수보다 구독자 품질(참여도)이 더 중요
- 조회수/구독자 비율이 채널 건강도의 핵심 지표
- 알고리즘은 참여도 높은 채널을 더 추천
- 충성도 높은 소규모 커뮤니티가 수익화에 유리

---

## 📁 Project Structure

```
Youtube-Channel-Analysis-Project/
├── 📂 data/                              # Raw data files / 원본 데이터
│   ├── youtube_fashion_data.csv          # Fashion category data / 패션 카테고리 데이터
│   ├── youtube_mukbang_data.csv          # Mukbang category data / 먹방 카테고리 데이터
│   └── youtube_travel_data.csv           # Travel category data / 여행 카테고리 데이터
│
├── 📂 notebooks, visualizations/         # Jupyter notebooks / 주피터 노트북
│   ├── Youtube_Channel_Anaylsis_Project.ipynb     # Main analysis notebook / 메인 분석 노트북
│   └── Youtube_Channel_Anaylsis_Project_backup.ipynb  # Backup / 백업
│
├── 📂 analysis/                          # Individual analysis scripts / 개별 분석 스크립트
│   ├── data_preprocessing.py            # Data preprocessing / 데이터 전처리
│   ├── 01_wordcloud_analysis.py         # Word cloud analysis / 워드클라우드 분석
│   ├── 02_upload_timing_analysis.py     # Upload timing analysis / 업로드 타이밍 분석
│   ├── 03_upload_frequency_analysis.py  # Upload frequency analysis / 업로드 주기 분석
│   ├── 04_correlation_analysis.py       # Correlation analysis / 상관관계 분석
│   ├── 05_video_duration_analysis.py    # Video duration analysis / 재생시간 분석
│   ├── 06_channel_age_analysis.py       # Channel age analysis / 채널 나이 분석
│   ├── 07_expected_views_analysis.py    # Expected views analysis / 기대조회수 분석
│   └── 08_subscriber_ratio_analysis.py  # Subscriber ratio analysis / 구독자 비율 분석
│
├── 📄 README.md                          # Project documentation / 프로젝트 문서
├── 📄 requirements.txt                   # Python dependencies / 파이썬 패키지 목록
├── 📄 LICENSE                            # MIT License / MIT 라이선스
└── 📄 .gitignore                         # Git ignore rules / Git 무시 규칙
```

---

## 🛠 Technologies Used

### Core Data Science Stack
- **Python 3.8+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Jupyter Notebook**: Interactive analysis environment

### Visualization
- **Matplotlib**: Plotting and visualization with Korean font support (Malgun Gothic)
- **Seaborn**: Statistical data visualization
- **WordCloud**: Korean text visualization

### Text Processing
- **Korean Language Processing**: Morphological analysis for Korean text
- **Collections**: Word frequency analysis

---

## 📋 Requirements

```bash
pip install pandas matplotlib seaborn wordcloud numpy jupyter notebook
```

**Or install from requirements.txt:**
```bash
pip install -r requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Youtube-Channel-Analysis-Project.git
cd Youtube-Channel-Analysis-Project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Jupyter Notebook
```bash
jupyter notebook "notebooks, visualizations/Youtube_Channel_Anaylsis_Project.ipynb"
```

### 4. Execute cells in order
1. **Cell 1-2**: Common data preprocessing / 공통 데이터 전처리
2. **Cell 3-4**: Word cloud analysis / 워드클라우드 분석
3. **Cell 5-6**: Upload timing analysis / 업로드 타이밍 분석
4. **Cell 7-8**: Upload frequency analysis / 업로드 주기 분석
5. **Cell 9-10**: Correlation analysis / 상관관계 분석
6. **Cell 11-12**: Video duration analysis / 재생시간 분석
7. **Cell 13-14**: Channel age analysis / 채널 나이 분석
8. **Cell 15-17**: Expected views analysis / 기대조회수 분석
9. **Cell 18-19**: Subscriber ratio analysis / 구독자 비율 분석

---

## 📊 Key Findings

### 🎯 Content Strategy Recommendations

**For Fashion Channels (패션 채널):**
- Optimal upload: Weekday afternoons (2-6 PM) or weekend mornings
- Best frequency: 4-7 day intervals
- Ideal duration: 8-12 minutes
- Focus on consistent styling keywords

**For Mukbang Channels (먹방 채널):**
- Optimal upload: Meal times (12-1 PM, 6-8 PM), any day
- Best frequency: 2-3 day intervals
- Ideal duration: 10-15 minutes
- High comment engagement potential

**For Travel Channels (여행 채널):**
- Optimal upload: Sunday evenings (6-9 PM)
- Best frequency: 6-7 day intervals (weekly)
- Ideal duration: Flexible (5-8 min highlights or 15-25 min vlogs)
- Seasonal trends matter significantly

### 📈 Universal Success Factors
1. **Consistency** > Channel age: Regular uploads beat old inactive channels
2. **Engagement quality** > Subscriber count: Active small community beats passive large audience
3. **Optimal timing**: Category-specific upload times significantly impact views
4. **Content duration**: Sweet spot exists for each category
5. **Upload frequency**: More is not always better - find your category's optimal interval

---

## 🎯 Use Cases

### For Content Creators (콘텐츠 크리에이터)
- Optimize upload schedule based on category-specific data
- Determine ideal video length for your niche
- Benchmark performance against category averages
- Identify trending keywords for titles

### For Marketers (마케터)
- Select influencers based on engagement quality, not just subscriber count
- Understand optimal campaign timing per category
- Analyze audience engagement patterns
- ROI optimization through data-driven decisions

### For Data Scientists (데이터 과학자)
- Korean language processing techniques
- Social media analytics methodology
- Time series analysis on content platforms
- Correlation analysis in engagement metrics

---

## 🔮 Future Enhancements

- [ ] Real-time data integration via YouTube Data API v3
- [ ] Sentiment analysis on Korean comments
- [ ] Thumbnail effectiveness analysis using computer vision
- [ ] Machine learning models for view prediction
- [ ] Multi-platform comparison (Instagram, TikTok)
- [ ] Automated reporting dashboard

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

For questions or collaboration opportunities, please open an issue on GitHub.

---

**Made with ❤️ using Python and Korean language processing**

**한국 유튜브 채널 분석을 위한 데이터 사이언스 프로젝트**
