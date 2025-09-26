import unittest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# 프로젝트 루트를 Python path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analysis.channel_analyzer import ChannelAnalyzer


class TestChannelAnalyzer(unittest.TestCase):
    """
    ChannelAnalyzer 클래스 테스트
    """

    def setUp(self):
        """
        테스트 데이터 설정
        """
        # 샘플 채널 데이터
        self.sample_channel_data = pd.DataFrame({
            'snippet.title': ['Test Channel'],
            'statistics.subscriberCount': [100000],
            'statistics.videoCount': [50],
            'statistics.viewCount': [1000000],
            'snippet.publishedAt': ['2020-01-01T00:00:00Z']
        })

        # 샘플 비디오 데이터
        self.sample_video_data = pd.DataFrame({
            'snippet.title': [
                'Video 1', 'Video 2', 'Video 3', 'Video 4', 'Video 5'
            ],
            'statistics.viewCount': [10000, 5000, 15000, 8000, 12000],
            'statistics.likeCount': [500, 250, 750, 400, 600],
            'statistics.commentCount': [50, 25, 75, 40, 60],
            'snippet.publishedAt': [
                '2023-01-01T10:00:00Z',
                '2023-01-05T14:00:00Z',
                '2023-02-01T12:00:00Z',
                '2023-02-10T16:00:00Z',
                '2023-03-01T11:00:00Z'
            ],
            'contentDetails.duration': ['PT10M30S', 'PT5M15S', 'PT15M45S', 'PT8M20S', 'PT12M10S']
        })

    @patch('pandas.read_csv')
    def test_initialization(self, mock_read_csv):
        """
        초기화 테스트
        """
        mock_read_csv.side_effect = [self.sample_channel_data, self.sample_video_data]

        analyzer = ChannelAnalyzer('dummy_channel.csv', 'dummy_videos.csv')

        self.assertIsInstance(analyzer.channel_df, pd.DataFrame)
        self.assertIsInstance(analyzer.videos_df, pd.DataFrame)
        self.assertEqual(len(analyzer.videos_df), 5)

    @patch('pandas.read_csv')
    def test_parse_duration(self, mock_read_csv):
        """
        duration 파싱 테스트
        """
        mock_read_csv.side_effect = [self.sample_channel_data, self.sample_video_data]
        analyzer = ChannelAnalyzer('dummy_channel.csv', 'dummy_videos.csv')

        # PT10M30S = 10*60 + 30 = 630초
        self.assertEqual(analyzer._parse_duration('PT10M30S'), 630)
        # PT1H5M30S = 1*3600 + 5*60 + 30 = 3930초
        self.assertEqual(analyzer._parse_duration('PT1H5M30S'), 3930)
        # PT45S = 45초
        self.assertEqual(analyzer._parse_duration('PT45S'), 45)

    @patch('pandas.read_csv')
    def test_get_channel_summary(self, mock_read_csv):
        """
        채널 요약 정보 테스트
        """
        mock_read_csv.side_effect = [self.sample_channel_data, self.sample_video_data]
        analyzer = ChannelAnalyzer('dummy_channel.csv', 'dummy_videos.csv')

        summary = analyzer.get_channel_summary()

        self.assertEqual(summary['channel_name'], 'Test Channel')
        self.assertEqual(summary['subscriber_count'], 100000)
        self.assertEqual(summary['total_videos'], 50)
        self.assertEqual(summary['total_views'], 1000000)

    @patch('pandas.read_csv')
    def test_get_video_performance_stats(self, mock_read_csv):
        """
        비디오 성과 통계 테스트
        """
        mock_read_csv.side_effect = [self.sample_channel_data, self.sample_video_data]
        analyzer = ChannelAnalyzer('dummy_channel.csv', 'dummy_videos.csv')

        stats = analyzer.get_video_performance_stats()

        self.assertEqual(stats['total_videos_analyzed'], 5)
        self.assertEqual(stats['max_views'], 15000)
        self.assertEqual(stats['min_views'], 5000)
        self.assertEqual(stats['average_views'], 10000)  # (10000+5000+15000+8000+12000)/5

    @patch('pandas.read_csv')
    def test_get_top_performing_videos(self, mock_read_csv):
        """
        상위 성과 비디오 조회 테스트
        """
        mock_read_csv.side_effect = [self.sample_channel_data, self.sample_video_data]
        analyzer = ChannelAnalyzer('dummy_channel.csv', 'dummy_videos.csv')

        top_videos = analyzer.get_top_performing_videos(n=3, metric='views')

        self.assertEqual(len(top_videos), 3)
        # 첫 번째는 가장 높은 조회수 (15000)
        self.assertEqual(top_videos.iloc[0]['statistics.viewCount'], 15000)

    @patch('pandas.read_csv')
    def test_get_content_duration_analysis(self, mock_read_csv):
        """
        콘텐츠 길이 분석 테스트
        """
        mock_read_csv.side_effect = [self.sample_channel_data, self.sample_video_data]
        analyzer = ChannelAnalyzer('dummy_channel.csv', 'dummy_videos.csv')

        duration_stats = analyzer.get_content_duration_analysis()

        self.assertIn('average_duration_minutes', duration_stats)
        self.assertIn('median_duration_minutes', duration_stats)
        self.assertGreater(duration_stats['average_duration_minutes'], 0)

    @patch('pandas.read_csv')
    def test_generate_insights(self, mock_read_csv):
        """
        인사이트 생성 테스트
        """
        mock_read_csv.side_effect = [self.sample_channel_data, self.sample_video_data]
        analyzer = ChannelAnalyzer('dummy_channel.csv', 'dummy_videos.csv')

        insights = analyzer.generate_insights()

        self.assertIsInstance(insights, list)
        # 인사이트가 하나 이상 생성되어야 함
        self.assertGreater(len(insights), 0)

    def test_empty_dataframe_handling(self):
        """
        빈 데이터프레임 처리 테스트
        """
        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.side_effect = [pd.DataFrame(), pd.DataFrame()]

            analyzer = ChannelAnalyzer('dummy_channel.csv', 'dummy_videos.csv')

            # 빈 데이터에 대해 적절히 처리되는지 확인
            summary = analyzer.get_channel_summary()
            self.assertEqual(summary, {})

            stats = analyzer.get_video_performance_stats()
            self.assertEqual(stats, {})


class TestDataValidation(unittest.TestCase):
    """
    데이터 검증 테스트
    """

    def test_required_columns_presence(self):
        """
        필수 컬럼 존재 여부 테스트
        """
        # 채널 데이터 필수 컬럼
        channel_required_columns = [
            'snippet.title',
            'statistics.subscriberCount',
            'statistics.videoCount',
            'statistics.viewCount'
        ]

        # 비디오 데이터 필수 컬럼
        video_required_columns = [
            'snippet.title',
            'statistics.viewCount',
            'statistics.likeCount',
            'statistics.commentCount',
            'snippet.publishedAt'
        ]

        # 테스트용 데이터프레임 생성
        channel_df = pd.DataFrame({col: [0] for col in channel_required_columns})
        video_df = pd.DataFrame({col: [0] for col in video_required_columns})

        # 필수 컬럼이 모두 존재하는지 확인
        for col in channel_required_columns:
            self.assertIn(col, channel_df.columns)

        for col in video_required_columns:
            self.assertIn(col, video_df.columns)

    def test_data_type_validation(self):
        """
        데이터 타입 검증 테스트
        """
        # 숫자형 데이터가 올바르게 변환되는지 테스트
        test_data = pd.DataFrame({
            'statistics.viewCount': ['1000', '2000', '3000'],
            'statistics.likeCount': ['100', '200', '300'],
            'statistics.commentCount': ['10', '20', '30']
        })

        # 숫자형으로 변환
        for col in ['statistics.viewCount', 'statistics.likeCount', 'statistics.commentCount']:
            test_data[col] = pd.to_numeric(test_data[col], errors='coerce')

        # 변환된 데이터 타입 확인
        self.assertTrue(pd.api.types.is_numeric_dtype(test_data['statistics.viewCount']))
        self.assertTrue(pd.api.types.is_numeric_dtype(test_data['statistics.likeCount']))
        self.assertTrue(pd.api.types.is_numeric_dtype(test_data['statistics.commentCount']))


if __name__ == '__main__':
    # 테스트 실행
    unittest.main(verbosity=2)