"""
6. 각 분야별 - 채널별 채널 개설일에 따른 총 구독자수 및 총 조회수 비교
채널 개설일이 오래되었다고 총 구독자수 및 총 조회수가 높은것이 아니다.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime, timedelta
from scipy.stats import pearsonr
from data_preprocessing import load_and_preprocess_data, filter_by_category, get_top_channels_by_category, setup_matplotlib, format_numbers
from matplotlib.ticker import FuncFormatter

def calculate_channel_age(creation_date, reference_date=None):
    """
    채널 생성일로부터 현재까지의 기간을 계산합니다.

    Parameters:
    creation_date: 채널 생성일
    reference_date: 기준일 (기본값: 현재 날짜)

    Returns:
    int: 채널 나이 (일 단위)
    """
    if reference_date is None:
        reference_date = datetime.now()

    if pd.isna(creation_date):
        return None

    try:
        if isinstance(creation_date, str):
            creation_date = pd.to_datetime(creation_date)

        age_days = (reference_date - creation_date).days
        return max(0, age_days)  # 음수 방지
    except:
        return None

def categorize_channel_age(age_days):
    """
    채널 나이를 카테고리로 분류합니다.

    Parameters:
    age_days (int): 채널 나이 (일 단위)

    Returns:
    str: 나이 카테고리
    """
    if age_days is None:
        return '알 수 없음'

    age_years = age_days / 365.25

    if age_years < 1:
        return '신생 (1년 미만)'
    elif age_years < 3:
        return '성장기 (1-3년)'
    elif age_years < 5:
        return '안정기 (3-5년)'
    elif age_years < 10:
        return '성숙기 (5-10년)'
    else:
        return '원로 (10년 이상)'

def analyze_channel_age_by_category(df, category, save_path="visualizations"):
    """
    특정 카테고리의 채널 나이 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    category (str): 분석할 카테고리
    save_path (str): 저장할 경로
    """
    category_df = filter_by_category(df, category)

    if category_df.empty:
        print(f"No data found for category: {category}")
        return

    # 채널별 통계 계산
    channel_stats = category_df.groupby('채널명').agg({
        '조회수': 'sum',
        '좋아요 수': 'sum',
        '댓글 수': 'sum',
        '구독자 수': 'first',  # 채널별로 동일하다고 가정
        '채널 개설일': 'first'
    }).reset_index()

    # 채널 나이 계산
    reference_date = datetime(2024, 9, 29)  # 분석 기준일
    channel_stats['채널나이_일'] = channel_stats['채널 개설일'].apply(
        lambda x: calculate_channel_age(x, reference_date)
    )
    channel_stats['채널나이_년'] = channel_stats['채널나이_일'] / 365.25
    channel_stats['나이카테고리'] = channel_stats['채널나이_일'].apply(categorize_channel_age)

    # 유효한 데이터만 필터링
    valid_channels = channel_stats.dropna(subset=['채널나이_일', '구독자 수', '조회수'])

    if valid_channels.empty:
        print(f"No valid channel age data for category: {category}")
        return

    # 시각화
    fig, axes = plt.subplots(3, 3, figsize=(20, 18))
    axes = axes.flatten()

    # 1. 채널 나이 vs 구독자 수
    ax1 = axes[0]
    ax1.scatter(valid_channels['채널나이_년'], valid_channels['구독자 수'], alpha=0.7, color='blue', s=60)
    ax1.set_title(f'{category} - 채널 나이 vs 구독자 수', fontsize=14, weight='bold')
    ax1.set_xlabel('채널 나이 (년)', fontsize=12)
    ax1.set_ylabel('구독자 수', fontsize=12)
    ax1.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 상관계수 계산 및 표시
    if len(valid_channels) > 1:
        age_sub_corr, age_sub_p = pearsonr(valid_channels['채널나이_년'], valid_channels['구독자 수'])
        corr_text = f"상관계수: {age_sub_corr:.3f}\np-value: {age_sub_p:.3e}"
        ax1.text(0.05, 0.95, corr_text, transform=ax1.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # 추세선 추가
        z = np.polyfit(valid_channels['채널나이_년'], valid_channels['구독자 수'], 1)
        p = np.poly1d(z)
        ax1.plot(valid_channels['채널나이_년'], p(valid_channels['채널나이_년']), "r--", alpha=0.8)

    # 2. 채널 나이 vs 총 조회수
    ax2 = axes[1]
    ax2.scatter(valid_channels['채널나이_년'], valid_channels['조회수'], alpha=0.7, color='green', s=60)
    ax2.set_title(f'{category} - 채널 나이 vs 총 조회수', fontsize=14, weight='bold')
    ax2.set_xlabel('채널 나이 (년)', fontsize=12)
    ax2.set_ylabel('총 조회수', fontsize=12)
    ax2.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 상관계수 계산 및 표시
    if len(valid_channels) > 1:
        age_views_corr, age_views_p = pearsonr(valid_channels['채널나이_년'], valid_channels['조회수'])
        corr_text = f"상관계수: {age_views_corr:.3f}\np-value: {age_views_p:.3e}"
        ax2.text(0.05, 0.95, corr_text, transform=ax2.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # 추세선 추가
        z = np.polyfit(valid_channels['채널나이_년'], valid_channels['조회수'], 1)
        p = np.poly1d(z)
        ax2.plot(valid_channels['채널나이_년'], p(valid_channels['조회수']), "r--", alpha=0.8)

    # 3. 나이 카테고리별 평균 구독자 수
    ax3 = axes[2]
    age_categories = ['신생 (1년 미만)', '성장기 (1-3년)', '안정기 (3-5년)', '성숙기 (5-10년)', '원로 (10년 이상)']
    age_subscribers = valid_channels.groupby('나이카테고리')['구독자 수'].mean().reindex(age_categories, fill_value=0)

    bars3 = ax3.bar(range(len(age_subscribers)), age_subscribers.values, color='lightcoral', alpha=0.7)
    ax3.set_title(f'{category} - 나이별 평균 구독자 수', fontsize=14, weight='bold')
    ax3.set_xlabel('채널 나이 카테고리', fontsize=12)
    ax3.set_ylabel('평균 구독자 수', fontsize=12)
    ax3.set_xticks(range(len(age_subscribers)))
    ax3.set_xticklabels(age_subscribers.index, rotation=45)
    ax3.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 막대 위에 값 표시
    for bar, value in zip(bars3, age_subscribers.values):
        if value > 0:
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    format_numbers(value, None), ha='center', va='bottom', fontsize=10)

    # 4. 나이 카테고리별 평균 조회수
    ax4 = axes[3]
    age_views = valid_channels.groupby('나이카테고리')['조회수'].mean().reindex(age_categories, fill_value=0)

    bars4 = ax4.bar(range(len(age_views)), age_views.values, color='lightblue', alpha=0.7)
    ax4.set_title(f'{category} - 나이별 평균 총 조회수', fontsize=14, weight='bold')
    ax4.set_xlabel('채널 나이 카테고리', fontsize=12)
    ax4.set_ylabel('평균 총 조회수', fontsize=12)
    ax4.set_xticks(range(len(age_views)))
    ax4.set_xticklabels(age_views.index, rotation=45)
    ax4.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 5. 채널 나이 분포
    ax5 = axes[4]
    age_counts = valid_channels['나이카테고리'].value_counts().reindex(age_categories, fill_value=0)

    wedges, texts, autotexts = ax5.pie(age_counts.values, labels=age_counts.index,
                                       autopct='%1.1f%%', startangle=90)
    ax5.set_title(f'{category} - 채널 나이 분포', fontsize=14, weight='bold')

    # 6. 구독자 수 vs 총 조회수 (채널 나이별 색상)
    ax6 = axes[5]

    # 나이 카테고리별 색상 매핑
    colors = {'신생 (1년 미만)': 'red', '성장기 (1-3년)': 'orange', '안정기 (3-5년)': 'yellow',
              '성숙기 (5-10년)': 'green', '원로 (10년 이상)': 'blue', '알 수 없음': 'gray'}

    for category_name in age_categories:
        cat_data = valid_channels[valid_channels['나이카테고리'] == category_name]
        if not cat_data.empty:
            ax6.scatter(cat_data['구독자 수'], cat_data['조회수'],
                       label=category_name, alpha=0.7, s=60,
                       color=colors.get(category_name, 'gray'))

    ax6.set_title(f'{category} - 구독자 수 vs 총 조회수 (나이별)', fontsize=14, weight='bold')
    ax6.set_xlabel('구독자 수', fontsize=12)
    ax6.set_ylabel('총 조회수', fontsize=12)
    ax6.xaxis.set_major_formatter(FuncFormatter(format_numbers))
    ax6.yaxis.set_major_formatter(FuncFormatter(format_numbers))
    ax6.legend(fontsize=8)

    # 7. 채널별 성과 효율성 (구독자 대비 조회수)
    ax7 = axes[6]
    valid_channels['조회수_구독자_비율'] = valid_channels['조회수'] / valid_channels['구독자 수']

    # 이상치 제거 (99th percentile 기준)
    ratio_99th = valid_channels['조회수_구독자_비율'].quantile(0.99)
    filtered_channels = valid_channels[valid_channels['조회수_구독자_비율'] <= ratio_99th]

    ax7.scatter(filtered_channels['채널나이_년'], filtered_channels['조회수_구독자_비율'],
               alpha=0.7, color='purple', s=60)
    ax7.set_title(f'{category} - 채널 나이 vs 구독자 대비 조회수 비율', fontsize=14, weight='bold')
    ax7.set_xlabel('채널 나이 (년)', fontsize=12)
    ax7.set_ylabel('총 조회수 / 구독자 수', fontsize=12)

    # 8. 나이별 평균 영상당 조회수
    ax8 = axes[7]

    # 영상 수 계산 (채널별)
    video_counts = category_df.groupby('채널명').size().reset_index(name='영상수')
    channel_stats_with_videos = valid_channels.merge(video_counts, on='채널명', how='left')
    channel_stats_with_videos['영상당_평균조회수'] = (
        channel_stats_with_videos['조회수'] / channel_stats_with_videos['영상수']
    )

    age_avg_views_per_video = (channel_stats_with_videos.groupby('나이카테고리')['영상당_평균조회수']
                              .mean().reindex(age_categories, fill_value=0))

    bars8 = ax8.bar(range(len(age_avg_views_per_video)), age_avg_views_per_video.values,
                   color='lightgreen', alpha=0.7)
    ax8.set_title(f'{category} - 나이별 평균 영상당 조회수', fontsize=14, weight='bold')
    ax8.set_xlabel('채널 나이 카테고리', fontsize=12)
    ax8.set_ylabel('평균 영상당 조회수', fontsize=12)
    ax8.set_xticks(range(len(age_avg_views_per_video)))
    ax8.set_xticklabels(age_avg_views_per_video.index, rotation=45)
    ax8.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 9. 성공 지표 종합 분석
    ax9 = axes[8]

    # 정규화된 종합 점수 계산
    age_performance = valid_channels.groupby('나이카테고리').agg({
        '구독자 수': 'mean',
        '조회수': 'mean',
        '좋아요 수': 'mean'
    }).reindex(age_categories, fill_value=0)

    # 정규화 (0-1 스케일)
    for col in age_performance.columns:
        max_val = age_performance[col].max()
        if max_val > 0:
            age_performance[col] = age_performance[col] / max_val

    # 종합 점수 계산 (가중평균)
    age_performance['종합점수'] = (
        age_performance['구독자 수'] * 0.4 +
        age_performance['조회수'] * 0.4 +
        age_performance['좋아요 수'] * 0.2
    )

    bars9 = ax9.bar(range(len(age_performance)), age_performance['종합점수'].values,
                   color='gold', alpha=0.7)
    ax9.set_title(f'{category} - 나이별 종합 성과 점수', fontsize=14, weight='bold')
    ax9.set_xlabel('채널 나이 카테고리', fontsize=12)
    ax9.set_ylabel('종합 점수 (정규화)', fontsize=12)
    ax9.set_xticks(range(len(age_performance)))
    ax9.set_xticklabels(age_performance.index, rotation=45)

    # 최고 점수 강조
    max_idx = age_performance['종합점수'].idxmax()
    max_pos = list(age_performance.index).index(max_idx)
    bars9[max_pos].set_color('red')
    bars9[max_pos].set_alpha(1.0)

    plt.tight_layout()

    # 저장
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/06_channel_age_{category}.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 분석 결과 반환
    results = {
        'age_subscribers_correlation': age_sub_corr if len(valid_channels) > 1 else 0,
        'age_views_correlation': age_views_corr if len(valid_channels) > 1 else 0,
        'best_age_category': max_idx,
        'age_performance': age_performance.to_dict(),
        'channel_count': len(valid_channels)
    }

    return results

def analyze_all_categories_channel_age(df, save_path="visualizations"):
    """
    모든 카테고리의 채널 나이 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    save_path (str): 저장할 경로
    """
    categories = df['카테고리'].unique()
    results = {}

    # 각 카테고리별 분석
    for category in categories:
        print(f"Processing channel age analysis for category: {category}")
        try:
            category_results = analyze_channel_age_by_category(df, category, save_path)
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
    results = analyze_all_categories_channel_age(df)

    # 결과 출력
    print("\n=== 카테고리별 채널 나이 분석 결과 ===")
    for category, result in results.items():
        if 'age_subscribers_correlation' in result:
            age_sub_corr = result['age_subscribers_correlation']
            age_views_corr = result['age_views_correlation']
            best_age = result.get('best_age_category', 'N/A')
            print(f"{category}: 나이-구독자 상관관계 {age_sub_corr:.3f}, 나이-조회수 상관관계 {age_views_corr:.3f}")
            print(f"         최고 성과 나이대: {best_age}")

    print("\n채널 나이 분석이 완료되었습니다!")
    print("결과는 visualizations/ 폴더에 저장되었습니다.")