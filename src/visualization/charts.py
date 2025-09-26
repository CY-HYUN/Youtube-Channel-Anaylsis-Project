import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from wordcloud import WordCloud


class YouTubeVisualizer:
    """
    YouTube 데이터 시각화 클래스
    """

    def __init__(self, style: str = 'seaborn-v0_8', figsize: Tuple[int, int] = (12, 8)):
        """
        시각화 설정 초기화

        Args:
            style (str): matplotlib 스타일
            figsize (Tuple[int, int]): 기본 그래프 크기
        """
        plt.style.use(style)
        self.figsize = figsize
        self.colors = sns.color_palette("husl", 10)

    def plot_video_performance(self, videos_df: pd.DataFrame,
                               metric: str = 'views',
                               top_n: int = 15) -> plt.Figure:
        """
        상위 동영상 성과 시각화

        Args:
            videos_df (pd.DataFrame): 동영상 데이터
            metric (str): 성과 지표 ('views', 'likes', 'comments')
            top_n (int): 표시할 동영상 수

        Returns:
            plt.Figure: 생성된 그래프
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        # 지표 매핑
        metric_map = {
            'views': 'statistics.viewCount',
            'likes': 'statistics.likeCount',
            'comments': 'statistics.commentCount'
        }

        if metric not in metric_map:
            raise ValueError(f"지원되지 않는 지표: {metric}")

        column = metric_map[metric]
        top_videos = videos_df.nlargest(top_n, column)

        # 제목 길이 제한
        titles = [title[:50] + '...' if len(title) > 50 else title
                  for title in top_videos['snippet.title']]

        # 바 차트 생성
        bars = ax.barh(range(len(titles)), top_videos[column], color=self.colors[0])

        # 레이블 설정
        ax.set_yticks(range(len(titles)))
        ax.set_yticklabels(titles, fontsize=10)
        ax.set_xlabel(f'{metric.capitalize()} Count', fontsize=12)
        ax.set_title(f'Top {top_n} Videos by {metric.capitalize()}', fontsize=14, fontweight='bold')

        # 값 표시
        for i, (bar, value) in enumerate(zip(bars, top_videos[column])):
            ax.text(value, bar.get_y() + bar.get_height() / 2,
                    f'{value:,.0f}', ha='left', va='center', fontsize=9)

        plt.tight_layout()
        return fig

    def plot_upload_frequency(self, videos_df: pd.DataFrame) -> plt.Figure:
        """
        업로드 빈도 시각화

        Args:
            videos_df (pd.DataFrame): 동영상 데이터

        Returns:
            plt.Figure: 생성된 그래프
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figsize[0], self.figsize[1] * 1.2))

        # 날짜 데이터 전처리
        videos_df['published_date'] = pd.to_datetime(videos_df['snippet.publishedAt'])
        videos_df['year_month'] = videos_df['published_date'].dt.to_period('M')
        videos_df['weekday'] = videos_df['published_date'].dt.day_name()

        # 월별 업로드 수
        monthly_uploads = videos_df['year_month'].value_counts().sort_index()
        monthly_uploads.plot(kind='line', ax=ax1, color=self.colors[1], marker='o', linewidth=2)
        ax1.set_title('Monthly Upload Frequency', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Month', fontsize=12)
        ax1.set_ylabel('Number of Uploads', fontsize=12)
        ax1.grid(True, alpha=0.3)

        # 요일별 업로드 수
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_uploads = videos_df['weekday'].value_counts().reindex(weekday_order, fill_value=0)
        weekday_uploads.plot(kind='bar', ax=ax2, color=self.colors[2])
        ax2.set_title('Upload Frequency by Day of Week', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Day of Week', fontsize=12)
        ax2.set_ylabel('Number of Uploads', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        return fig

    def plot_engagement_analysis(self, videos_df: pd.DataFrame) -> plt.Figure:
        """
        참여도 분석 시각화

        Args:
            videos_df (pd.DataFrame): 동영상 데이터

        Returns:
            plt.Figure: 생성된 그래프
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

        # 참여율 계산
        videos_df['engagement_rate'] = (
                (videos_df['statistics.likeCount'] + videos_df['statistics.commentCount']) /
                videos_df['statistics.viewCount'] * 100
        )

        # 1. 조회수 vs 좋아요 수
        ax1.scatter(videos_df['statistics.viewCount'], videos_df['statistics.likeCount'],
                    alpha=0.6, color=self.colors[0])
        ax1.set_xlabel('View Count', fontsize=12)
        ax1.set_ylabel('Like Count', fontsize=12)
        ax1.set_title('Views vs Likes', fontsize=14, fontweight='bold')

        # 2. 조회수 vs 댓글 수
        ax2.scatter(videos_df['statistics.viewCount'], videos_df['statistics.commentCount'],
                    alpha=0.6, color=self.colors[1])
        ax2.set_xlabel('View Count', fontsize=12)
        ax2.set_ylabel('Comment Count', fontsize=12)
        ax2.set_title('Views vs Comments', fontsize=14, fontweight='bold')

        # 3. 참여율 분포
        ax3.hist(videos_df['engagement_rate'], bins=30, alpha=0.7, color=self.colors[2])
        ax3.set_xlabel('Engagement Rate (%)', fontsize=12)
        ax3.set_ylabel('Frequency', fontsize=12)
        ax3.set_title('Engagement Rate Distribution', fontsize=14, fontweight='bold')

        # 4. 시간별 참여율 변화
        videos_df['published_date'] = pd.to_datetime(videos_df['snippet.publishedAt'])
        monthly_engagement = videos_df.groupby(videos_df['published_date'].dt.to_period('M'))['engagement_rate'].mean()
        monthly_engagement.plot(ax=ax4, color=self.colors[3], marker='o', linewidth=2)
        ax4.set_title('Monthly Average Engagement Rate', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Month', fontsize=12)
        ax4.set_ylabel('Engagement Rate (%)', fontsize=12)
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_duration_analysis(self, videos_df: pd.DataFrame) -> plt.Figure:
        """
        동영상 길이 분석 시각화

        Args:
            videos_df (pd.DataFrame): 동영상 데이터

        Returns:
            plt.Figure: 생성된 그래프
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Duration을 초 단위로 변환하는 함수
        def parse_duration(duration_str):
            if pd.isna(duration_str):
                return 0
            import re
            pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
            match = pattern.match(duration_str)
            if not match:
                return 0
            hours = int(match.group(1)) if match.group(1) else 0
            minutes = int(match.group(2)) if match.group(2) else 0
            seconds = int(match.group(3)) if match.group(3) else 0
            return hours * 3600 + minutes * 60 + seconds

        # Duration 데이터 처리
        videos_df['duration_seconds'] = videos_df['contentDetails.duration'].apply(parse_duration)
        videos_df['duration_minutes'] = videos_df['duration_seconds'] / 60

        # 1. 동영상 길이 분포
        ax1.hist(videos_df['duration_minutes'], bins=30, alpha=0.7, color=self.colors[0])
        ax1.set_xlabel('Duration (minutes)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.set_title('Video Duration Distribution', fontsize=14, fontweight='bold')

        # 2. 길이별 평균 조회수
        videos_df['duration_category'] = pd.cut(
            videos_df['duration_minutes'],
            bins=[0, 5, 10, 20, 30, 60, float('inf')],
            labels=['0-5min', '5-10min', '10-20min', '20-30min', '30-60min', '60min+']
        )

        duration_performance = videos_df.groupby('duration_category')['statistics.viewCount'].mean()
        duration_performance.plot(kind='bar', ax=ax2, color=self.colors[1])
        ax2.set_title('Average Views by Duration Category', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Duration Category', fontsize=12)
        ax2.set_ylabel('Average Views', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        return fig

    def create_word_cloud(self, videos_df: pd.DataFrame, title_column: str = 'snippet.title') -> plt.Figure:
        """
        동영상 제목으로 워드클라우드 생성

        Args:
            videos_df (pd.DataFrame): 동영상 데이터
            title_column (str): 제목 컬럼명

        Returns:
            plt.Figure: 생성된 워드클라우드
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        # 모든 제목 합치기
        all_titles = ' '.join(videos_df[title_column].astype(str))

        # 워드클라우드 생성
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            max_words=100,
            colormap='Set3'
        ).generate(all_titles)

        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Most Common Words in Video Titles', fontsize=16, fontweight='bold', pad=20)

        plt.tight_layout()
        return fig

    def plot_performance_correlation(self, videos_df: pd.DataFrame) -> plt.Figure:
        """
        성과 지표 간 상관관계 분석

        Args:
            videos_df (pd.DataFrame): 동영상 데이터

        Returns:
            plt.Figure: 상관관계 히트맵
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        # 상관관계 분석할 컬럼
        correlation_columns = [
            'statistics.viewCount',
            'statistics.likeCount',
            'statistics.commentCount',
        ]

        # Duration 컬럼이 있다면 추가
        if 'contentDetails.duration' in videos_df.columns:
            def parse_duration(duration_str):
                if pd.isna(duration_str):
                    return 0
                import re
                pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
                match = pattern.match(duration_str)
                if not match:
                    return 0
                hours = int(match.group(1)) if match.group(1) else 0
                minutes = int(match.group(2)) if match.group(2) else 0
                seconds = int(match.group(3)) if match.group(3) else 0
                return hours * 3600 + minutes * 60 + seconds

            videos_df['duration_seconds'] = videos_df['contentDetails.duration'].apply(parse_duration)
            correlation_columns.append('duration_seconds')

        # 상관관계 계산
        correlation_data = videos_df[correlation_columns].corr()

        # 히트맵 생성
        sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0,
                    square=True, ax=ax, cbar_kws={'shrink': .8})

        ax.set_title('Performance Metrics Correlation', fontsize=16, fontweight='bold')

        plt.tight_layout()
        return fig

    def save_all_charts(self, videos_df: pd.DataFrame, output_dir: str = 'visualizations'):
        """
        모든 차트를 파일로 저장

        Args:
            videos_df (pd.DataFrame): 동영상 데이터
            output_dir (str): 출력 디렉토리
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        charts = [
            (self.plot_video_performance(videos_df), 'top_videos_performance.png'),
            (self.plot_upload_frequency(videos_df), 'upload_frequency.png'),
            (self.plot_engagement_analysis(videos_df), 'engagement_analysis.png'),
            (self.plot_duration_analysis(videos_df), 'duration_analysis.png'),
            (self.create_word_cloud(videos_df), 'title_wordcloud.png'),
            (self.plot_performance_correlation(videos_df), 'performance_correlation.png'),
        ]

        for fig, filename in charts:
            fig.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
            plt.close(fig)

        print(f"모든 차트가 {output_dir} 디렉토리에 저장되었습니다.")