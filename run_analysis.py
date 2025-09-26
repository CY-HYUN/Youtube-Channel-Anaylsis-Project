#!/usr/bin/env python3
"""
YouTube Channel Analysis - 간편 실행 스크립트

이 스크립트는 전체 분석 파이프라인을 간편하게 실행할 수 있도록 합니다.
패키지 설치부터 분석 실행까지 자동화되어 있습니다.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """필요한 패키지 설치"""
    print("📦 필요한 패키지를 설치합니다...")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 패키지 설치 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 패키지 설치 실패: {e}")
        return False

def check_api_key():
    """API 키 확인"""
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("⚠️  YOUTUBE_API_KEY 환경변수가 설정되지 않았습니다.")
        print("\n📝 API 키 설정 방법:")
        print("Windows: set YOUTUBE_API_KEY=your_api_key_here")
        print("Linux/Mac: export YOUTUBE_API_KEY=your_api_key_here")
        print("\n🔗 API 키 발급: https://console.cloud.google.com/")
        return False
    return True

def run_analysis_mode():
    """분석 모드 실행"""
    print("\n🔍 사용 가능한 모드:")
    print("1. collect - 데이터 수집")
    print("2. analyze - 데이터 분석")
    print("3. visualize - 데이터 시각화")
    print("4. all - 전체 파이프라인 (권장)")
    print("5. demo - 데모 분석 (샘플 채널)")

    choice = input("\n실행할 모드를 선택하세요 (1-5): ").strip()

    mode_map = {
        '1': 'collect',
        '2': 'analyze',
        '3': 'visualize',
        '4': 'all',
        '5': 'demo'
    }

    mode = mode_map.get(choice)
    if not mode:
        print("❌ 잘못된 선택입니다.")
        return False

    if mode == 'demo':
        # 데모 모드 - 샘플 채널 분석
        sample_channels = [
            "UCuTITJp_8VXjjthWdPdmwKA",  # 샘플 채널 1
            "UC_x5XG1OV2P6uZZ5FSM9Ttw"   # 샘플 채널 2
        ]

        cmd = [
            sys.executable, "main.py",
            "--mode", "all",
            "--channel-id", sample_channels[0],
            "--max-videos", "20"
        ]
    else:
        if mode in ['collect', 'all']:
            channel_id = input("분석할 채널 ID를 입력하세요: ").strip()
            if not channel_id:
                print("❌ 채널 ID는 필수입니다.")
                return False

            cmd = [
                sys.executable, "main.py",
                "--mode", mode,
                "--channel-id", channel_id,
                "--max-videos", "50"
            ]
        else:
            cmd = [sys.executable, "main.py", "--mode", mode]

    try:
        print(f"\n🚀 {mode} 모드 실행 중...")
        subprocess.run(cmd, check=True)
        print("✅ 분석 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 분석 실행 실패: {e}")
        return False

def show_results():
    """결과 확인"""
    print("\n📊 생성된 결과물:")

    # 데이터 폴더 확인
    data_dir = Path("data/raw")
    if data_dir.exists():
        csv_files = list(data_dir.glob("*.csv"))
        if csv_files:
            print(f"  📄 데이터 파일: {len(csv_files)}개")
            for f in csv_files[:3]:
                print(f"    • {f.name}")
            if len(csv_files) > 3:
                print(f"    ... 및 {len(csv_files)-3}개 더")

    # 시각화 폴더 확인
    vis_dir = Path("visualizations")
    if vis_dir.exists():
        png_files = list(vis_dir.rglob("*.png"))
        if png_files:
            print(f"  🖼️  시각화 파일: {len(png_files)}개")
            for f in png_files[:3]:
                print(f"    • {f}")
            if len(png_files) > 3:
                print(f"    ... 및 {len(png_files)-3}개 더")

def main():
    """메인 실행 함수"""
    print("🎬 YouTube Channel Analysis - 간편 실행기")
    print("=" * 60)

    # 1. 패키지 설치
    if not install_requirements():
        return

    # 2. API 키 확인 (collect 모드가 아닌 경우 스킵 가능)
    print("\n🔑 API 키 확인 중...")
    has_api_key = check_api_key()

    # 3. 분석 실행
    if run_analysis_mode():
        # 4. 결과 표시
        show_results()

        print("\n🎉 분석이 완료되었습니다!")
        print("\n💡 다음 단계:")
        print("  • Jupyter 노트북으로 상세 분석: jupyter notebook Youtube_Channel_Anaylsis_Project.ipynb")
        print("  • 추가 분석: python notebooks/data_analysis.py")
        print("  • 결과 확인: data/raw/ 및 visualizations/ 폴더 확인")
    else:
        print("\n❌ 분석 실행 중 문제가 발생했습니다.")

if __name__ == "__main__":
    main()