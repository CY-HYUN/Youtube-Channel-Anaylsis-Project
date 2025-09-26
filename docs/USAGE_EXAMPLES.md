# 사용 예시 가이드

## 개요

이 문서는 YouTube Channel Analysis Project의 다양한 사용 방법과 실제 예시를 제공합니다.

## 빠른 시작

### 1. 환경 설정

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/Youtube-Channel-Analysis-Project.git
cd Youtube-Channel-Analysis-Project

# 2. 의존성 설치
pip install -r requirements.txt

# 3. API 키 설정
export YOUTUBE_API_KEY="your_youtube_api_key_here"
```

### 2. 기본 실행

```bash
# 모든 단계 실행 (데이터 수집 → 분석 → 시각화)
python main.py --mode all --channel-id UCuTITJp_8VXjjthWdPdmwKA

# 특정 단계만 실행
python main.py --mode collect --channel-id UCuTITJp_8VXjjthWdPdmwKA
python main.py --mode analyze
python main.py --mode visualize
```

## 상세 사용 방법

### 데이터 수집

#### 단일 채널 분석
```bash
python main.py --mode collect \
    --channel-id UCuTITJp_8VXjjthWdPdmwKA \
    --max-videos 100
```

#### 여러 채널 동시 분석
```bash
python main.py --mode collect \
    --channel-id UCuTITJp_8VXjjthWdPdmwKA \
    --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw \
    --channel-id UCEDXXCXj5UKKkVNTZUKLKtQ \
    --max-videos 50
```

#### 프로그래밍 방식 사용
```python
from src.data_collection.youtube_api import YouTubeDataCollector
from config.config import Config

# 데이터 수집기 초기화
api_key = Config.get_api_key()
collector = YouTubeDataCollector(api_key)

# 채널 데이터 수집
channel_id = "UCuTITJp_8VXjjthWdPdmwKA"
data = collector.collect_channel_data(channel_id, max_videos=100)

# CSV로 저장
collector.save_data_to_csv(data, "data/raw")
```

### 데이터 분석

#### 기본 분석
```python
from src.analysis.channel_analyzer import ChannelAnalyzer

# 분석기 초기화
analyzer = ChannelAnalyzer(
    "data/raw/Channel_Name_channel_info.csv",
    "data/raw/Channel_Name_videos.csv"
)

# 채널 요약 정보
summary = analyzer.get_channel_summary()
print(f"채널명: {summary['channel_name']}")
print(f"구독자 수: {summary['subscriber_count']:,}")
print(f"총 영상 수: {summary['total_videos']:,}")

# 성과 통계
performance = analyzer.get_video_performance_stats()
print(f"평균 조회수: {performance['average_views']:,.0f}")
print(f"평균 참여율: {performance['average_engagement_rate']:.2f}%")

# 상위 성과 영상
top_videos = analyzer.get_top_performing_videos(n=10, metric='views')
print("\\n=== 상위 조회수 영상 ===")
for idx, row in top_videos.iterrows():
    title = row['snippet.title'][:50] + "..." if len(row['snippet.title']) > 50 else row['snippet.title']
    views = row['statistics.viewCount']
    print(f"{title}: {views:,} views")
```

#### 고급 분석
```python
# 업로드 빈도 분석
frequency_analysis = analyzer.get_upload_frequency_analysis()
print(f"월평균 업로드: {frequency_analysis['average_monthly_uploads']:.1f}개")
print(f"가장 활발한 요일: {frequency_analysis['most_active_weekday']}")

# 콘텐츠 길이 분석
duration_analysis = analyzer.get_content_duration_analysis()
print(f"평균 영상 길이: {duration_analysis['average_duration_minutes']:.1f}분")

# AI 기반 인사이트
insights = analyzer.generate_insights()
for insight in insights:
    print(f"💡 {insight}")
```

### 데이터 시각화

#### 기본 시각화
```python
from src.visualization.charts import YouTubeVisualizer
import pandas as pd

# 시각화 도구 초기화
visualizer = YouTubeVisualizer()

# 데이터 로드
videos_df = pd.read_csv("data/raw/Channel_Name_videos.csv")

# 상위 성과 영상 차트
fig = visualizer.plot_video_performance(videos_df, metric='views', top_n=15)
fig.savefig('top_videos.png', dpi=300, bbox_inches='tight')

# 업로드 빈도 분석
fig = visualizer.plot_upload_frequency(videos_df)
fig.savefig('upload_frequency.png', dpi=300, bbox_inches='tight')

# 참여도 분석
fig = visualizer.plot_engagement_analysis(videos_df)
fig.savefig('engagement_analysis.png', dpi=300, bbox_inches='tight')
```

#### 모든 차트 한 번에 생성
```python
# 모든 시각화를 자동으로 생성하고 저장
visualizer.save_all_charts(videos_df, output_dir="visualizations/channel_name")
```

## 실제 분석 예시

### 예시 1: 기술 교육 채널 분석

```bash
# 1. 데이터 수집
python main.py --mode collect --channel-id UC_tech_channel_id --max-videos 200

# 2. 실행 결과 예시
```

**채널 요약:**
- 채널명: Tech Education Hub
- 구독자: 1,200,000명
- 총 영상: 500개
- 총 조회수: 50,000,000회

**성과 분석:**
- 평균 조회수: 100,000회
- 최고 조회수: 1,500,000회
- 평균 참여율: 6.8%
- 월평균 업로드: 12개

**주요 인사이트:**
- 💡 최고 조회수 영상이 평균보다 15배 높아 바이럴 콘텐츠 특성 분석 필요
- 💡 화요일에 가장 많이 업로드하는 패턴을 보입니다
- 💡 20-30분 길이의 영상이 가장 높은 평균 조회수를 기록

### 예시 2: 여러 채널 비교 분석

```python
# 여러 채널의 성과 비교
channels = [
    ("Tech Channel A", "UCxxxxxxxxxxxx"),
    ("Tech Channel B", "UCyyyyyyyyyyyy"),
    ("Tech Channel C", "UCzzzzzzzzzzzz")
]

comparison_data = []

for name, channel_id in channels:
    # 각 채널 데이터 수집 및 분석
    data = collector.collect_channel_data(channel_id)
    analyzer = ChannelAnalyzer(f"{name}_channel_info.csv", f"{name}_videos.csv")

    summary = analyzer.get_channel_summary()
    performance = analyzer.get_video_performance_stats()

    comparison_data.append({
        'channel': name,
        'subscribers': summary['subscriber_count'],
        'avg_views': performance['average_views'],
        'engagement_rate': performance['average_engagement_rate']
    })

# 비교 결과 출력
import pandas as pd
comparison_df = pd.DataFrame(comparison_data)
print(comparison_df)
```

### 예시 3: 시간별 트렌드 분석

```python
# 월별 성과 트렌드 분석
monthly_performance = videos_df.groupby(
    videos_df['published_date'].dt.to_period('M')
).agg({
    'statistics.viewCount': 'mean',
    'statistics.likeCount': 'mean',
    'statistics.commentCount': 'mean'
})

# 트렌드 시각화
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))
monthly_performance['statistics.viewCount'].plot(ax=ax, marker='o')
ax.set_title('Monthly Average Views Trend')
ax.set_ylabel('Average Views')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_trend.png', dpi=300)
```

## 자동화 스크립트 예시

### 일일 모니터링 스크립트

```python
#!/usr/bin/env python3
"""
daily_monitor.py - 일일 채널 모니터링 스크립트
"""

import schedule
import time
from datetime import datetime
from src.data_collection.youtube_api import YouTubeDataCollector
from src.analysis.channel_analyzer import ChannelAnalyzer

def daily_analysis():
    """일일 분석 실행"""
    print(f"[{datetime.now()}] 일일 분석 시작")

    # 모니터링할 채널 목록
    channels = ["UCuTITJp_8VXjjthWdPdmwKA", "UC_x5XG1OV2P6uZZ5FSM9Ttw"]

    for channel_id in channels:
        try:
            # 최신 데이터 수집 (최근 20개 영상만)
            collector = YouTubeDataCollector(api_key)
            data = collector.collect_channel_data(channel_id, max_videos=20)

            # 간단한 분석
            analyzer = ChannelAnalyzer(
                f"temp_{channel_id}_channel.csv",
                f"temp_{channel_id}_videos.csv"
            )

            summary = analyzer.get_channel_summary()
            performance = analyzer.get_video_performance_stats()

            print(f"채널: {summary['channel_name']}")
            print(f"최근 영상 평균 조회수: {performance['average_views']:,.0f}")

        except Exception as e:
            print(f"채널 {channel_id} 분석 실패: {e}")

# 매일 오전 9시에 실행
schedule.every().day.at("09:00").do(daily_analysis)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(3600)  # 1시간마다 확인
```

## 성능 최적화 팁

### 1. API 호출 최적화
```python
# 배치 처리로 API 호출 최소화
video_ids = [video['id'] for video in video_list]
batch_size = 50  # API 최대 허용량

for i in range(0, len(video_ids), batch_size):
    batch = video_ids[i:i+batch_size]
    video_details = collector.get_video_details(batch)
    time.sleep(0.1)  # API 호출 제한 방지
```

### 2. 데이터 캐싱
```python
import pickle
from pathlib import Path

# 데이터 캐시 저장
def save_cache(data, filename):
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)

    with open(cache_dir / filename, 'wb') as f:
        pickle.dump(data, f)

# 캐시 로드
def load_cache(filename):
    cache_path = Path("cache") / filename
    if cache_path.exists():
        with open(cache_path, 'rb') as f:
            return pickle.load(f)
    return None
```

### 3. 대용량 데이터 처리
```python
# 청크 단위로 데이터 처리
chunk_size = 1000
for chunk in pd.read_csv("large_video_data.csv", chunksize=chunk_size):
    # 각 청크에 대해 분석 수행
    result = analyze_chunk(chunk)
    save_chunk_result(result)
```

## 문제 해결 가이드

### 일반적인 오류와 해결책

**1. API 키 관련 오류**
```
ValueError: YouTube API 키가 설정되지 않았습니다.
```
**해결책:**
- 환경변수 `YOUTUBE_API_KEY` 설정 확인
- API 키가 올바른지 Google Cloud Console에서 확인

**2. 할당량 초과 오류**
```
403 Forbidden: Quota exceeded
```
**해결책:**
- 다음날까지 대기하거나 할당량 증액 요청
- API 호출 최적화로 사용량 줄이기

**3. 데이터 파일 없음**
```
FileNotFoundError: [Errno 2] No such file or directory
```
**해결책:**
- 데이터 수집 단계가 완료되었는지 확인
- 파일 경로가 올바른지 확인

### 디버깅 모드 사용

```python
import logging

# 디버그 로그 활성화
logging.basicConfig(level=logging.DEBUG)

# 또는 메인 스크립트에서
python main.py --mode all --channel-id UCxxxx --debug
```

## 추가 자료

- [YouTube Data API v3 문서](https://developers.google.com/youtube/v3)
- [pandas 공식 문서](https://pandas.pydata.org/docs/)
- [matplotlib 튜토리얼](https://matplotlib.org/tutorials/)
- [seaborn 갤러리](https://seaborn.pydata.org/examples/)