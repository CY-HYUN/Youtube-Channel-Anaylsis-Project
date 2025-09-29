"""
YouTube Channel Analysis - Data Preprocessing
공통적인 데이터 전처리 함수들을 포함합니다.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def load_and_preprocess_data(use_api=False, api_key=None, data_dir="data"):
    """
    데이터를 로드하고 전처리를 수행합니다.
    API 모드일 때는 YouTube Data API를 사용하고, 그렇지 않으면 샘플 데이터를 생성합니다.

    Parameters:
    use_api (bool): YouTube API 사용 여부
    api_key (str): YouTube Data API 키
    data_dir (str): 로컬 데이터 파일 디렉토리 (사용되지 않음, 호환성 위해 유지)

    Returns:
    pd.DataFrame: 전처리된 통합 데이터프레임
    """

    if use_api and api_key:
        print("Loading data from YouTube API...")
        try:
            combined_df = load_from_youtube_api(api_key)
        except Exception as e:
            print(f"API 로딩 실패: {e}")
            print("샘플 데이터를 대신 사용합니다...")
            combined_df = generate_sample_data()
    else:
        print("Using sample data for demonstration...")
        combined_df = generate_sample_data()

    return preprocess_dataframe(combined_df)

def generate_sample_data():
    """
    데모용 샘플 데이터를 생성합니다.
    """
    import random
    from datetime import datetime, timedelta

    # 카테고리 및 채널 정보
    categories = {
        'Gaming': ['GameChannel A', 'GameChannel B', 'GameChannel C', 'GameChannel D', 'GameChannel E'],
        'Food': ['FoodChannel A', 'FoodChannel B', 'FoodChannel C', 'FoodChannel D', 'FoodChannel E'],
        'KPOP': ['KPOPChannel A', 'KPOPChannel B', 'KPOPChannel C', 'KPOPChannel D', 'KPOPChannel E'],
        'Kids': ['KidsChannel A', 'KidsChannel B', 'KidsChannel C', 'KidsChannel D', 'KidsChannel E'],
        'Science': ['ScienceChannel A', 'ScienceChannel B', 'ScienceChannel C', 'ScienceChannel D', 'ScienceChannel E'],
        'Variety': ['VarietyChannel A', 'VarietyChannel B', 'VarietyChannel C', 'VarietyChannel D', 'VarietyChannel E']
    }

    sample_titles = {
        'Gaming': ['게임 리뷰', '신작 게임', '게임 공략', '라이브 플레이', '게임 추천'],
        'Food': ['맛집 탐방', '요리 레시피', '먹방', '음식 리뷰', '디저트 만들기'],
        'KPOP': ['뮤직비디오', '댄스 커버', '아이돌 리액션', '콘서트 후기', '신곡 소개'],
        'Kids': ['교육 만화', '장난감 리뷰', '동요', '학습 영상', '놀이 시간'],
        'Science': ['과학 실험', '기술 리뷰', '우주 탐험', '발명품 소개', 'IT 뉴스'],
        'Variety': ['예능 리뷰', '토크쇼', '코미디', '버라이어티', '웃긴 영상']
    }

    # 샘플 데이터 생성
    data = []
    np.random.seed(42)
    random.seed(42)

    for category, channels in categories.items():
        for channel in channels:
            for i in range(100):  # 각 채널당 100개 영상
                # 기본 정보
                base_subscribers = np.random.lognormal(12, 1.5)  # 구독자수
                base_views = np.random.lognormal(10, 2)  # 조회수

                # 게시일 생성 (최근 2년)
                days_ago = np.random.randint(1, 730)
                upload_date = datetime.now() - timedelta(days=days_ago)

                data.append({
                    '카테고리': category,
                    '채널명': channel,
                    '제목': f"{random.choice(sample_titles[category])} {i+1}",
                    '조회수': int(base_views),
                    '좋아요 수': int(base_views * np.random.uniform(0.02, 0.08)),
                    '댓글 수': int(base_views * np.random.uniform(0.005, 0.02)),
                    '구독자수': int(base_subscribers),
                    '재생시간': f"{np.random.randint(5, 60)}:{np.random.randint(0, 59):02d}",
                    '게시일': upload_date.strftime('%Y-%m-%d'),
                    '게시시간': f"{np.random.randint(0, 24):02d}:{np.random.randint(0, 60):02d}",
                    '채널 개설일': (datetime.now() - timedelta(days=np.random.randint(365, 3650))).strftime('%Y-%m-%d')
                })

    return pd.DataFrame(data)

def load_from_youtube_api(api_key):
    """
    YouTube Data API를 사용하여 실제 데이터를 로드합니다.

    Parameters:
    api_key (str): YouTube Data API 키

    Returns:
    pd.DataFrame: API에서 가져온 데이터프레임
    """
    try:
        from googleapiclient.discovery import build

        # YouTube API 클라이언트 생성
        youtube = build('youtube', 'v3', developerKey=api_key)

        # 여기에 실제 API 호출 로직을 구현
        # 예시: 인기 채널들의 영상 정보를 가져오는 코드

        print("YouTube API를 통한 실제 데이터 로딩 기능은 구현 중입니다.")
        print("현재는 샘플 데이터를 반환합니다.")

        # 실제 구현에서는 API 호출 결과를 반환
        return generate_sample_data()

    except ImportError:
        print("google-api-python-client가 설치되지 않았습니다.")
        print("pip install google-api-python-client 로 설치해주세요.")
        return generate_sample_data()
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")
        return generate_sample_data()

def preprocess_dataframe(df):
    """
    DataFrame에 대한 전처리를 수행합니다.

    Parameters:
    df (pd.DataFrame): 원본 데이터프레임

    Returns:
    pd.DataFrame: 전처리된 데이터프레임
    """

    # 데이터프레임 복사
    df = df.copy()

    # 날짜 형식을 datetime으로 변환
    if '게시일' in df.columns:
        df['게시일'] = pd.to_datetime(df['게시일'], errors='coerce')

        # 요일과 시간대 추출
        df['요일'] = df['게시일'].dt.day_name()
        df['시간대'] = df['게시일'].dt.hour

    # 수치형 컬럼들에서 쉼표 제거 및 숫자로 변환
    numeric_columns = ['조회수', '좋아요 수', '댓글 수']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # '영상 수' 컬럼이 존재하는지 확인 후 변환
    if '영상 수' in df.columns:
        df['영상 수'] = df['영상 수'].astype(str).str.replace(',', '', regex=False)
        df['영상 수'] = pd.to_numeric(df['영상 수'], errors='coerce').fillna(0).astype(int)

    # 요일 순서 설정
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # '요일' 컬럼을 카테고리로 변환, '미정' 추가 및 결측값 처리
    if '요일' in df.columns:
        df['요일'] = pd.Categorical(df['요일'], categories=day_order, ordered=True)
        df['요일'] = df['요일'].cat.add_categories('미정').fillna('미정')

        # '미정' 값을 가진 행 제거
        df = df[df['요일'] != '미정']

    # 나머지 결측값을 0으로 채움 (카테고리 컬럼 제외)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # 쇼츠 영상 제거 (비디오 길이가 60초 이하인 비디오 제외)
    if '재생 시간(분)' in df.columns:
        df = df[df['재생 시간(분)'] > 1]  # 1분 이하 제거

    return df

def filter_by_category(df, category):
    """
    특정 카테고리로 데이터를 필터링합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    category (str): 필터링할 카테고리명

    Returns:
    pd.DataFrame: 필터링된 데이터프레임
    """
    return df[df['카테고리'] == category].copy()

def get_top_channels_by_category(df, category, top_n=5, metric='조회수'):
    """
    특정 카테고리에서 상위 N개 채널을 반환합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    category (str): 카테고리명
    top_n (int): 상위 몇 개 채널을 가져올지
    metric (str): 정렬 기준 컬럼명

    Returns:
    list: 상위 채널명 리스트
    """
    category_df = filter_by_category(df, category)

    if '채널명' in category_df.columns:
        top_channels = (category_df.groupby('채널명')[metric]
                       .mean()
                       .sort_values(ascending=False)
                       .head(top_n)
                       .index.tolist())
        return top_channels
    else:
        return []

def clean_korean_text(text):
    """
    한글 텍스트 전처리를 수행합니다.

    Parameters:
    text (str): 원본 텍스트

    Returns:
    str: 전처리된 텍스트
    """
    import re

    if pd.isna(text):
        return ""

    # 한글만 추출 (숫자, 특수문자 제거)
    korean_text = re.sub(r'[^가-힣\s]', ' ', str(text))

    # 연속된 공백을 하나로 통합
    korean_text = re.sub(r'\s+', ' ', korean_text)

    # 앞뒤 공백 제거
    return korean_text.strip()

def format_numbers(x, pos):
    """
    숫자를 K, M 단위로 포맷팅합니다.
    """
    if x >= 1e6:
        return f'{x/1e6:.1f}M'
    elif x >= 1e3:
        return f'{x/1e3:.1f}K'
    else:
        return f'{x:.0f}'

def setup_matplotlib():
    """
    Matplotlib 한글 설정을 수행합니다.
    """
    # 그래프 설정
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.unicode_minus'] = False

    # 한글 폰트 설정 (시스템에 따라 다를 수 있음)
    try:
        plt.rcParams['font.family'] = 'Malgun Gothic'
    except:
        try:
            plt.rcParams['font.family'] = 'AppleGothic'
        except:
            plt.rcParams['font.family'] = 'DejaVu Sans'

# 카테고리 한국어 매핑
CATEGORY_MAPPING = {
    'gaming': '게임',
    'cooking': '요리',
    'kpop': 'K-POP',
    'kids': '키즈',
    'science': '과학',
    'entertainment': '엔터테인먼트',
    'fashion': '패션',
    'travel': '여행'
}

def get_korean_category_name(category):
    """
    영어 카테고리명을 한국어로 변환합니다.
    """
    return CATEGORY_MAPPING.get(category.lower(), category)

if __name__ == "__main__":
    # 테스트 실행
    setup_matplotlib()
    df = load_and_preprocess_data()
    print(f"Total records: {len(df)}")
    print(f"Categories: {df['카테고리'].unique()}")
    print(f"Columns: {df.columns.tolist()}")