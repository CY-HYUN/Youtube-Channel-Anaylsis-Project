"""
1. 워드클라우드 - 분야별 & 채널별
분야별 상위 5명의 유튜버들이 제목에 자주 사용하는 단어 분석
"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import os
from data_preprocessing import load_and_preprocess_data, get_top_channels_by_category, clean_korean_text, setup_matplotlib

def generate_wordcloud(text, title, ax, font_path=None, max_words=100):
    """
    워드클라우드를 생성합니다.

    Parameters:
    text (str): 워드클라우드에 사용할 텍스트
    title (str): 그래프 제목
    ax: matplotlib axes 객체
    font_path (str): 한글 폰트 경로
    max_words (int): 최대 단어 수
    """
    if not text.strip():
        ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center', fontsize=16)
        ax.set_title(title, fontsize=16, weight='bold')
        ax.axis('off')
        return

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        max_words=max_words,
        font_path=font_path,
        colormap='coolwarm',
        contour_color='black',
        contour_width=1
    ).generate(text)

    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title, fontsize=16, weight='bold')

def analyze_wordcloud_by_category(df, category, save_path="visualizations"):
    """
    특정 카테고리의 워드클라우드 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    category (str): 분석할 카테고리
    save_path (str): 저장할 경로
    """
    # 카테고리별 데이터 필터링
    category_df = df[df['카테고리'] == category].copy()

    if category_df.empty:
        print(f"No data found for category: {category}")
        return

    # 상위 5개 채널 가져오기
    top_channels = get_top_channels_by_category(df, category, top_n=5)

    if not top_channels:
        print(f"No channels found for category: {category}")
        return

    # 각 채널별 제목 결합
    channel_titles = {}
    for channel in top_channels:
        channel_df = category_df[category_df['채널명'] == channel]
        if '제목' in channel_df.columns:
            titles = ' '.join(channel_df['제목'].dropna().astype(str))
            # 한글만 추출
            korean_titles = clean_korean_text(titles)
            channel_titles[channel] = korean_titles

    # 전체 카테고리 제목 결합
    if '제목' in category_df.columns:
        all_titles = ' '.join(category_df['제목'].dropna().astype(str))
        all_korean_titles = clean_korean_text(all_titles)
    else:
        all_korean_titles = ""

    # 시각화
    num_channels = len(top_channels)
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()

    # 각 채널별 워드클라우드 생성
    for i, channel in enumerate(top_channels):
        if i < len(axes) - 1:  # 마지막 자리는 전체용으로 남겨둠
            generate_wordcloud(
                channel_titles.get(channel, ""),
                f'{channel} - {category} 워드클라우드',
                axes[i]
            )

    # 전체 카테고리 워드클라우드 생성
    generate_wordcloud(
        all_korean_titles,
        f'{category} 전체 워드클라우드',
        axes[-1]
    )

    # 빈 subplot 숨기기
    for i in range(num_channels, len(axes) - 1):
        axes[i].axis('off')

    plt.tight_layout()

    # 저장
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/01_wordcloud_{category}.png', dpi=300, bbox_inches='tight')
    plt.show()

    return channel_titles

def analyze_all_categories_wordcloud(df, save_path="visualizations"):
    """
    모든 카테고리의 워드클라우드 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    save_path (str): 저장할 경로
    """
    categories = df['카테고리'].unique()

    results = {}
    for category in categories:
        print(f"Processing wordcloud analysis for category: {category}")
        try:
            channel_titles = analyze_wordcloud_by_category(df, category, save_path)
            results[category] = channel_titles
        except Exception as e:
            print(f"Error processing {category}: {str(e)}")
            continue

    return results

def get_top_keywords_by_category(df, category, top_n=20):
    """
    카테고리별 상위 키워드를 추출합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    category (str): 카테고리명
    top_n (int): 상위 몇 개 키워드를 가져올지

    Returns:
    list: 상위 키워드 리스트
    """
    category_df = df[df['카테고리'] == category].copy()

    if category_df.empty or '제목' not in category_df.columns:
        return []

    # 모든 제목 결합
    all_titles = ' '.join(category_df['제목'].dropna().astype(str))
    clean_titles = clean_korean_text(all_titles)

    # 단어 분리 및 카운트
    words = clean_titles.split()
    # 한 글자 단어 제거
    words = [word for word in words if len(word) > 1]

    # 상위 키워드 추출
    word_counts = Counter(words)
    top_keywords = [word for word, count in word_counts.most_common(top_n)]

    return top_keywords

if __name__ == "__main__":
    # 실행 예시
    setup_matplotlib()

    # 데이터 로드
    df = load_and_preprocess_data()

    # 모든 카테고리 분석
    results = analyze_all_categories_wordcloud(df)

    # 카테고리별 상위 키워드 출력
    print("\n=== 카테고리별 상위 키워드 ===")
    for category in df['카테고리'].unique():
        keywords = get_top_keywords_by_category(df, category, top_n=10)
        print(f"\n{category}: {', '.join(keywords[:10])}")

    print("\n워드클라우드 분석이 완료되었습니다!")
    print("결과는 visualizations/ 폴더에 저장되었습니다.")