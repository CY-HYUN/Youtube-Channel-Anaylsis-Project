"""
3. 각 분야별 업로드 주기에 따른 평균 조회수 및 좋아요수 파악
가장 최적의 업로드 주기가 몇일인지 파악
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime, timedelta
from data_preprocessing import load_and_preprocess_data, filter_by_category, get_top_channels_by_category, setup_matplotlib, format_numbers
from matplotlib.ticker import FuncFormatter

def calculate_upload_frequency(df, channel_name):
    """
    특정 채널의 업로드 주기를 계산합니다.

    Parameters:
    df (pd.DataFrame): 채널 데이터프레임
    channel_name (str): 채널명

    Returns:
    dict: 업로드 주기 정보
    """
    channel_df = df[df['채널명'] == channel_name].copy()

    if channel_df.empty or '게시일' not in channel_df.columns:
        return {}

    # 날짜 순으로 정렬
    channel_df = channel_df.sort_values('게시일')

    # 업로드 간격 계산 (일 단위)
    upload_dates = channel_df['게시일'].dt.date
    intervals = []

    for i in range(1, len(upload_dates)):
        interval = (upload_dates.iloc[i] - upload_dates.iloc[i-1]).days
        if interval > 0:  # 같은 날 여러 업로드 제외
            intervals.append(interval)

    if not intervals:
        return {}

    avg_interval = np.mean(intervals)
    median_interval = np.median(intervals)

    # 주기별 성과 계산
    channel_df['업로드간격'] = [0] + intervals  # 첫 번째 영상은 0

    # 업로드 간격을 그룹으로 나누기 (1일, 2-3일, 4-7일, 8-14일, 15일+)
    def categorize_interval(interval):
        if interval <= 1:
            return '매일 (1일)'
        elif interval <= 3:
            return '2-3일'
        elif interval <= 7:
            return '주 1-2회 (4-7일)'
        elif interval <= 14:
            return '격주 (8-14일)'
        else:
            return '월 1-2회 (15일+)'

    channel_df['업로드주기구간'] = channel_df['업로드간격'].apply(categorize_interval)

    # 주기별 평균 성과
    frequency_performance = channel_df.groupby('업로드주기구간').agg({
        '조회수': 'mean',
        '좋아요 수': 'mean',
        '댓글 수': 'mean'
    }).round(0)

    return {
        'avg_interval': avg_interval,
        'median_interval': median_interval,
        'intervals': intervals,
        'frequency_performance': frequency_performance,
        'channel_data': channel_df
    }

def analyze_upload_frequency_by_category(df, category, save_path="visualizations"):
    """
    특정 카테고리의 업로드 주기 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    category (str): 분석할 카테고리
    save_path (str): 저장할 경로
    """
    category_df = filter_by_category(df, category)

    if category_df.empty:
        print(f"No data found for category: {category}")
        return

    # 상위 5개 채널 분석
    top_channels = get_top_channels_by_category(df, category, top_n=5)

    if not top_channels:
        print(f"No channels found for category: {category}")
        return

    # 각 채널별 업로드 주기 분석
    channel_results = {}
    for channel in top_channels:
        result = calculate_upload_frequency(category_df, channel)
        if result:
            channel_results[channel] = result

    if not channel_results:
        print(f"No valid upload frequency data for category: {category}")
        return

    # 시각화
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()

    # 1. 채널별 평균 업로드 주기
    ax1 = axes[0]
    channels = list(channel_results.keys())
    avg_intervals = [channel_results[ch]['avg_interval'] for ch in channels]

    bars1 = ax1.bar(range(len(channels)), avg_intervals, color='skyblue', alpha=0.7)
    ax1.set_title(f'{category} - 채널별 평균 업로드 주기', fontsize=14, weight='bold')
    ax1.set_xlabel('채널', fontsize=12)
    ax1.set_ylabel('평균 간격 (일)', fontsize=12)
    ax1.set_xticks(range(len(channels)))
    ax1.set_xticklabels([ch[:10] + '...' if len(ch) > 10 else ch for ch in channels], rotation=45)

    # 막대 위에 값 표시
    for bar, value in zip(bars1, avg_intervals):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{value:.1f}일', ha='center', va='bottom', fontsize=10)

    # 2. 업로드 주기별 평균 조회수 (전체 카테고리)
    ax2 = axes[1]
    all_frequency_data = []
    for channel, result in channel_results.items():
        if 'channel_data' in result:
            channel_data = result['channel_data'].copy()
            channel_data['채널명'] = channel
            all_frequency_data.append(channel_data)

    if all_frequency_data:
        combined_data = pd.concat(all_frequency_data, ignore_index=True)

        frequency_views = combined_data.groupby('업로드주기구간')['조회수'].mean().sort_values(ascending=False)

        bars2 = ax2.bar(range(len(frequency_views)), frequency_views.values, color='lightcoral', alpha=0.7)
        ax2.set_title(f'{category} - 업로드 주기별 평균 조회수', fontsize=14, weight='bold')
        ax2.set_xlabel('업로드 주기', fontsize=12)
        ax2.set_ylabel('평균 조회수', fontsize=12)
        ax2.set_xticks(range(len(frequency_views)))
        ax2.set_xticklabels(frequency_views.index, rotation=45)
        ax2.yaxis.set_major_formatter(FuncFormatter(format_numbers))

        # 막대 위에 값 표시
        for bar, value in zip(bars2, frequency_views.values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    format_numbers(value, None), ha='center', va='bottom', fontsize=10)

    # 3. 업로드 주기별 평균 좋아요 수
    ax3 = axes[2]
    if all_frequency_data:
        frequency_likes = combined_data.groupby('업로드주기구간')['좋아요 수'].mean().sort_values(ascending=False)

        bars3 = ax3.bar(range(len(frequency_likes)), frequency_likes.values, color='lightgreen', alpha=0.7)
        ax3.set_title(f'{category} - 업로드 주기별 평균 좋아요 수', fontsize=14, weight='bold')
        ax3.set_xlabel('업로드 주기', fontsize=12)
        ax3.set_ylabel('평균 좋아요 수', fontsize=12)
        ax3.set_xticks(range(len(frequency_likes)))
        ax3.set_xticklabels(frequency_likes.index, rotation=45)
        ax3.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 4. 채널별 업로드 간격 분포 (박스플롯)
    ax4 = axes[3]
    interval_data = []
    interval_labels = []
    for channel, result in channel_results.items():
        if 'intervals' in result and result['intervals']:
            interval_data.append(result['intervals'])
            interval_labels.append(channel[:10] + '...' if len(channel) > 10 else channel)

    if interval_data:
        ax4.boxplot(interval_data, labels=interval_labels)
        ax4.set_title(f'{category} - 채널별 업로드 간격 분포', fontsize=14, weight='bold')
        ax4.set_xlabel('채널', fontsize=12)
        ax4.set_ylabel('업로드 간격 (일)', fontsize=12)
        ax4.tick_params(axis='x', rotation=45)

    # 5. 업로드 주기와 조회수 상관관계 산점도
    ax5 = axes[4]
    if all_frequency_data:
        # 업로드간격을 숫자로 변환
        interval_mapping = {
            '매일 (1일)': 1,
            '2-3일': 2.5,
            '주 1-2회 (4-7일)': 5.5,
            '격주 (8-14일)': 11,
            '월 1-2회 (15일+)': 20
        }

        combined_data['업로드간격_숫자'] = combined_data['업로드주기구간'].map(interval_mapping)

        # 유효한 데이터만 필터링
        valid_data = combined_data.dropna(subset=['업로드간격_숫자', '조회수'])

        if not valid_data.empty:
            ax5.scatter(valid_data['업로드간격_숫자'], valid_data['조회수'], alpha=0.6, color='purple')
            ax5.set_title(f'{category} - 업로드 간격 vs 조회수', fontsize=14, weight='bold')
            ax5.set_xlabel('업로드 간격 (일)', fontsize=12)
            ax5.set_ylabel('조회수', fontsize=12)
            ax5.yaxis.set_major_formatter(FuncFormatter(format_numbers))

            # 추세선 추가
            if len(valid_data) > 1:
                z = np.polyfit(valid_data['업로드간격_숫자'], valid_data['조회수'], 1)
                p = np.poly1d(z)
                ax5.plot(valid_data['업로드간격_숫자'], p(valid_data['업로드간격_숫자']), "r--", alpha=0.8)

    # 6. 최적 업로드 주기 추천
    ax6 = axes[5]
    if all_frequency_data:
        # 조회수와 좋아요수를 종합한 성과 점수 계산
        frequency_performance = combined_data.groupby('업로드주기구간').agg({
            '조회수': 'mean',
            '좋아요 수': 'mean'
        })

        # 정규화 후 종합 점수 계산
        norm_views = frequency_performance['조회수'] / frequency_performance['조회수'].max()
        norm_likes = frequency_performance['좋아요 수'] / frequency_performance['좋아요 수'].max()
        frequency_performance['종합점수'] = (norm_views + norm_likes) / 2

        best_frequency = frequency_performance.sort_values('종합점수', ascending=False)

        bars6 = ax6.bar(range(len(best_frequency)), best_frequency['종합점수'].values,
                       color='gold', alpha=0.7)
        ax6.set_title(f'{category} - 업로드 주기별 종합 성과 점수', fontsize=14, weight='bold')
        ax6.set_xlabel('업로드 주기', fontsize=12)
        ax6.set_ylabel('종합 점수 (정규화)', fontsize=12)
        ax6.set_xticks(range(len(best_frequency)))
        ax6.set_xticklabels(best_frequency.index, rotation=45)

        # 최고 점수 강조
        max_idx = best_frequency['종합점수'].idxmax()
        max_pos = list(best_frequency.index).index(max_idx)
        bars6[max_pos].set_color('red')
        bars6[max_pos].set_alpha(1.0)

    plt.tight_layout()

    # 저장
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/03_upload_frequency_{category}.png', dpi=300, bbox_inches='tight')
    plt.show()

    return channel_results

def analyze_all_categories_upload_frequency(df, save_path="visualizations"):
    """
    모든 카테고리의 업로드 주기 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    save_path (str): 저장할 경로
    """
    categories = df['카테고리'].unique()
    results = {}

    # 각 카테고리별 분석
    for category in categories:
        print(f"Processing upload frequency analysis for category: {category}")
        try:
            category_results = analyze_upload_frequency_by_category(df, category, save_path)
            results[category] = category_results
        except Exception as e:
            print(f"Error processing {category}: {str(e)}")
            continue

    return results

if __name__ == "__main__":
    # 실행 예시
    setup_matplotlib()

    # 데이터 로드
    df = load_and_preprocess_data()

    # 전체 분석 실행
    results = analyze_all_categories_upload_frequency(df)

    # 결과 출력
    print("\n=== 카테고리별 평균 업로드 주기 ===")
    for category, category_results in results.items():
        if category_results:
            avg_intervals = [result['avg_interval'] for result in category_results.values() if 'avg_interval' in result]
            if avg_intervals:
                category_avg = np.mean(avg_intervals)
                print(f"{category}: 평균 {category_avg:.1f}일")

    print("\n업로드 주기 분석이 완료되었습니다!")
    print("결과는 visualizations/ 폴더에 저장되었습니다.")