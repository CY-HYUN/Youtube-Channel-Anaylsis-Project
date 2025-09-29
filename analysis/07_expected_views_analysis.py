"""
7. 각 분야 별 & 분야별 - 채널별 기대조회수 충족 여부 파악
각 채널 별 전체 동영상의 기대조회수 기준으로 최근 200개 기대조회수 파악
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime, timedelta
from data_preprocessing import load_and_preprocess_data, filter_by_category, get_top_channels_by_category, setup_matplotlib, format_numbers
from matplotlib.ticker import FuncFormatter

def calculate_expected_views(df, channel_name, baseline_period_months=12):
    """
    채널의 기대 조회수를 계산합니다.

    Parameters:
    df (pd.DataFrame): 채널 데이터
    channel_name (str): 채널명
    baseline_period_months (int): 기준 기간 (개월)

    Returns:
    dict: 기대 조회수 관련 지표
    """
    channel_df = df[df['채널명'] == channel_name].copy()

    if channel_df.empty or '게시일' not in channel_df.columns:
        return {}

    # 날짜 순으로 정렬
    channel_df = channel_df.sort_values('게시일')

    # 기준일 설정 (가장 최근 데이터 기준)
    latest_date = channel_df['게시일'].max()
    baseline_start = latest_date - timedelta(days=baseline_period_months * 30)

    # 기준 기간 데이터 (기대치 계산용)
    baseline_data = channel_df[channel_df['게시일'] >= baseline_start].copy()

    if baseline_data.empty:
        # 기준 기간에 데이터가 없으면 전체 데이터 사용
        baseline_data = channel_df.copy()

    # 기대 조회수 계산 (평균, 중앙값, 분위수)
    expected_views_mean = baseline_data['조회수'].mean()
    expected_views_median = baseline_data['조회수'].median()
    expected_views_q25 = baseline_data['조회수'].quantile(0.25)
    expected_views_q75 = baseline_data['조회수'].quantile(0.75)

    # 최근 영상들의 성과 (최대 200개)
    recent_videos = channel_df.tail(min(200, len(channel_df))).copy()

    # 기대치 대비 성과 계산
    recent_videos['기대치_평균'] = expected_views_mean
    recent_videos['기대치_중앙값'] = expected_views_median
    recent_videos['성과비율_평균'] = recent_videos['조회수'] / expected_views_mean
    recent_videos['성과비율_중앙값'] = recent_videos['조회수'] / expected_views_median

    # 기대치 충족 여부
    recent_videos['기대치충족_평균'] = recent_videos['조회수'] >= expected_views_mean
    recent_videos['기대치충족_중앙값'] = recent_videos['조회수'] >= expected_views_median

    # 통계 계산
    success_rate_mean = recent_videos['기대치충족_평균'].mean() * 100
    success_rate_median = recent_videos['기대치충족_중앙값'].mean() * 100
    avg_performance_ratio = recent_videos['성과비율_평균'].mean()

    return {
        'expected_views_mean': expected_views_mean,
        'expected_views_median': expected_views_median,
        'expected_views_q25': expected_views_q25,
        'expected_views_q75': expected_views_q75,
        'recent_videos': recent_videos,
        'success_rate_mean': success_rate_mean,
        'success_rate_median': success_rate_median,
        'avg_performance_ratio': avg_performance_ratio,
        'total_recent_videos': len(recent_videos),
        'baseline_period': baseline_period_months
    }

def analyze_expected_views_by_category(df, category, save_path="visualizations"):
    """
    특정 카테고리의 기대 조회수 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    category (str): 분석할 카테고리
    save_path (str): 저장할 경로
    """
    category_df = filter_by_category(df, category)

    if category_df.empty:
        print(f"No data found for category: {category}")
        return

    # 상위 채널들 분석
    top_channels = get_top_channels_by_category(df, category, top_n=8)

    if not top_channels:
        print(f"No channels found for category: {category}")
        return

    # 각 채널별 기대 조회수 분석
    channel_results = {}
    for channel in top_channels:
        result = calculate_expected_views(category_df, channel)
        if result:
            channel_results[channel] = result

    if not channel_results:
        print(f"No valid expected views data for category: {category}")
        return

    # 시각화
    fig, axes = plt.subplots(3, 3, figsize=(20, 18))
    axes = axes.flatten()

    # 1. 채널별 기대치 충족률 (평균 기준)
    ax1 = axes[0]
    channels = list(channel_results.keys())
    success_rates = [channel_results[ch]['success_rate_mean'] for ch in channels]

    bars1 = ax1.bar(range(len(channels)), success_rates,
                   color=['green' if x >= 50 else 'red' for x in success_rates], alpha=0.7)
    ax1.set_title(f'{category} - 채널별 기대치 충족률 (평균 기준)', fontsize=14, weight='bold')
    ax1.set_xlabel('채널', fontsize=12)
    ax1.set_ylabel('충족률 (%)', fontsize=12)
    ax1.set_xticks(range(len(channels)))
    ax1.set_xticklabels([ch[:10] + '...' if len(ch) > 10 else ch for ch in channels], rotation=45)
    ax1.axhline(y=50, color='black', linestyle='--', alpha=0.7, label='50% 기준선')
    ax1.legend()

    # 막대 위에 값 표시
    for bar, value in zip(bars1, success_rates):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{value:.1f}%', ha='center', va='bottom', fontsize=10)

    # 2. 채널별 평균 성과 비율
    ax2 = axes[1]
    performance_ratios = [channel_results[ch]['avg_performance_ratio'] for ch in channels]

    bars2 = ax2.bar(range(len(channels)), performance_ratios,
                   color=['green' if x >= 1.0 else 'orange' if x >= 0.7 else 'red' for x in performance_ratios],
                   alpha=0.7)
    ax2.set_title(f'{category} - 채널별 평균 성과 비율', fontsize=14, weight='bold')
    ax2.set_xlabel('채널', fontsize=12)
    ax2.set_ylabel('성과 비율 (기대치 대비)', fontsize=12)
    ax2.set_xticks(range(len(channels)))
    ax2.set_xticklabels([ch[:10] + '...' if len(ch) > 10 else ch for ch in channels], rotation=45)
    ax2.axhline(y=1.0, color='black', linestyle='--', alpha=0.7, label='기대치 100%')
    ax2.legend()

    # 막대 위에 값 표시
    for bar, value in zip(bars2, performance_ratios):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{value:.2f}', ha='center', va='bottom', fontsize=10)

    # 3. 기대치 충족률 분포
    ax3 = axes[2]
    success_rate_ranges = ['매우 낮음 (0-25%)', '낮음 (25-50%)', '보통 (50-75%)', '높음 (75-100%)']
    very_low = len([r for r in success_rates if 0 <= r < 25])
    low = len([r for r in success_rates if 25 <= r < 50])
    medium = len([r for r in success_rates if 50 <= r < 75])
    high = len([r for r in success_rates if 75 <= r <= 100])

    sizes = [very_low, low, medium, high]
    colors = ['red', 'orange', 'yellow', 'green']

    ax3.pie(sizes, labels=success_rate_ranges, colors=colors, autopct='%1.1f%%', startangle=90)
    ax3.set_title(f'{category} - 기대치 충족률 분포', fontsize=14, weight='bold')

    # 4. 시간에 따른 성과 변화 (대표 채널)
    ax4 = axes[3]
    if channels:
        # 가장 많은 영상을 가진 채널 선택
        best_channel = max(channels, key=lambda x: channel_results[x]['total_recent_videos'])
        recent_videos = channel_results[best_channel]['recent_videos']

        if not recent_videos.empty and len(recent_videos) > 10:
            # 최근 50개 영상만 표시
            plot_data = recent_videos.tail(50).copy()
            plot_data['순번'] = range(len(plot_data))

            ax4.plot(plot_data['순번'], plot_data['성과비율_평균'], marker='o', alpha=0.7, color='blue')
            ax4.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='기대치 100%')
            ax4.set_title(f'{best_channel[:15]}... - 최근 성과 변화', fontsize=14, weight='bold')
            ax4.set_xlabel('영상 순번 (최근 순)', fontsize=12)
            ax4.set_ylabel('성과 비율', fontsize=12)
            ax4.legend()
            ax4.grid(True, alpha=0.3)

    # 5. 채널별 기대 조회수 비교
    ax5 = axes[4]
    expected_views = [channel_results[ch]['expected_views_mean'] for ch in channels]

    bars5 = ax5.bar(range(len(channels)), expected_views, color='lightblue', alpha=0.7)
    ax5.set_title(f'{category} - 채널별 기대 조회수', fontsize=14, weight='bold')
    ax5.set_xlabel('채널', fontsize=12)
    ax5.set_ylabel('기대 조회수', fontsize=12)
    ax5.set_xticks(range(len(channels)))
    ax5.set_xticklabels([ch[:10] + '...' if len(ch) > 10 else ch for ch in channels], rotation=45)
    ax5.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 막대 위에 값 표시
    for bar, value in zip(bars5, expected_views):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                format_numbers(value, None), ha='center', va='bottom', fontsize=10)

    # 6. 성과 비율 vs 기대 조회수 산점도
    ax6 = axes[5]
    ax6.scatter(expected_views, performance_ratios, alpha=0.7, color='purple', s=100)

    # 채널명 라벨 추가
    for i, channel in enumerate(channels):
        channel_name = channel[:8] + '...' if len(channel) > 8 else channel
        ax6.annotate(channel_name, (expected_views[i], performance_ratios[i]),
                   xytext=(5, 5), textcoords='offset points', fontsize=8)

    ax6.set_title(f'{category} - 기대 조회수 vs 성과 비율', fontsize=14, weight='bold')
    ax6.set_xlabel('기대 조회수', fontsize=12)
    ax6.set_ylabel('평균 성과 비율', fontsize=12)
    ax6.xaxis.set_major_formatter(FuncFormatter(format_numbers))
    ax6.axhline(y=1.0, color='red', linestyle='--', alpha=0.7)
    ax6.grid(True, alpha=0.3)

    # 7. 최근 성과 분포 (전체 채널)
    ax7 = axes[6]
    all_recent_ratios = []
    for channel, result in channel_results.items():
        if 'recent_videos' in result and not result['recent_videos'].empty:
            ratios = result['recent_videos']['성과비율_평균'].values
            all_recent_ratios.extend(ratios)

    if all_recent_ratios:
        # 이상치 제거 (99th percentile 기준)
        ratio_99th = np.percentile(all_recent_ratios, 99)
        filtered_ratios = [r for r in all_recent_ratios if r <= ratio_99th]

        ax7.hist(filtered_ratios, bins=30, alpha=0.7, color='lightgreen', edgecolor='black')
        ax7.axvline(x=1.0, color='red', linestyle='--', alpha=0.7, label='기대치 100%')
        ax7.axvline(x=np.mean(filtered_ratios), color='blue', linestyle='--', alpha=0.7,
                   label=f'평균: {np.mean(filtered_ratios):.2f}')
        ax7.set_title(f'{category} - 최근 성과 비율 분포', fontsize=14, weight='bold')
        ax7.set_xlabel('성과 비율', fontsize=12)
        ax7.set_ylabel('영상 수', fontsize=12)
        ax7.legend()

    # 8. 기대치 vs 실제 조회수 상위 10개 영상
    ax8 = axes[7]
    all_recent_videos = []
    for channel, result in channel_results.items():
        if 'recent_videos' in result and not result['recent_videos'].empty:
            videos = result['recent_videos'].copy()
            videos['채널명'] = channel
            all_recent_videos.append(videos)

    if all_recent_videos:
        combined_videos = pd.concat(all_recent_videos, ignore_index=True)
        top_performers = combined_videos.nlargest(10, '성과비율_평균')

        x_pos = range(len(top_performers))
        bars8_expected = ax8.bar(x_pos, top_performers['기대치_평균'].values,
                               alpha=0.7, color='lightcoral', label='기대 조회수')
        bars8_actual = ax8.bar(x_pos, top_performers['조회수'].values,
                             alpha=0.7, color='lightblue', label='실제 조회수')

        ax8.set_title(f'{category} - 상위 10개 영상 기대치 vs 실제', fontsize=14, weight='bold')
        ax8.set_xlabel('영상 순위', fontsize=12)
        ax8.set_ylabel('조회수', fontsize=12)
        ax8.yaxis.set_major_formatter(FuncFormatter(format_numbers))
        ax8.legend()

    # 9. 카테고리 전체 성과 요약
    ax9 = axes[8]

    # 전체 통계 계산
    total_videos = sum([result['total_recent_videos'] for result in channel_results.values()])
    avg_success_rate = np.mean(success_rates) if success_rates else 0
    avg_performance_ratio = np.mean(performance_ratios) if performance_ratios else 0

    # 성과 등급 분류
    if avg_success_rate >= 75 and avg_performance_ratio >= 1.2:
        grade = "우수"
        grade_color = "green"
    elif avg_success_rate >= 50 and avg_performance_ratio >= 1.0:
        grade = "양호"
        grade_color = "blue"
    elif avg_success_rate >= 25 and avg_performance_ratio >= 0.7:
        grade = "보통"
        grade_color = "orange"
    else:
        grade = "개선필요"
        grade_color = "red"

    # 텍스트 표시
    summary_text = f"""
    {category} 카테고리 성과 요약

    분석 채널 수: {len(channels)}개
    총 분석 영상: {total_videos}개

    평균 기대치 충족률: {avg_success_rate:.1f}%
    평균 성과 비율: {avg_performance_ratio:.2f}

    종합 등급: {grade}
    """

    ax9.text(0.5, 0.5, summary_text, ha='center', va='center', fontsize=12,
            bbox=dict(boxstyle='round,pad=0.5', facecolor=grade_color, alpha=0.3))
    ax9.set_xlim(0, 1)
    ax9.set_ylim(0, 1)
    ax9.axis('off')
    ax9.set_title(f'{category} - 종합 성과 평가', fontsize=14, weight='bold')

    plt.tight_layout()

    # 저장
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/07_expected_views_{category}.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 분석 결과 반환
    results = {
        'channel_results': channel_results,
        'avg_success_rate': avg_success_rate,
        'avg_performance_ratio': avg_performance_ratio,
        'grade': grade,
        'total_channels': len(channels),
        'total_videos': total_videos
    }

    return results

def analyze_all_categories_expected_views(df, save_path="visualizations"):
    """
    모든 카테고리의 기대 조회수 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    save_path (str): 저장할 경로
    """
    categories = df['카테고리'].unique()
    results = {}

    # 각 카테고리별 분석
    for category in categories:
        print(f"Processing expected views analysis for category: {category}")
        try:
            category_results = analyze_expected_views_by_category(df, category, save_path)
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
    results = analyze_all_categories_expected_views(df)

    # 결과 출력
    print("\n=== 카테고리별 기대 조회수 분석 결과 ===")
    for category, result in results.items():
        if 'avg_success_rate' in result:
            success_rate = result['avg_success_rate']
            performance_ratio = result['avg_performance_ratio']
            grade = result['grade']
            print(f"{category}: 기대치 충족률 {success_rate:.1f}%, 성과비율 {performance_ratio:.2f}, 등급 {grade}")

    print("\n기대 조회수 분석이 완료되었습니다!")
    print("결과는 visualizations/ 폴더에 저장되었습니다.")