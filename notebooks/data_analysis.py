#!/usr/bin/env python3
"""
YouTube Channel Data Analysis Script

이 스크립트는 Jupyter 노트북의 핵심 분석 로직을
독립적으로 실행할 수 있도록 추출한 것입니다.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class YouTubeChannelAnalysis:
    """YouTube 채널 데이터 분석을 위한 클래스"""

    def __init__(self, data_path=None):
        """
        초기화

        Args:
            data_path (str): 데이터 파일 경로
        """
        self.data_path = data_path
        self.df = None

    def load_data(self, file_path=None):
        """데이터 로드"""
        path = file_path or self.data_path
        if path:
            if path.endswith('.csv'):
                self.df = pd.read_csv(path)
            elif path.endswith('.json'):
                self.df = pd.read_json(path)
            print(f"✅ 데이터 로드 완료: {len(self.df)} rows, {len(self.df.columns)} columns")
        else:
            print("❌ 데이터 파일 경로를 지정해주세요.")

    def basic_statistics(self):
        """기본 통계 정보"""
        if self.df is None:
            print("❌ 먼저 데이터를 로드해주세요.")
            return

        print("\n=== 기본 통계 정보 ===")
        print(f"📊 데이터셋 크기: {self.df.shape}")
        print(f"📈 수치형 컬럼: {len(self.df.select_dtypes(include=[np.number]).columns)}개")
        print(f"📝 텍스트 컬럼: {len(self.df.select_dtypes(include=['object']).columns)}개")

        # 결측치 정보
        missing = self.df.isnull().sum()
        if missing.any():
            print("\n📋 결측치 현황:")
            for col, count in missing[missing > 0].items():
                print(f"  • {col}: {count}개 ({count/len(self.df)*100:.1f}%)")
        else:
            print("\n✅ 결측치 없음")

    def visualize_data(self, save_path=None):
        """데이터 시각화"""
        if self.df is None:
            print("❌ 먼저 데이터를 로드해주세요.")
            return

        # 수치형 컬럼만 선택
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns

        if len(numeric_columns) == 0:
            print("❌ 시각화할 수치형 데이터가 없습니다.")
            return

        # 상관관계 히트맵
        plt.figure(figsize=(12, 8))
        correlation_matrix = self.df[numeric_columns].corr()

        sns.heatmap(correlation_matrix,
                   annot=True,
                   cmap='coolwarm',
                   center=0,
                   square=True,
                   fmt='.2f')
        plt.title('📊 변수 간 상관관계 히트맵')
        plt.tight_layout()

        if save_path:
            plt.savefig(f"{save_path}/correlation_heatmap.png", dpi=300)
        plt.show()

        # 수치형 변수 분포
        n_cols = min(4, len(numeric_columns))
        n_rows = (len(numeric_columns) + n_cols - 1) // n_cols

        plt.figure(figsize=(15, 4 * n_rows))
        for i, col in enumerate(numeric_columns):
            plt.subplot(n_rows, n_cols, i + 1)
            self.df[col].hist(bins=30, alpha=0.7, color='skyblue')
            plt.title(f'{col} 분포')
            plt.xlabel(col)
            plt.ylabel('빈도')

        plt.tight_layout()
        if save_path:
            plt.savefig(f"{save_path}/distributions.png", dpi=300)
        plt.show()

    def generate_insights(self):
        """데이터 인사이트 생성"""
        if self.df is None:
            print("❌ 먼저 데이터를 로드해주세요.")
            return

        insights = []

        # 기본 정보
        insights.append(f"📊 총 {len(self.df):,}개의 데이터 포인트를 분석했습니다.")

        # 수치형 데이터 분석
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            insights.append(f"🔢 {len(numeric_columns)}개의 수치형 변수를 발견했습니다.")

            # 각 수치형 컬럼의 특성 분석
            for col in numeric_columns:
                stats = self.df[col].describe()
                if stats['std'] > 0:  # 변동이 있는 데이터만
                    cv = stats['std'] / stats['mean'] if stats['mean'] != 0 else 0
                    if cv > 1:
                        insights.append(f"📈 {col}은(는) 높은 변동성을 보입니다 (CV: {cv:.2f})")

        # 결측치 분석
        missing_cols = self.df.columns[self.df.isnull().any()].tolist()
        if missing_cols:
            insights.append(f"⚠️ {len(missing_cols)}개 컬럼에서 결측치가 발견되었습니다: {', '.join(missing_cols[:3])}")

        return insights

    def export_results(self, output_path="analysis_results.csv"):
        """분석 결과 내보내기"""
        if self.df is None:
            print("❌ 먼저 데이터를 로드해주세요.")
            return

        # 기본 통계 요약
        summary_stats = self.df.describe()
        summary_stats.to_csv(output_path.replace('.csv', '_summary.csv'))

        print(f"✅ 분석 결과가 {output_path}로 저장되었습니다.")


def main():
    """메인 실행 함수"""
    print("🎬 YouTube Channel Data Analysis")
    print("=" * 50)

    # 분석 객체 생성
    analyzer = YouTubeChannelAnalysis()

    # 샘플 데이터 경로 (실제 경로로 변경)
    data_path = "data/raw/sample_data.csv"  # 실제 데이터 파일 경로로 변경

    # 데이터 로드 시도
    try:
        analyzer.load_data(data_path)

        # 기본 통계 분석
        analyzer.basic_statistics()

        # 시각화
        analyzer.visualize_data("visualizations")

        # 인사이트 생성
        insights = analyzer.generate_insights()
        print("\n=== 🔍 주요 인사이트 ===")
        for insight in insights:
            print(f"💡 {insight}")

        # 결과 내보내기
        analyzer.export_results()

    except FileNotFoundError:
        print(f"❌ 데이터 파일을 찾을 수 없습니다: {data_path}")
        print("📝 다음 중 하나를 수행하세요:")
        print("1. 올바른 데이터 파일 경로를 지정")
        print("2. main.py를 사용하여 데이터 수집 먼저 실행")
        print("3. Jupyter 노트북에서 분석 수행")


if __name__ == "__main__":
    main()