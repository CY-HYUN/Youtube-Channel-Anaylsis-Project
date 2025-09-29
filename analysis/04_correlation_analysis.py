"""
4. 각 분야별 - 채널별 조회수와 좋아요수 & 조회수와 댓글수의 상관관계
조회수와 좋아요수 & 조회수와 댓글수는 양의 상관관계 분석
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from scipy.stats import pearsonr, spearmanr
from data_preprocessing import load_and_preprocess_data, filter_by_category, get_top_channels_by_category, setup_matplotlib, format_numbers
from matplotlib.ticker import FuncFormatter

def calculate_correlation_metrics(df, x_col, y_col):
    """
    두 변수 간의 상관관계 지표를 계산합니다.

    Parameters:
    df (pd.DataFrame): 데이터프레임
    x_col (str): X축 변수 컬럼명
    y_col (str): Y축 변수 컬럼명

    Returns:
    dict: 상관관계 지표
    """
    # 유효한 데이터만 필터링
    valid_data = df[[x_col, y_col]].dropna()

    if len(valid_data) < 2:
        return {}

    # 피어슨 상관계수
    pearson_corr, pearson_p = pearsonr(valid_data[x_col], valid_data[y_col])

    # 스피어만 상관계수
    spearman_corr, spearman_p = spearmanr(valid_data[x_col], valid_data[y_col])

    # R² 계산
    r_squared = pearson_corr ** 2

    return {
        'pearson_correlation': pearson_corr,
        'pearson_p_value': pearson_p,
        'spearman_correlation': spearman_corr,
        'spearman_p_value': spearman_p,
        'r_squared': r_squared,
        'sample_size': len(valid_data)
    }

def analyze_correlation_by_category(df, category, save_path="visualizations"):
    """
    특정 카테고리의 상관관계 분석을 수행합니다.

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
    required_cols = ['조회수', '좋아요 수', '댓글 수']
    missing_cols = [col for col in required_cols if col not in category_df.columns]
    if missing_cols:
        print(f"Missing columns for {category}: {missing_cols}")
        return

    # 상관관계 계산
    views_likes_corr = calculate_correlation_metrics(category_df, '조회수', '좋아요 수')
    views_comments_corr = calculate_correlation_metrics(category_df, '조회수', '댓글 수')
    likes_comments_corr = calculate_correlation_metrics(category_df, '좋아요 수', '댓글 수')

    # 시각화
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    # 1. 조회수 vs 좋아요 수 산점도
    ax1 = axes[0, 0]
    valid_data = category_df[['조회수', '좋아요 수']].dropna()

    if not valid_data.empty:
        ax1.scatter(valid_data['조회수'], valid_data['좋아요 수'], alpha=0.6, color='blue')
        ax1.set_title(f'{category} - 조회수 vs 좋아요 수', fontsize=14, weight='bold')
        ax1.set_xlabel('조회수', fontsize=12)
        ax1.set_ylabel('좋아요 수', fontsize=12)

        # 상관계수 표시
        if views_likes_corr:
            corr_text = f"Pearson r = {views_likes_corr['pearson_correlation']:.3f}\n"
            corr_text += f"R² = {views_likes_corr['r_squared']:.3f}\n"
            corr_text += f"p-value = {views_likes_corr['pearson_p_value']:.3e}"
            ax1.text(0.05, 0.95, corr_text, transform=ax1.transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # 추세선 추가
        if len(valid_data) > 1:
            z = np.polyfit(valid_data['조회수'], valid_data['좋아요 수'], 1)
            p = np.poly1d(z)
            ax1.plot(valid_data['조회수'], p(valid_data['조회수']), "r--", alpha=0.8)

        ax1.xaxis.set_major_formatter(FuncFormatter(format_numbers))
        ax1.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 2. 조회수 vs 댓글 수 산점도
    ax2 = axes[0, 1]
    valid_data = category_df[['조회수', '댓글 수']].dropna()

    if not valid_data.empty:
        ax2.scatter(valid_data['조회수'], valid_data['댓글 수'], alpha=0.6, color='green')
        ax2.set_title(f'{category} - 조회수 vs 댓글 수', fontsize=14, weight='bold')
        ax2.set_xlabel('조회수', fontsize=12)
        ax2.set_ylabel('댓글 수', fontsize=12)

        # 상관계수 표시
        if views_comments_corr:
            corr_text = f"Pearson r = {views_comments_corr['pearson_correlation']:.3f}\n"
            corr_text += f"R² = {views_comments_corr['r_squared']:.3f}\n"
            corr_text += f"p-value = {views_comments_corr['pearson_p_value']:.3e}"
            ax2.text(0.05, 0.95, corr_text, transform=ax2.transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # 추세선 추가
        if len(valid_data) > 1:
            z = np.polyfit(valid_data['조회수'], valid_data['댓글 수'], 1)
            p = np.poly1d(z)
            ax2.plot(valid_data['조회수'], p(valid_data['조회수']), "r--", alpha=0.8)

        ax2.xaxis.set_major_formatter(FuncFormatter(format_numbers))
        ax2.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 3. 좋아요 수 vs 댓글 수 산점도
    ax3 = axes[0, 2]
    valid_data = category_df[['좋아요 수', '댓글 수']].dropna()

    if not valid_data.empty:
        ax3.scatter(valid_data['좋아요 수'], valid_data['댓글 수'], alpha=0.6, color='orange')
        ax3.set_title(f'{category} - 좋아요 수 vs 댓글 수', fontsize=14, weight='bold')
        ax3.set_xlabel('좋아요 수', fontsize=12)
        ax3.set_ylabel('댓글 수', fontsize=12)

        # 상관계수 표시
        if likes_comments_corr:
            corr_text = f"Pearson r = {likes_comments_corr['pearson_correlation']:.3f}\n"
            corr_text += f"R² = {likes_comments_corr['r_squared']:.3f}\n"
            corr_text += f"p-value = {likes_comments_corr['pearson_p_value']:.3e}"
            ax3.text(0.05, 0.95, corr_text, transform=ax3.transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # 추세선 추가
        if len(valid_data) > 1:
            z = np.polyfit(valid_data['좋아요 수'], valid_data['댓글 수'], 1)
            p = np.poly1d(z)
            ax3.plot(valid_data['좋아요 수'], p(valid_data['좋아요 수']), "r--", alpha=0.8)

        ax3.xaxis.set_major_formatter(FuncFormatter(format_numbers))
        ax3.yaxis.set_major_formatter(FuncFormatter(format_numbers))

    # 4. 상관관계 히트맵
    ax4 = axes[1, 0]
    correlation_matrix = category_df[['조회수', '좋아요 수', '댓글 수']].corr()

    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, cbar_kws={'label': '상관계수'}, ax=ax4)
    ax4.set_title(f'{category} - 상관관계 히트맵', fontsize=14, weight='bold')

    # 5. 채널별 상관관계 비교
    ax5 = axes[1, 1]
    top_channels = get_top_channels_by_category(df, category, top_n=5)

    if top_channels:
        channel_correlations = []
        channel_names = []

        for channel in top_channels:
            channel_df = category_df[category_df['채널명'] == channel]
            if len(channel_df) > 2:  # 최소 3개 이상의 데이터가 있어야 상관관계 계산 가능
                corr_metrics = calculate_correlation_metrics(channel_df, '조회수', '좋아요 수')
                if corr_metrics:
                    channel_correlations.append(corr_metrics['pearson_correlation'])
                    channel_names.append(channel[:15] + '...' if len(channel) > 15 else channel)

        if channel_correlations:
            bars = ax5.bar(range(len(channel_names)), channel_correlations,
                          color=['red' if x < 0.5 else 'green' for x in channel_correlations], alpha=0.7)
            ax5.set_title(f'{category} - 채널별 조회수-좋아요 상관관계', fontsize=14, weight='bold')
            ax5.set_xlabel('채널', fontsize=12)
            ax5.set_ylabel('상관계수', fontsize=12)
            ax5.set_xticks(range(len(channel_names)))
            ax5.set_xticklabels(channel_names, rotation=45)
            ax5.axhline(y=0.7, color='red', linestyle='--', alpha=0.7, label='강한 상관관계 (0.7)')
            ax5.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='중간 상관관계 (0.5)')
            ax5.legend()

            # 막대 위에 값 표시
            for bar, value in zip(bars, channel_correlations):
                ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{value:.3f}', ha='center', va='bottom', fontsize=10)

    # 6. 참여도 지표 분석 (좋아요율, 댓글율)
    ax6 = axes[1, 2]

    # 참여도 지표 계산
    category_df_copy = category_df.copy()
    category_df_copy['좋아요율'] = (category_df_copy['좋아요 수'] / category_df_copy['조회수'] * 100).fillna(0)
    category_df_copy['댓글율'] = (category_df_copy['댓글 수'] / category_df_copy['조회수'] * 100).fillna(0)

    # 유효한 데이터만 필터링 (이상치 제거)
    valid_engagement = category_df_copy[
        (category_df_copy['좋아요율'] <= 50) & (category_df_copy['댓글율'] <= 10)  # 현실적인 범위로 제한
    ]

    if not valid_engagement.empty:
        ax6.scatter(valid_engagement['좋아요율'], valid_engagement['댓글율'], alpha=0.6, color='purple')
        ax6.set_title(f'{category} - 좋아요율 vs 댓글율', fontsize=14, weight='bold')
        ax6.set_xlabel('좋아요율 (%)', fontsize=12)
        ax6.set_ylabel('댓글율 (%)', fontsize=12)

        # 평균선 표시
        mean_like_rate = valid_engagement['좋아요율'].mean()
        mean_comment_rate = valid_engagement['댓글율'].mean()
        ax6.axvline(x=mean_like_rate, color='red', linestyle='--', alpha=0.7, label=f'평균 좋아요율: {mean_like_rate:.2f}%')
        ax6.axhline(y=mean_comment_rate, color='blue', linestyle='--', alpha=0.7, label=f'평균 댓글율: {mean_comment_rate:.2f}%')
        ax6.legend()

    plt.tight_layout()

    # 저장
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/04_correlation_{category}.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 결과 반환
    results = {
        'views_likes_correlation': views_likes_corr,
        'views_comments_correlation': views_comments_corr,
        'likes_comments_correlation': likes_comments_corr,
        'correlation_matrix': correlation_matrix.to_dict()
    }

    return results

def analyze_all_categories_correlation(df, save_path="visualizations"):
    """
    모든 카테고리의 상관관계 분석을 수행합니다.

    Parameters:
    df (pd.DataFrame): 전체 데이터프레임
    save_path (str): 저장할 경로
    """
    categories = df['카테고리'].unique()
    results = {}

    # 각 카테고리별 분석
    for category in categories:
        print(f"Processing correlation analysis for category: {category}")
        try:
            category_results = analyze_correlation_by_category(df, category, save_path)
            results[category] = category_results
        except Exception as e:
            print(f"Error processing {category}: {str(e)}")
            continue

    # 전체 요약 시각화
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 카테고리별 조회수-좋아요 상관계수 비교
    ax1 = axes[0, 0]
    categories_list = []
    views_likes_corrs = []

    for category, result in results.items():
        if 'views_likes_correlation' in result and result['views_likes_correlation']:
            categories_list.append(category)
            views_likes_corrs.append(result['views_likes_correlation']['pearson_correlation'])

    if categories_list:
        bars1 = ax1.bar(range(len(categories_list)), views_likes_corrs,
                       color=['red' if x < 0.5 else 'orange' if x < 0.7 else 'green' for x in views_likes_corrs],
                       alpha=0.7)
        ax1.set_title('카테고리별 조회수-좋아요 상관관계', fontsize=14, weight='bold')
        ax1.set_xlabel('카테고리', fontsize=12)
        ax1.set_ylabel('상관계수', fontsize=12)
        ax1.set_xticks(range(len(categories_list)))
        ax1.set_xticklabels(categories_list, rotation=45)
        ax1.axhline(y=0.7, color='red', linestyle='--', alpha=0.7, label='강한 상관관계')
        ax1.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='중간 상관관계')
        ax1.legend()

        # 막대 위에 값 표시
        for bar, value in zip(bars1, views_likes_corrs):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.3f}', ha='center', va='bottom', fontsize=10)

    # 카테고리별 조회수-댓글 상관계수 비교
    ax2 = axes[0, 1]
    views_comments_corrs = []

    for category in categories_list:
        if category in results and 'views_comments_correlation' in results[category] and results[category]['views_comments_correlation']:
            views_comments_corrs.append(results[category]['views_comments_correlation']['pearson_correlation'])
        else:
            views_comments_corrs.append(0)

    if views_comments_corrs:
        bars2 = ax2.bar(range(len(categories_list)), views_comments_corrs,
                       color=['red' if x < 0.5 else 'orange' if x < 0.7 else 'green' for x in views_comments_corrs],
                       alpha=0.7)
        ax2.set_title('카테고리별 조회수-댓글 상관관계', fontsize=14, weight='bold')
        ax2.set_xlabel('카테고리', fontsize=12)
        ax2.set_ylabel('상관계수', fontsize=12)
        ax2.set_xticks(range(len(categories_list)))
        ax2.set_xticklabels(categories_list, rotation=45)
        ax2.axhline(y=0.7, color='red', linestyle='--', alpha=0.7)
        ax2.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7)

    # 상관관계 강도 분포
    ax3 = axes[1, 0]
    all_correlations = views_likes_corrs + views_comments_corrs
    if all_correlations:
        correlation_ranges = ['약함 (0-0.3)', '중간 (0.3-0.7)', '강함 (0.7-1.0)']
        weak = len([c for c in all_correlations if 0 <= c < 0.3])
        medium = len([c for c in all_correlations if 0.3 <= c < 0.7])
        strong = len([c for c in all_correlations if 0.7 <= c <= 1.0])

        sizes = [weak, medium, strong]
        colors = ['red', 'orange', 'green']

        ax3.pie(sizes, labels=correlation_ranges, colors=colors, autopct='%1.1f%%', startangle=90)
        ax3.set_title('상관관계 강도 분포', fontsize=14, weight='bold')

    # 평균 상관계수 비교
    ax4 = axes[1, 1]
    if categories_list:
        avg_views_likes = np.mean(views_likes_corrs) if views_likes_corrs else 0
        avg_views_comments = np.mean(views_comments_corrs) if views_comments_corrs else 0

        metrics = ['조회수-좋아요', '조회수-댓글']
        values = [avg_views_likes, avg_views_comments]

        bars4 = ax4.bar(metrics, values, color=['blue', 'green'], alpha=0.7)
        ax4.set_title('평균 상관관계 비교', fontsize=14, weight='bold')
        ax4.set_ylabel('평균 상관계수', fontsize=12)

        # 막대 위에 값 표시
        for bar, value in zip(bars4, values):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.3f}', ha='center', va='bottom', fontsize=12, weight='bold')

    plt.tight_layout()

    # 저장
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/04_correlation_summary.png', dpi=300, bbox_inches='tight')
    plt.show()

    return results

if __name__ == "__main__":
    # 실행 예시
    setup_matplotlib()

    # 데이터 로드
    df = load_and_preprocess_data()

    # 전체 분석 실행
    results = analyze_all_categories_correlation(df)

    # 결과 출력
    print("\n=== 카테고리별 상관관계 분석 결과 ===")
    for category, result in results.items():
        if 'views_likes_correlation' in result and result['views_likes_correlation']:
            vl_corr = result['views_likes_correlation']['pearson_correlation']
            vc_corr = result['views_comments_correlation']['pearson_correlation'] if 'views_comments_correlation' in result and result['views_comments_correlation'] else 0
            print(f"{category}: 조회수-좋아요 {vl_corr:.3f}, 조회수-댓글 {vc_corr:.3f}")

    print("\n상관관계 분석이 완료되었습니다!")
    print("결과는 visualizations/ 폴더에 저장되었습니다.")