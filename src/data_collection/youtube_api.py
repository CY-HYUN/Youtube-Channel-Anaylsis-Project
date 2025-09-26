import os
import requests
import pandas as pd
from typing import Dict, List, Optional
import json
import time


class YouTubeDataCollector:
    """
    YouTube API를 사용하여 채널 및 영상 데이터를 수집하는 클래스
    """

    def __init__(self, api_key: str):
        """
        YouTube API 키로 초기화

        Args:
            api_key (str): YouTube Data API v3 키
        """
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    def get_channel_info(self, channel_id: str) -> Dict:
        """
        채널 기본 정보 조회

        Args:
            channel_id (str): 채널 ID

        Returns:
            Dict: 채널 정보
        """
        url = f"{self.base_url}/channels"
        params = {
            'part': 'snippet,statistics,brandingSettings',
            'id': channel_id,
            'key': self.api_key
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API 요청 실패: {response.status_code}")

    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> List[Dict]:
        """
        채널의 동영상 목록 조회

        Args:
            channel_id (str): 채널 ID
            max_results (int): 최대 결과 개수

        Returns:
            List[Dict]: 동영상 목록
        """
        # 채널의 업로드 플레이리스트 ID 가져오기
        channel_info = self.get_channel_info(channel_id)
        uploads_playlist_id = channel_info['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # 플레이리스트의 동영상 목록 가져오기
        url = f"{self.base_url}/playlistItems"
        params = {
            'part': 'snippet,contentDetails',
            'playlistId': uploads_playlist_id,
            'maxResults': max_results,
            'key': self.api_key
        }

        videos = []
        next_page_token = None

        while len(videos) < max_results:
            if next_page_token:
                params['pageToken'] = next_page_token

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                videos.extend(data.get('items', []))

                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    break

                time.sleep(0.1)  # API 호출 제한 방지
            else:
                raise Exception(f"API 요청 실패: {response.status_code}")

        return videos[:max_results]

    def get_video_details(self, video_ids: List[str]) -> List[Dict]:
        """
        동영상 상세 정보 조회

        Args:
            video_ids (List[str]): 동영상 ID 목록

        Returns:
            List[Dict]: 동영상 상세 정보 목록
        """
        url = f"{self.base_url}/videos"

        # API는 한 번에 최대 50개까지만 조회 가능
        batch_size = 50
        all_videos = []

        for i in range(0, len(video_ids), batch_size):
            batch_ids = video_ids[i:i + batch_size]

            params = {
                'part': 'snippet,statistics,contentDetails',
                'id': ','.join(batch_ids),
                'key': self.api_key
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                all_videos.extend(data.get('items', []))
                time.sleep(0.1)  # API 호출 제한 방지
            else:
                raise Exception(f"API 요청 실패: {response.status_code}")

        return all_videos

    def collect_channel_data(self, channel_id: str, max_videos: int = 100) -> Dict:
        """
        채널의 모든 데이터 수집

        Args:
            channel_id (str): 채널 ID
            max_videos (int): 수집할 최대 동영상 개수

        Returns:
            Dict: 채널 정보와 동영상 데이터
        """
        # 채널 정보 수집
        channel_info = self.get_channel_info(channel_id)

        # 동영상 목록 수집
        videos = self.get_channel_videos(channel_id, max_videos)
        video_ids = [video['contentDetails']['videoId'] for video in videos]

        # 동영상 상세 정보 수집
        video_details = self.get_video_details(video_ids)

        return {
            'channel_info': channel_info,
            'video_details': video_details
        }

    def save_data_to_csv(self, data: Dict, output_dir: str = "data/raw"):
        """
        수집된 데이터를 CSV 파일로 저장

        Args:
            data (Dict): 수집된 데이터
            output_dir (str): 출력 디렉토리
        """
        os.makedirs(output_dir, exist_ok=True)

        channel_name = data['channel_info']['items'][0]['snippet']['title']
        safe_channel_name = "".join(c for c in channel_name if c.isalnum() or c in (' ', '-', '_')).rstrip()

        # 채널 정보 저장
        channel_df = pd.json_normalize(data['channel_info']['items'])
        channel_df.to_csv(f"{output_dir}/{safe_channel_name}_channel_info.csv", index=False, encoding='utf-8-sig')

        # 동영상 데이터 저장
        videos_df = pd.json_normalize(data['video_details'])
        videos_df.to_csv(f"{output_dir}/{safe_channel_name}_videos.csv", index=False, encoding='utf-8-sig')

        print(f"데이터가 {output_dir} 디렉토리에 저장되었습니다.")


def main():
    """
    메인 실행 함수
    """
    # API 키 설정 (환경변수에서 가져오기)
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("YouTube API 키가 설정되지 않았습니다.")
        print("환경변수 YOUTUBE_API_KEY를 설정하거나 config/api_keys.py 파일을 생성하세요.")
        return

    # 데이터 수집기 초기화
    collector = YouTubeDataCollector(api_key)

    # 예시 채널 ID (실제 사용시 변경 필요)
    channel_ids = [
        "UCuTITJp_8VXjjthWdPdmwKA",  # 예시 채널 ID
        # 추가 채널 ID들
    ]

    for channel_id in channel_ids:
        try:
            print(f"채널 {channel_id} 데이터 수집 중...")
            data = collector.collect_channel_data(channel_id, max_videos=100)
            collector.save_data_to_csv(data)
            print(f"채널 {channel_id} 데이터 수집 완료!")
        except Exception as e:
            print(f"채널 {channel_id} 데이터 수집 실패: {e}")


if __name__ == "__main__":
    main()