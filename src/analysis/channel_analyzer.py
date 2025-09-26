import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
import re


class ChannelAnalyzer:
    """
    YouTube 채널 데이터 분석 클래스
    """

    def __init__(self, channel_data_path: str, videos_data_path: str):
        """
        데이터 파일 경로로 초기화

        Args:
            channel_data_path (str): 채널 정보 CSV 파일 경로
            videos_data_path (str): 동영상 데이터 CSV 파일 경로
        """
        self.channel_df = pd.read_csv(channel_data_path)
        self.videos_df = pd.read_csv(videos_data_path)
        self._preprocess_data()

    def _preprocess_data(self):
        """
        데이터 전처리
        """
        # 날짜 컬럼 변환
        if 'snippet.publishedAt' in self.videos_df.columns:
            self.videos_df['published_date'] = pd.to_datetime(self.videos_df['snippet.publishedAt'])

        # 통계 컬럼들을 숫자형으로 변환
        stat_columns = [
            'statistics.viewCount',
            'statistics.likeCount',
            'statistics.commentCount'
        ]

        for col in stat_columns:
            if col in self.videos_df.columns:
                self.videos_df[col] = pd.to_numeric(self.videos_df[col], errors='coerce').fillna(0)

        # 영상 길이 정보 처리
        if 'contentDetails.duration' in self.videos_df.columns:
            self.videos_df['duration_seconds'] = self.videos_df['contentDetails.duration'].apply(
                self._parse_duration
            )

    def _parse_duration(self, duration_str: str) -> int:
        """
        YouTube duration 형식(PT4M13S)을 초 단위로 변환

        Args:
            duration_str (str): YouTube duration 문자열

        Returns:
            int: 초 단위 duration
        """
        if pd.isna(duration_str):
            return 0

        # PT4M13S 형식 파싱
        pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
        match = pattern.match(duration_str)

        if not match:
            return 0

        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0

        return hours * 3600 + minutes * 60 + seconds

    def get_channel_summary(self) -> Dict:
        """
        채널 요약 통계

        Returns:
            Dict: 채널 요약 정보
        """
        if self.channel_df.empty:
            return {}

        channel_info = self.channel_df.iloc[0]

        summary = {
            'channel_name': channel_info.get('snippet.title', 'Unknown'),
            'subscriber_count': int(channel_info.get('statistics.subscriberCount', 0)),
            'total_videos': int(channel_info.get('statistics.videoCount', 0)),
            'total_views': int(channel_info.get('statistics.viewCount', 0)),
            'channel_created': channel_info.get('snippet.publishedAt', 'Unknown')
        }

        return summary

    def get_video_performance_stats(self) -> Dict:
        """
        동영상 성과 통계

        Returns:
            Dict: 동영상 성과 통계
        """
        if self.videos_df.empty:
            return {}

        stats = {
            'total_videos_analyzed': len(self.videos_df),
            'average_views': self.videos_df['statistics.viewCount'].mean(),
            'median_views': self.videos_df['statistics.viewCount'].median(),
            'max_views': self.videos_df['statistics.viewCount'].max(),
            'min_views': self.videos_df['statistics.viewCount'].min(),
            'average_likes': self.videos_df['statistics.likeCount'].mean(),
            'average_comments': self.videos_df['statistics.commentCount'].mean(),
        }

        # 참여율 계산
        stats['average_engagement_rate'] = (
                (self.videos_df['statistics.likeCount'] + self.videos_df['statistics.commentCount']) /
                self.videos_df['statistics.viewCount'] * 100
        ).mean()

        return stats

    def get_top_performing_videos(self, n: int = 10, metric: str = 'views') -> pd.DataFrame:
        """
        상위 성과 동영상 조회

        Args:
            n (int): 반환할 동영상 수
            metric (str): 정렬 기준 ('views', 'likes', 'comments', 'engagement')

        Returns:
            pd.DataFrame: 상위 성과 동영상
        """
        if self.videos_df.empty:
            return pd.DataFrame()

        if metric == 'views':
            sort_column = 'statistics.viewCount'
        elif metric == 'likes':
            sort_column = 'statistics.likeCount'
        elif metric == 'comments':
            sort_column = 'statistics.commentCount'
        elif metric == 'engagement':
            # 참여율 계산
            self.videos_df['engagement_rate'] = (
                    (self.videos_df['statistics.likeCount'] + self.videos_df['statistics.commentCount']) /
                    self.videos_df['statistics.viewCount'] * 100
            )
            sort_column = 'engagement_rate'

        top_videos = self.videos_df.nlargest(n, sort_column)

        # 필요한 컬럼만 선택
        columns = [
            'snippet.title',
            'statistics.viewCount',
            'statistics.likeCount',
            'statistics.commentCount',
            'published_date'
        ]

        return top_videos[columns]

    def get_upload_frequency_analysis(self) -> Dict:
        """
        업로드 빈도 분석

        Returns:
            Dict: 업로드 빈도 분석 결과
        """
        if self.videos_df.empty or 'published_date' not in self.videos_df.columns:
            return {}

        # 월별 업로드 수
        self.videos_df['year_month'] = self.videos_df['published_date'].dt.to_period('M')
        monthly_uploads = self.videos_df['year_month'].value_counts().sort_index()

        # 요일별 업로드 수
        self.videos_df['weekday'] = self.videos_df['published_date'].dt.day_name()
        weekday_uploads = self.videos_df['weekday'].value_counts()

        return {
            'monthly_uploads': monthly_uploads.to_dict(),
            'weekday_uploads': weekday_uploads.to_dict(),
            'average_monthly_uploads': monthly_uploads.mean(),
            'most_active_month': monthly_uploads.idxmax().strftime('%Y-%m'),
            'most_active_weekday': weekday_uploads.idxmax()
        }

    def get_content_duration_analysis(self) -> Dict:
        """
        콘텐츠 길이 분석

        Returns:
            Dict: 콘텐츠 길이 분석 결과
        """
        if 'duration_seconds' not in self.videos_df.columns:
            return {}

        duration_stats = {
            'average_duration_minutes': self.videos_df['duration_seconds'].mean() / 60,
            'median_duration_minutes': self.videos_df['duration_seconds'].median() / 60,
            'max_duration_minutes': self.videos_df['duration_seconds'].max() / 60,
            'min_duration_minutes': self.videos_df['duration_seconds'].min() / 60,
        }

        # 길이별 카테고리 분석
        self.videos_df['duration_category'] = pd.cut(
            self.videos_df['duration_seconds'] / 60,
            bins=[0, 5, 10, 20, 30, 60, float('inf')],
            labels=['Very Short (0-5min)', 'Short (5-10min)', 'Medium (10-20min)',
                    'Long (20-30min)', 'Very Long (30-60min)', 'Extra Long (60min+)']
        )

        category_performance = self.videos_df.groupby('duration_category').agg({
            'statistics.viewCount': 'mean',
            'statistics.likeCount': 'mean',
            'statistics.commentCount': 'mean'
        })

        duration_stats['category_performance'] = category_performance.to_dict()

        return duration_stats

    def generate_insights(self) -> List[str]:
        """
        분석 결과를 바탕으로 인사이트 생성

        Returns:
            List[str]: 인사이트 목록
        """
        insights = []

        # 성과 분석
        performance_stats = self.get_video_performance_stats()
        if performance_stats:
            avg_views = performance_stats['average_views']
            max_views = performance_stats['max_views']

            if max_views > avg_views * 3:
                insights.append(
                    f"최고 조회수 영상({max_views:,.0f})이 평균({avg_views:,.0f})보다 "
                    f"{max_views / avg_views:.1f}배 높아 바이럴 콘텐츠의 특성을 분석해볼 필요가 있습니다."
                )

        # 업로드 빈도 분석
        frequency_analysis = self.get_upload_frequency_analysis()
        if frequency_analysis:
            avg_monthly = frequency_analysis.get('average_monthly_uploads', 0)
            most_active_day = frequency_analysis.get('most_active_weekday', '')

            if avg_monthly > 8:
                insights.append("월 8회 이상의 높은 업로드 빈도를 유지하고 있어 활발한 채널입니다.")
            elif avg_monthly < 2:
                insights.append("업로드 빈도가 낮아 더 일정한 콘텐츠 제작이 필요할 수 있습니다.")

            if most_active_day:
                insights.append(f"{most_active_day}에 가장 많이 업로드하는 패턴을 보입니다.")

        # 참여율 분석
        if performance_stats.get('average_engagement_rate', 0) > 5:
            insights.append("평균 5% 이상의 높은 참여율을 보여 양질의 콘텐츠를 제작하고 있습니다.")

        return insights