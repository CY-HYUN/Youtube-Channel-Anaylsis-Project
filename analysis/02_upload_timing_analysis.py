"""
2. 각 분야별 & 채널별 - 요일, 시간대별 평균 조회수
각 분야 및 채널별 가장 많이 나오는 조회수의 요일 및 시간대 분석
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from data_preprocessing import load_and_preprocess_data, filter_by_category, get_top_channels_by_category, setup_matplotlib, format_numbers
from matplotlib.ticker import FuncFormatter

def analyze_upload_timing_by_category(df, category, save_path="visualizations"):
    """
    특정 카테고리의 업로드 타이밍 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    category (str): 분석할 카테고리
    save_path (str): 저장할 경로
    """
    category_df = filter_by_category(df, category)

    if category_df.empty:
        print(f"No data found for category: {category}")
        return

    # 요일별 한국어 매핑
    day_mapping = {
        'Monday': '월요일',
        'Tuesday': '화요일',
        'Wednesday': '수요일',
        'Thursday': '목요일',
        'Friday': '금요일',
        'Saturday': '토요일',
        'Sunday': '일요일'
    }

    # 요일별, 시간대별 평균 조회수 계산
    day_views = category_df.groupby('요일')['조회수'].mean().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    hour_views = category_df.groupby('시간대')['조회수'].mean()

    # 시각화
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. 요일별 평균 조회수
    ax1 = axes[0, 0]
    day_views_korean = day_views.copy()
    day_views_korean.index = [day_mapping.get(day, day) for day in day_views_korean.index]

    bars1 = ax1.bar(day_views_korean.index, day_views_korean.values, color='skyblue', alpha=0.7)
    ax1.set_title(f'{category} - 요일별 평균 조회수', fontsize=14, weight='bold')
    ax1.set_xlabel('요일', fontsize=12)
    ax1.set_ylabel('평균 조회수', fontsize=12)
    ax1.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 막대 위에 값 표시
    for bar, value in zip(bars1, day_views_korean.values):
        if not np.isnan(value):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    format_numbers(value, None), ha='center', va='bottom', fontsize=10)

    # 2. 시간대별 평균 조회수
    ax2 = axes[0, 1]
    bars2 = ax2.bar(hour_views.index, hour_views.values, color='lightcoral', alpha=0.7)
    ax2.set_title(f'{category} - 시간대별 평균 조회수', fontsize=14, weight='bold')
    ax2.set_xlabel('시간대', fontsize=12)
    ax2.set_ylabel('평균 조회수', fontsize=12)
    ax2.yaxis.set_major_formatter(FuncFormatter(format_numbers))
    ax2.set_xticks(range(0, 24, 3))

    # 최고/최저 시간대 표시
    max_hour = hour_views.idxmax()
    min_hour = hour_views.idxmin()
    ax2.axvline(x=max_hour, color='red', linestyle='--', alpha=0.7, label=f'최고: {max_hour}시')
    ax2.axvline(x=min_hour, color='blue', linestyle='--', alpha=0.7, label=f'최저: {min_hour}시')
    ax2.legend()

    # 3. 채널별 최적 요일 비교 (상위 5개 채널)
    ax3 = axes[1, 0]
    top_channels = get_top_channels_by_category(df, category, top_n=5)

    if top_channels:
        channel_best_days = {}
        for channel in top_channels:
            channel_df = category_df[category_df['채널명'] == channel]
            if not channel_df.empty:
                best_day = channel_df.groupby('요일')['조회수'].mean().idxmax()
                channel_best_days[channel] = day_mapping.get(best_day, best_day)

        if channel_best_days:
            channels = list(channel_best_days.keys())
            best_days = list(channel_best_days.values())

            bars3 = ax3.barh(channels, range(len(channels)), color='lightgreen', alpha=0.7)
            ax3.set_title(f'{category} - 채널별 최적 업로드 요일', fontsize=14, weight='bold')
            ax3.set_xlabel('순위', fontsize=12)

            # 요일 정보를 텍스트로 표시
            for i, (bar, day) in enumerate(zip(bars3, best_days)):
                ax3.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                        day, ha='left', va='center', fontsize=10, weight='bold')

    # 4. 히트맵: 요일 × 시간대 조회수 분포
    ax4 = axes[1, 1]
    if '요일' in category_df.columns and '시간대' in category_df.columns:
        # 피벗 테이블 생성
        heatmap_data = category_df.pivot_table(
            values='조회수',
            index='요일',
            columns='시간대',
            aggfunc='mean'
        )

        # 요일 순서 정렬
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(day_order)
        heatmap_data.index = [day_mapping.get(day, day) for day in heatmap_data.index]

        sns.heatmap(heatmap_data, cmap='YlOrRd', cbar_kws={'label': '평균 조회수'}, ax=ax4)
        ax4.set_title(f'{category} - 요일 × 시간대 조회수 히트맵', fontsize=14, weight='bold')
        ax4.set_xlabel('시간대', fontsize=12)
        ax4.set_ylabel('요일', fontsize=12)

    plt.tight_layout()

    # 저장
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/02_upload_timing_{category}.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 분석 결과 반환
    results = {
        'best_day': day_mapping.get(day_views.idxmax(), day_views.idxmax()),
        'worst_day': day_mapping.get(day_views.idxmin(), day_views.idxmin()),
        'best_hour': hour_views.idxmax(),
        'worst_hour': hour_views.idxmin(),
        'day_views': day_views.to_dict(),
        'hour_views': hour_views.to_dict()
    }

    return results

def analyze_upload_timing_summary(df, save_path="visualizations"):
    """
    모든 카테고리의 업로드 타이밍 요약 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    save_path (str): 저장할 경로
    """
    categories = df['카테고리'].unique()
    results = {}

    # 각 카테고리별 분석
    for category in categories:
        print(f"Processing upload timing analysis for category: {category}")
        try:
            category_results = analyze_upload_timing_by_category(df, category, save_path)
            results[category] = category_results
        except Exception as e:
            print(f"Error processing {category}: {str(e)}")
            continue

    # 전체 요약 시각화
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 카테고리별 최적 요일 분포
    ax1 = axes[0, 0]
    best_days = [results[cat]['best_day'] for cat in results.keys() if 'best_day' in results[cat]]
    day_counts = pd.Series(best_days).value_counts()

    ax1.pie(day_counts.values, labels=day_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('카테고리별 최적 업로드 요일 분포', fontsize=14, weight='bold')

    # 카테고리별 최적 시간대 분포
    ax2 = axes[0, 1]
    best_hours = [results[cat]['best_hour'] for cat in results.keys() if 'best_hour' in results[cat]]
    hour_counts = pd.Series(best_hours).value_counts().sort_index()

    ax2.bar(hour_counts.index, hour_counts.values, color='orange', alpha=0.7)
    ax2.set_title('카테고리별 최적 업로드 시간대 분포', fontsize=14, weight='bold')
    ax2.set_xlabel('시간대', fontsize=12)
    ax2.set_ylabel('카테고리 수', fontsize=12)

    # 카테고리별 요일 성과 비교
    ax3 = axes[1, 0]
    category_names = list(results.keys())
    best_day_names = [results[cat]['best_day'] for cat in category_names if 'best_day' in results[cat]]

    colors = plt.cm.Set3(np.linspace(0, 1, len(category_names)))
    ax3.barh(category_names, range(len(category_names)), color=colors, alpha=0.7)

    for i, day in enumerate(best_day_names):
        if i < len(category_names):
            ax3.text(0.5, i, day, ha='center', va='center', fontsize=10, weight='bold')

    ax3.set_title('카테고리별 최적 업로드 요일', fontsize=14, weight='bold')
    ax3.set_xlabel('카테고리', fontsize=12)

    # 카테고리별 시간대 성과 비교
    ax4 = axes[1, 1]
    best_hour_names = [f"{results[cat]['best_hour']}시" for cat in category_names if 'best_hour' in results[cat]]

    ax4.barh(category_names, range(len(category_names)), color=colors, alpha=0.7)

    for i, hour in enumerate(best_hour_names):
        if i < len(category_names):
            ax4.text(0.5, i, hour, ha='center', va='center', fontsize=10, weight='bold')

    ax4.set_title('카테고리별 최적 업로드 시간대', fontsize=14, weight='bold')
    ax4.set_xlabel('카테고리', fontsize=12)

    plt.tight_layout()

    # 저장
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/02_upload_timing_summary.png', dpi=300, bbox_inches='tight')
    plt.show()

    return results

if __name__ == "__main__":
    # 실행 예시
    setup_matplotlib()

    # 데이터 로드
    df = load_and_preprocess_data()

    # 전체 분석 실행
    results = analyze_upload_timing_summary(df)

    # 결과 출력
    print("\n=== 카테고리별 최적 업로드 타이밍 ===")
    for category, result in results.items():
        if 'best_day' in result and 'best_hour' in result:
            print(f"{category}: {result['best_day']} {result['best_hour']}시")

    print("\n업로드 타이밍 분석이 완료되었습니다!")
    print("결과는 visualizations/ 폴더에 저장되었습니다.")