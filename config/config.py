import os
from typing import Dict, List


class Config:
    """
    프로젝트 설정 관리 클래스
    """

    # API 설정
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

    # 데이터 경로 설정
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

    # 시각화 설정
    FIGURE_SIZE = (12, 8)
    DPI = 300
    STYLE = 'seaborn-v0_8'

    # 분석 설정
    TOP_N_VIDEOS = 20
    DATE_FORMAT = '%Y-%m-%d'

    # 채널 목록 (예시)
    SAMPLE_CHANNELS = {
        'tech': [
            'UCuTITJp_8VXjjthWdPdmwKA',  # 예시 채널 ID
        ],
        'entertainment': [
            # 엔터테인먼트 채널 ID들
        ],
        'education': [
            # 교육 채널 ID들
        ]
    }

    @classmethod
    def get_api_key(cls) -> str:
        """
        API 키 반환, 설정되지 않은 경우 에러 메시지 출력

        Returns:
            str: API 키
        """
        if not cls.YOUTUBE_API_KEY:
            raise ValueError(
                "YouTube API 키가 설정되지 않았습니다.\n"
                "환경변수 YOUTUBE_API_KEY를 설정하거나\n"
                "config/api_keys.py 파일을 생성하세요."
            )
        return cls.YOUTUBE_API_KEY

    @classmethod
    def create_directories(cls):
        """
        필요한 디렉토리들을 생성
        """
        directories = [
            cls.DATA_DIR,
            cls.RAW_DATA_DIR,
            cls.PROCESSED_DATA_DIR
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)


# API 키 파일 템플릿 생성 (실제 사용시 API 키 입력 필요)
API_KEYS_TEMPLATE = '''
# config/api_keys.py
# 실제 API 키를 입력하세요

YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"

# 환경변수로도 설정 가능:
# export YOUTUBE_API_KEY="your_api_key_here"
'''