#!/usr/bin/env python3
"""
YouTube Channel Analysis Project - Main Entry Point

이 스크립트는 YouTube 채널 분석 프로젝트의 메인 실행 파일입니다.
데이터 수집, 분석, 시각화를 통합적으로 수행할 수 있습니다.

Usage:
    python main.py --mode [collect|analyze|visualize|all]
    python main.py --help

Example:
    python main.py --mode all --channel-id UCuTITJp_8VXjjthWdPdmwKA
"""

import argparse
import os
import sys
from pathlib import Path

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.data_collection.youtube_api import YouTubeDataCollector
    from src.analysis.channel_analyzer import ChannelAnalyzer
    from src.visualization.charts import YouTubeVisualizer
    from config.config import Config
except ImportError as e:
    print(f"모듈 import 오류: {e}")
    print("필요한 패키지를 설치하고 프로젝트 구조를 확인해주세요.")
    sys.exit(1)


def collect_data(api_key: str, channel_ids: list, max_videos: int = 100):
    """
    YouTube 데이터 수집

    Args:
        api_key (str): YouTube API 키
        channel_ids (list): 분석할 채널 ID 목록
        max_videos (int): 채널당 수집할 최대 영상 수
    """
    print("📊 YouTube 데이터 수집 시작...")

    collector = YouTubeDataCollector(api_key)
    Config.create_directories()

    for channel_id in channel_ids:
        try:
            print(f"채널 {channel_id} 데이터 수집 중...")
            data = collector.collect_channel_data(channel_id, max_videos)
            collector.save_data_to_csv(data, Config.RAW_DATA_DIR)
            print(f"✅ 채널 {channel_id} 데이터 수집 완료!")
        except Exception as e:
            print(f"❌ 채널 {channel_id} 데이터 수집 실패: {e}")


def analyze_data(data_directory: str):
    """
    수집된 데이터 분석

    Args:
        data_directory (str): 데이터가 저장된 디렉토리 경로
    """
    print("🔍 데이터 분석 시작...")

    # 데이터 디렉토리에서 CSV 파일들 찾기
    data_path = Path(data_directory)
    channel_files = list(data_path.glob("*_channel_info.csv"))
    video_files = list(data_path.glob("*_videos.csv"))

    if not channel_files or not video_files:
        print("❌ 분석할 데이터 파일을 찾을 수 없습니다.")
        print(f"다음 위치에 *_channel_info.csv와 *_videos.csv 파일이 있는지 확인하세요: {data_directory}")
        return

    for channel_file in channel_files:
        # 대응하는 비디오 파일 찾기
        base_name = channel_file.stem.replace('_channel_info', '')
        video_file = data_path / f"{base_name}_videos.csv"

        if video_file.exists():
            try:
                print(f"\n📈 {base_name} 채널 분석 중...")

                analyzer = ChannelAnalyzer(str(channel_file), str(video_file))

                # 채널 요약
                print("\n=== 채널 요약 ===")
                summary = analyzer.get_channel_summary()
                for key, value in summary.items():
                    print(f"{key}: {value:,}" if isinstance(value, int) else f"{key}: {value}")

                # 비디오 성과 통계
                print("\n=== 비디오 성과 통계 ===")
                performance = analyzer.get_video_performance_stats()
                for key, value in performance.items():
                    if isinstance(value, float):
                        print(f"{key}: {value:,.1f}")
                    else:
                        print(f"{key}: {value:,}" if isinstance(value, int) else f"{key}: {value}")

                # 상위 비디오
                print("\n=== 상위 조회수 비디오 (Top 5) ===")
                top_videos = analyzer.get_top_performing_videos(n=5)
                for idx, row in top_videos.iterrows():
                    print(f"• {row['snippet.title'][:50]}... - {row['statistics.viewCount']:,} views")

                # 인사이트
                print("\n=== 주요 인사이트 ===")
                insights = analyzer.generate_insights()
                for insight in insights:
                    print(f"💡 {insight}")

                print(f"\n✅ {base_name} 채널 분석 완료!")

            except Exception as e:
                print(f"❌ {base_name} 채널 분석 실패: {e}")


def create_visualizations(data_directory: str, output_directory: str):
    """
    데이터 시각화

    Args:
        data_directory (str): 데이터가 저장된 디렉토리 경로
        output_directory (str): 시각화 결과를 저장할 디렉토리 경로
    """
    print("📊 데이터 시각화 시작...")

    data_path = Path(data_directory)
    video_files = list(data_path.glob("*_videos.csv"))

    if not video_files:
        print("❌ 시각화할 비디오 데이터 파일을 찾을 수 없습니다.")
        return

    visualizer = YouTubeVisualizer()

    for video_file in video_files:
        try:
            base_name = video_file.stem.replace('_videos', '')
            print(f"📊 {base_name} 채널 시각화 중...")

            import pandas as pd
            videos_df = pd.read_csv(video_file)

            # 채널별 출력 디렉토리 생성
            channel_output_dir = Path(output_directory) / base_name
            channel_output_dir.mkdir(parents=True, exist_ok=True)

            # 모든 차트 생성 및 저장
            visualizer.save_all_charts(videos_df, str(channel_output_dir))

            print(f"✅ {base_name} 채널 시각화 완료!")

        except Exception as e:
            print(f"❌ {video_file.name} 시각화 실패: {e}")


def main():
    """
    메인 함수
    """
    parser = argparse.ArgumentParser(
        description="YouTube Channel Analysis Project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시 사용법:
  python main.py --mode collect --channel-id UCuTITJp_8VXjjthWdPdmwKA
  python main.py --mode analyze
  python main.py --mode visualize
  python main.py --mode all --channel-id UCuTITJp_8VXjjthWdPdmwKA --max-videos 50
        """
    )

    parser.add_argument(
        '--mode',
        choices=['collect', 'analyze', 'visualize', 'all'],
        default='all',
        help='실행할 모드 선택 (기본값: all)'
    )

    parser.add_argument(
        '--channel-id',
        action='append',
        help='분석할 YouTube 채널 ID (여러 개 지정 가능)'
    )

    parser.add_argument(
        '--max-videos',
        type=int,
        default=100,
        help='채널당 수집할 최대 영상 수 (기본값: 100)'
    )

    parser.add_argument(
        '--data-dir',
        default='data/raw',
        help='데이터 디렉토리 경로 (기본값: data/raw)'
    )

    parser.add_argument(
        '--output-dir',
        default='visualizations',
        help='시각화 결과 출력 디렉토리 (기본값: visualizations)'
    )

    args = parser.parse_args()

    print("🚀 YouTube Channel Analysis Project")
    print("=" * 50)

    # 데이터 수집
    if args.mode in ['collect', 'all']:
        try:
            api_key = Config.get_api_key()
            channel_ids = args.channel_id or []

            if not channel_ids:
                # 기본 샘플 채널 사용
                channel_ids = Config.SAMPLE_CHANNELS.get('tech', [])
                if channel_ids:
                    print(f"⚠️  채널 ID가 지정되지 않아 샘플 채널을 사용합니다: {channel_ids}")
                else:
                    print("⚠️  채널 ID를 지정하세요: --channel-id YOUR_CHANNEL_ID")
                    return

            collect_data(api_key, channel_ids, args.max_videos)

        except ValueError as e:
            print(f"❌ API 키 오류: {e}")
            if args.mode == 'all':
                print("데이터 수집을 건너뛰고 분석을 계속합니다...")
            else:
                return

    # 데이터 분석
    if args.mode in ['analyze', 'all']:
        analyze_data(args.data_dir)

    # 데이터 시각화
    if args.mode in ['visualize', 'all']:
        create_visualizations(args.data_dir, args.output_dir)

    print("\n🎉 모든 작업이 완료되었습니다!")
    print(f"📁 데이터: {args.data_dir}")
    print(f"📊 시각화: {args.output_dir}")


if __name__ == "__main__":
    main()