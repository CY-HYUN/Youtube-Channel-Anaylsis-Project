"""
8. 각 분야별 총 조회수 및 총 구독자수 비율 비교 및 분석
구독자 대비 조회수 효율성 분석 및 채널별 성과 비교
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from data_preprocessing import load_and_preprocess_data, filter_by_category, get_top_channels_by_category, setup_matplotlib, format_numbers
from matplotlib.ticker import FuncFormatter

def calculate_subscriber_metrics(df, channel_name):
    """
    특정 채널의 구독자 관련 지표를 계산합니다.

    Parameters:
    df (pd.DataFrame): 채널 데이터프레임
    channel_name (str): 채널명

    Returns:
    dict: 구독자 관련 지표
    """
    channel_df = df[df['채널명'] == channel_name].copy()

    if channel_df.empty:
        return {}

    # 총 구독자수와 총 조회수
    total_subscribers = channel_df['구독자수'].iloc[0] if '구독자수' in channel_df.columns else 0
    total_views = channel_df['조회수'].sum()
    video_count = len(channel_df)

    # 구독자 당 조회수 (Views per Subscriber)
    views_per_subscriber = total_views / total_subscribers if total_subscribers > 0 else 0

    # 구독자 당 영상 수
    videos_per_subscriber = video_count / total_subscribers if total_subscribers > 0 else 0

    # 평균 영상 조회수
    avg_views_per_video = total_views / video_count if video_count > 0 else 0

    # 구독자 대비 평균 조회수 비율
    subscriber_engagement = avg_views_per_video / total_subscribers if total_subscribers > 0 else 0

    # 채널 성과 등급 (구독자 대비 조회수 효율성)
    if views_per_subscriber >= 10:
        performance_grade = "매우 높음"
    elif views_per_subscriber >= 5:
        performance_grade = "높음"
    elif views_per_subscriber >= 2:
        performance_grade = "보통"
    elif views_per_subscriber >= 1:
        performance_grade = "낮음"
    else:
        performance_grade = "매우 낮음"

    return {
        'total_subscribers': total_subscribers,
        'total_views': total_views,
        'video_count': video_count,
        'views_per_subscriber': views_per_subscriber,
        'videos_per_subscriber': videos_per_subscriber,
        'avg_views_per_video': avg_views_per_video,
        'subscriber_engagement': subscriber_engagement,
        'performance_grade': performance_grade
    }

def analyze_subscriber_ratio_by_category(df, category, save_path="visualizations"):
    """
    특정 카테고리의 구독자 비율 분석을 수행합니다.

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

    # 각 채널별 구독자 지표 분석
    channel_metrics = {}
    for channel in top_channels:
        metrics = calculate_subscriber_metrics(category_df, channel)
        if metrics:
            channel_metrics[channel] = metrics

    if not channel_metrics:
        print(f"No valid subscriber data for category: {category}")
        return

    # 시각화
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()

    # 1. 채널별 총 구독자수
    ax1 = axes[0]
    channels = list(channel_metrics.keys())
    subscribers = [channel_metrics[ch]['total_subscribers'] for ch in channels]

    bars1 = ax1.bar(range(len(channels)), subscribers, color='skyblue', alpha=0.7)
    ax1.set_title(f'{category} - 채널별 총 구독자수', fontsize=14, weight='bold')
    ax1.set_xlabel('채널', fontsize=12)
    ax1.set_ylabel('구독자수', fontsize=12)
    ax1.set_xticks(range(len(channels)))
    ax1.set_xticklabels([ch[:10] + '...' if len(ch) > 10 else ch for ch in channels], rotation=45)
    ax1.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 막대 위에 값 표시
    for bar, value in zip(bars1, subscribers):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                format_numbers(value, None), ha='center', va='bottom', fontsize=10)

    # 2. 구독자 당 조회수 (Views per Subscriber)
    ax2 = axes[1]
    views_per_sub = [channel_metrics[ch]['views_per_subscriber'] for ch in channels]

    bars2 = ax2.bar(range(len(channels)), views_per_sub, color='lightcoral', alpha=0.7)
    ax2.set_title(f'{category} - 구독자 당 총 조회수', fontsize=14, weight='bold')
    ax2.set_xlabel('채널', fontsize=12)
    ax2.set_ylabel('구독자 당 조회수', fontsize=12)
    ax2.set_xticks(range(len(channels)))
    ax2.set_xticklabels([ch[:10] + '...' if len(ch) > 10 else ch for ch in channels], rotation=45)

    # 막대 위에 값 표시
    for bar, value in zip(bars2, views_per_sub):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{value:.1f}', ha='center', va='bottom', fontsize=10)

    # 3. 구독자 참여도 (평균 영상 조회수 / 구독자수)
    ax3 = axes[2]
    engagement = [channel_metrics[ch]['subscriber_engagement'] for ch in channels]

    bars3 = ax3.bar(range(len(channels)), engagement, color='lightgreen', alpha=0.7)
    ax3.set_title(f'{category} - 구독자 참여도', fontsize=14, weight='bold')
    ax3.set_xlabel('채널', fontsize=12)
    ax3.set_ylabel('참여도 (평균 조회수/구독자수)', fontsize=12)
    ax3.set_xticks(range(len(channels)))
    ax3.set_xticklabels([ch[:10] + '...' if len(ch) > 10 else ch for ch in channels], rotation=45)

    # 막대 위에 값 표시
    for bar, value in zip(bars3, engagement):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{value:.3f}', ha='center', va='bottom', fontsize=10)

    # 4. 구독자수 vs 총 조회수 산점도
    ax4 = axes[3]
    total_views = [channel_metrics[ch]['total_views'] for ch in channels]

    colors = ['red', 'blue', 'green', 'orange', 'purple'][:len(channels)]
    for i, (sub, view, ch) in enumerate(zip(subscribers, total_views, channels)):
        ax4.scatter(sub, view, color=colors[i], s=100, alpha=0.7, label=ch[:15] + '...' if len(ch) > 15 else ch)

    ax4.set_title(f'{category} - 구독자수 vs 총 조회수', fontsize=14, weight='bold')
    ax4.set_xlabel('구독자수', fontsize=12)
    ax4.set_ylabel('총 조회수', fontsize=12)
    ax4.xaxis.set_major_formatter(FuncFormatter(format_numbers))
    ax4.yaxis.set_major_formatter(FuncFormatter(format_numbers))
    ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

    # 추세선 추가
    if len(subscribers) > 1:
        z = np.polyfit(subscribers, total_views, 1)
        p = np.poly1d(z)
        ax4.plot(subscribers, p(subscribers), "r--", alpha=0.8)

    # 5. 채널별 성과 등급
    ax5 = axes[4]
    grades = [channel_metrics[ch]['performance_grade'] for ch in channels]
    grade_colors = {'매우 높음': 'darkgreen', '높음': 'green', '보통': 'yellow', '낮음': 'orange', '매우 낮음': 'red'}
    colors = [grade_colors[grade] for grade in grades]

    bars5 = ax5.bar(range(len(channels)), [1]*len(channels), color=colors, alpha=0.7)
    ax5.set_title(f'{category} - 구독자 대비 성과 등급', fontsize=14, weight='bold')
    ax5.set_xlabel('채널', fontsize=12)
    ax5.set_ylabel('성과 등급', fontsize=12)
    ax5.set_xticks(range(len(channels)))
    ax5.set_xticklabels([ch[:10] + '...' if len(ch) > 10 else ch for ch in channels], rotation=45)
    ax5.set_ylim(0, 1.5)

    # 등급 텍스트 표시
    for i, (bar, grade) in enumerate(zip(bars5, grades)):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                grade, ha='center', va='center', fontsize=10, weight='bold')

    # 6. 효율성 지표 종합 비교 (레이더 차트 스타일)
    ax6 = axes[5]

    # 정규화된 지표들
    norm_subscribers = np.array(subscribers) / max(subscribers) if max(subscribers) > 0 else np.zeros(len(subscribers))
    norm_views_per_sub = np.array(views_per_sub) / max(views_per_sub) if max(views_per_sub) > 0 else np.zeros(len(views_per_sub))
    norm_engagement = np.array(engagement) / max(engagement) if max(engagement) > 0 else np.zeros(len(engagement))

    # 종합 효율성 점수
    efficiency_scores = (norm_views_per_sub + norm_engagement) / 2

    bars6 = ax6.bar(range(len(channels)), efficiency_scores, color='gold', alpha=0.7)
    ax6.set_title(f'{category} - 구독자 효율성 종합 점수', fontsize=14, weight='bold')
    ax6.set_xlabel('채널', fontsize=12)
    ax6.set_ylabel('효율성 점수 (정규화)', fontsize=12)
    ax6.set_xticks(range(len(channels)))
    ax6.set_xticklabels([ch[:10] + '...' if len(ch) > 10 else ch for ch in channels], rotation=45)

    # 최고 점수 강조
    if len(efficiency_scores) > 0:
        max_idx = np.argmax(efficiency_scores)
        bars6[max_idx].set_color('red')
        bars6[max_idx].set_alpha(1.0)

    plt.tight_layout()

    # 저장
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/08_subscriber_ratio_{category}.png', dpi=300, bbox_inches='tight')
    plt.show()

    return channel_metrics

def analyze_all_categories_subscriber_ratio(df, save_path="visualizations"):
    """
    모든 카테고리의 구독자 비율 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    save_path (str): 저장할 경로
    """
    categories = df['카테고리'].unique()
    results = {}

    # 각 카테고리별 분석
    for category in categories:
        print(f"Processing subscriber ratio analysis for category: {category}")
        try:
            category_results = analyze_subscriber_ratio_by_category(df, category, save_path)
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
    results = analyze_all_categories_subscriber_ratio(df)

    # 결과 출력
    print("\n=== 카테고리별 구독자 효율성 분석 ===" )
    for category, category_results in results.items():
        if category_results:
            print(f"\n{category}:")
            for channel, metrics in category_results.items():
                views_per_sub = metrics.get('views_per_subscriber', 0)
                grade = metrics.get('performance_grade', 'N/A')
                print(f"  {channel}: 구독자당 {views_per_sub:.1f} 조회수, 성과등급: {grade}")

    print("\n구독자 비율 분석이 완료되었습니다!")
    print("결과는 visualizations/ 폴더에 저장되었습니다.")