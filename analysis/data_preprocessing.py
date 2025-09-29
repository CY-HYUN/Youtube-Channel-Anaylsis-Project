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

def load_and_preprocess_data(data_dir="data"):
    """
    모든 CSV 파일을 읽고 하나의 DataFrame으로 결합하며 전처리를 수행합니다.

    Parameters:
    data_dir (str): 데이터 파일이 있는 디렉토리 경로

    Returns:
    pd.DataFrame: 전처리된 통합 데이터프레임
    """

    # CSV 파일들을 읽고 하나의 DataFrame으로 결합
    all_dataframes = []

    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(data_dir, filename)
            df = pd.read_csv(file_path)

            # 파일 경로 정보 추가 (카테고리 정보)
            df['카테고리'] = filename.replace('.csv', '')
            df['파일경로'] = file_path

            all_dataframes.append(df)

    # 모든 데이터프레임을 하나로 결합
    combined_df = pd.concat(all_dataframes, ignore_index=True)

    return preprocess_dataframe(combined_df)

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