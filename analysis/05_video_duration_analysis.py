"""
5. 각 분야별 & 채널별 재생시간, 총 조회수 분포 파악으로 조회수대비 상위 10개 하위 10개 재생시간 비교
각 분야별 재생시간이 길수록 조회수가 낮을까? (영상길이가 길수록 사람들은 피로감을 느낀다)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from scipy.stats import pearsonr
from data_preprocessing import load_and_preprocess_data, filter_by_category, get_top_channels_by_category, setup_matplotlib, format_numbers
from matplotlib.ticker import FuncFormatter

def categorize_video_duration(duration_minutes):
    """
    영상 길이를 카테고리로 분류합니다.

    Parameters:
    duration_minutes (float): 영상 길이 (분)

    Returns:
    str: 길이 카테고리
    """
    if duration_minutes <= 5:
        return '초단편 (5분 이하)'
    elif duration_minutes <= 15:
        return '단편 (5-15분)'
    elif duration_minutes <= 30:
        return '중편 (15-30분)'
    elif duration_minutes <= 60:
        return '장편 (30-60분)'
    else:
        return '초장편 (60분 초과)'

def analyze_duration_performance_by_category(df, category, save_path="visualizations"):
    """
    특정 카테고리의 영상 길이와 성과 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    category (str): 분석할 카테고리
    save_path (str): 저장할 경로
    """
    category_df = filter_by_category(df, category)

    if category_df.empty:
        print(f"No data found for category: {category}")
        return

    # 필요한 컬럼 확인
    if '재생 시간(분)' not in category_df.columns:
        print(f"No duration data for category: {category}")
        return

    # 데이터 전처리
    category_df = category_df.copy()
    category_df = category_df.dropna(subset=['재생 시간(분)', '조회수'])

    # 이상치 제거 (99th percentile 기준)
    duration_99th = category_df['재생 시간(분)'].quantile(0.99)
    views_99th = category_df['조회수'].quantile(0.99)

    category_df = category_df[
        (category_df['재생 시간(분)'] <= duration_99th) &
        (category_df['조회수'] <= views_99th) &
        (category_df['재생 시간(분)'] > 0)
    ]

    if category_df.empty:
        print(f"No valid data after filtering for category: {category}")
        return

    # 영상 길이 카테고리 추가
    category_df['길이카테고리'] = category_df['재생 시간(분)'].apply(categorize_video_duration)

    # 조회수 기준 상위/하위 10개 영상
    top_10_views = category_df.nlargest(10, '조회수')
    bottom_10_views = category_df.nsmallest(10, '조회수')

    # 시각화
    fig, axes = plt.subplots(3, 3, figsize=(20, 18))
    axes = axes.flatten()

    # 1. 영상 길이 vs 조회수 산점도
    ax1 = axes[0]
    ax1.scatter(category_df['재생 시간(분)'], category_df['조회수'], alpha=0.6, color='blue')
    ax1.set_title(f'{category} - 영상 길이 vs 조회수', fontsize=14, weight='bold')
    ax1.set_xlabel('재생 시간 (분)', fontsize=12)
    ax1.set_ylabel('조회수', fontsize=12)
    ax1.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 상관계수 계산 및 표시
    if len(category_df) > 1:
        correlation, p_value = pearsonr(category_df['재생 시간(분)'], category_df['조회수'])
        corr_text = f"상관계수: {correlation:.3f}\np-value: {p_value:.3e}"
        ax1.text(0.05, 0.95, corr_text, transform=ax1.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # 추세선 추가
        z = np.polyfit(category_df['재생 시간(분)'], category_df['조회수'], 1)
        p = np.poly1d(z)
        ax1.plot(category_df['재생 시간(분)'], p(category_df['재생 시간(분)']), "r--", alpha=0.8)

    # 2. 길이 카테고리별 평균 조회수
    ax2 = axes[1]
    duration_categories = ['초단편 (5분 이하)', '단편 (5-15분)', '중편 (15-30분)', '장편 (30-60분)', '초장편 (60분 초과)']
    duration_views = category_df.groupby('길이카테고리')['조회수'].mean().reindex(duration_categories, fill_value=0)

    bars2 = ax2.bar(range(len(duration_views)), duration_views.values, color='lightcoral', alpha=0.7)
    ax2.set_title(f'{category} - 길이별 평균 조회수', fontsize=14, weight='bold')
    ax2.set_xlabel('영상 길이 카테고리', fontsize=12)
    ax2.set_ylabel('평균 조회수', fontsize=12)
    ax2.set_xticks(range(len(duration_views)))
    ax2.set_xticklabels(duration_views.index, rotation=45)
    ax2.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 막대 위에 값 표시
    for bar, value in zip(bars2, duration_views.values):
        if value > 0:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    format_numbers(value, None), ha='center', va='bottom', fontsize=10)

    # 3. 상위 10개 vs 하위 10개 영상 길이 비교
    ax3 = axes[2]
    top_durations = top_10_views['재생 시간(분)'].values
    bottom_durations = bottom_10_views['재생 시간(분)'].values

    positions = [1, 2]
    data_to_plot = [top_durations, bottom_durations]
    labels = ['상위 10개', '하위 10개']

    bp = ax3.boxplot(data_to_plot, positions=positions, patch_artist=True, labels=labels)
    bp['boxes'][0].set_facecolor('gold')
    bp['boxes'][1].set_facecolor('lightblue')

    ax3.set_title(f'{category} - 조회수 상/하위 10개 영상 길이 분포', fontsize=14, weight='bold')
    ax3.set_ylabel('재생 시간 (분)', fontsize=12)

    # 평균값 표시
    top_mean = np.mean(top_durations) if len(top_durations) > 0 else 0
    bottom_mean = np.mean(bottom_durations) if len(bottom_durations) > 0 else 0
    ax3.text(1, top_mean, f'평균: {top_mean:.1f}분', ha='center', va='bottom', fontsize=10, weight='bold')
    ax3.text(2, bottom_mean, f'평균: {bottom_mean:.1f}분', ha='center', va='bottom', fontsize=10, weight='bold')

    # 4. 길이 카테고리별 영상 수 분포
    ax4 = axes[3]
    duration_counts = category_df['길이카테고리'].value_counts().reindex(duration_categories, fill_value=0)

    wedges, texts, autotexts = ax4.pie(duration_counts.values, labels=duration_counts.index,
                                       autopct='%1.1f%%', startangle=90)
    ax4.set_title(f'{category} - 길이별 영상 수 분포', fontsize=14, weight='bold')

    # 5. 시간대별 평균 조회수 (10분 단위)
    ax5 = axes[4]

    # 10분 단위로 그룹화
    category_df['시간대_10분단위'] = (category_df['재생 시간(분)'] // 10) * 10
    time_groups = category_df.groupby('시간대_10분단위')['조회수'].agg(['mean', 'count']).reset_index()

    # 영상 수가 5개 이상인 그룹만 표시
    time_groups = time_groups[time_groups['count'] >= 5]

    if not time_groups.empty:
        bars5 = ax5.bar(time_groups['시간대_10분단위'], time_groups['mean'], width=8, alpha=0.7, color='green')
        ax5.set_title(f'{category} - 시간대별 평균 조회수 (10분 단위)', fontsize=14, weight='bold')
        ax5.set_xlabel('재생 시간 (분)', fontsize=12)
        ax5.set_ylabel('평균 조회수', fontsize=12)
        ax5.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 6. 채널별 평균 영상 길이 vs 평균 조회수
    ax6 = axes[5]
    top_channels = get_top_channels_by_category(df, category, top_n=8)

    if top_channels:
        channel_stats = []
        for channel in top_channels:
            channel_data = category_df[category_df['채널명'] == channel]
            if not channel_data.empty:
                avg_duration = channel_data['재생 시간(분)'].mean()
                avg_views = channel_data['조회수'].mean()
                channel_stats.append({
                    '채널명': channel,
                    '평균길이': avg_duration,
                    '평균조회수': avg_views
                })

        if channel_stats:
            channel_df_stats = pd.DataFrame(channel_stats)
            ax6.scatter(channel_df_stats['평균길이'], channel_df_stats['평균조회수'],
                       s=100, alpha=0.7, color='purple')

            # 채널명 라벨 추가
            for i, row in channel_df_stats.iterrows():
                channel_name = row['채널명'][:10] + '...' if len(row['채널명']) > 10 else row['채널명']
                ax6.annotate(channel_name, (row['평균길이'], row['평균조회수']),
                           xytext=(5, 5), textcoords='offset points', fontsize=8)

            ax6.set_title(f'{category} - 채널별 평균 길이 vs 평균 조회수', fontsize=14, weight='bold')
            ax6.set_xlabel('평균 영상 길이 (분)', fontsize=12)
            ax6.set_ylabel('평균 조회수', fontsize=12)
            ax6.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 7. 길이별 좋아요율 분석
    ax7 = axes[6]
    category_df['좋아요율'] = (category_df['좋아요 수'] / category_df['조회수'] * 100).fillna(0)

    # 이상치 제거
    category_df_filtered = category_df[category_df['좋아요율'] <= 20]  # 20% 이하만

    duration_like_rate = category_df_filtered.groupby('길이카테고리')['좋아요율'].mean().reindex(duration_categories, fill_value=0)

    bars7 = ax7.bar(range(len(duration_like_rate)), duration_like_rate.values, color='orange', alpha=0.7)
    ax7.set_title(f'{category} - 길이별 평균 좋아요율', fontsize=14, weight='bold')
    ax7.set_xlabel('영상 길이 카테고리', fontsize=12)
    ax7.set_ylabel('평균 좋아요율 (%)', fontsize=12)
    ax7.set_xticks(range(len(duration_like_rate)))
    ax7.set_xticklabels(duration_like_rate.index, rotation=45)

    # 8. 길이별 댓글율 분석
    ax8 = axes[7]
    category_df['댓글율'] = (category_df['댓글 수'] / category_df['조회수'] * 100).fillna(0)

    # 이상치 제거
    category_df_filtered = category_df[category_df['댓글율'] <= 5]  # 5% 이하만

    duration_comment_rate = category_df_filtered.groupby('길이카테고리')['댓글율'].mean().reindex(duration_categories, fill_value=0)

    bars8 = ax8.bar(range(len(duration_comment_rate)), duration_comment_rate.values, color='lightgreen', alpha=0.7)
    ax8.set_title(f'{category} - 길이별 평균 댓글율', fontsize=14, weight='bold')
    ax8.set_xlabel('영상 길이 카테고리', fontsize=12)
    ax8.set_ylabel('평균 댓글율 (%)', fontsize=12)
    ax8.set_xticks(range(len(duration_comment_rate)))
    ax8.set_xticklabels(duration_comment_rate.index, rotation=45)

    # 9. 최적 길이 분석 (종합 점수)
    ax9 = axes[8]

    # 정규화된 종합 점수 계산
    duration_performance = category_df.groupby('길이카테고리').agg({
        '조회수': 'mean',
        '좋아요 수': 'mean',
        '댓글 수': 'mean'
    }).reindex(duration_categories, fill_value=0)

    # 정규화 (0-1 스케일)
    for col in duration_performance.columns:
        max_val = duration_performance[col].max()
        if max_val > 0:
            duration_performance[col] = duration_performance[col] / max_val

    # 종합 점수 계산 (가중평균)
    duration_performance['종합점수'] = (
        duration_performance['조회수'] * 0.5 +
        duration_performance['좋아요 수'] * 0.3 +
        duration_performance['댓글 수'] * 0.2
    )

    bars9 = ax9.bar(range(len(duration_performance)), duration_performance['종합점수'].values,
                   color='gold', alpha=0.7)
    ax9.set_title(f'{category} - 길이별 종합 성과 점수', fontsize=14, weight='bold')
    ax9.set_xlabel('영상 길이 카테고리', fontsize=12)
    ax9.set_ylabel('종합 점수 (정규화)', fontsize=12)
    ax9.set_xticks(range(len(duration_performance)))
    ax9.set_xticklabels(duration_performance.index, rotation=45)

    # 최고 점수 강조
    max_idx = duration_performance['종합점수'].idxmax()
    max_pos = list(duration_performance.index).index(max_idx)
    bars9[max_pos].set_color('red')
    bars9[max_pos].set_alpha(1.0)

    # 막대 위에 값 표시
    for bar, value in zip(bars9, duration_performance['종합점수'].values):
        ax9.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.3f}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()

    # 저장
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/05_video_duration_{category}.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 분석 결과 반환
    results = {
        'correlation': correlation if len(category_df) > 1 else 0,
        'p_value': p_value if len(category_df) > 1 else 1,
        'top_10_avg_duration': top_mean,
        'bottom_10_avg_duration': bottom_mean,
        'duration_views': duration_views.to_dict(),
        'best_duration_category': max_idx,
        'duration_performance': duration_performance.to_dict()
    }

    return results

def analyze_all_categories_duration(df, save_path="visualizations"):
    """
    모든 카테고리의 영상 길이 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    save_path (str): 저장할 경로
    """
    categories = df['카테고리'].unique()
    results = {}

    # 각 카테고리별 분석
    for category in categories:
        print(f"Processing video duration analysis for category: {category}")
        try:
            category_results = analyze_duration_performance_by_category(df, category, save_path)
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
    results = analyze_all_categories_duration(df)

    # 결과 출력
    print("\n=== 카테고리별 영상 길이 분석 결과 ===")
    for category, result in results.items():
        if 'correlation' in result:
            correlation = result['correlation']
            best_duration = result.get('best_duration_category', 'N/A')
            print(f"{category}: 길이-조회수 상관관계 {correlation:.3f}, 최적 길이 {best_duration}")

    print("\n영상 길이 분석이 완료되었습니다!")
    print("결과는 visualizations/ 폴더에 저장되었습니다.")