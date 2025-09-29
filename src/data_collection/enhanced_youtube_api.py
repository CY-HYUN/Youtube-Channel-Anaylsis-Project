"""
Enhanced YouTube Data Collector with Enterprise-Grade Features

This module provides a robust, production-ready interface for collecting YouTube channel
and video data with comprehensive error handling, rate limiting, caching, and logging.
"""

import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Tuple
from urllib.parse import urlencode
import json
import os
from functools import wraps

import aiohttp
import pandas as pd
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from cachetools import TTLCache
import hashlib

# Configure structured logging
logger = structlog.get_logger(__name__)


@dataclass
class APIResponse:
    """Structured response container for API calls."""
    success: bool
    data: Optional[Dict] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    rate_limit_remaining: Optional[int] = None
    quota_cost: int = 1


@dataclass
class ChannelMetrics:
    """Structured container for channel performance metrics."""
    channel_id: str
    title: str
    subscriber_count: int
    video_count: int
    view_count: int
    custom_url: Optional[str]
    country: Optional[str]
    published_at: datetime
    thumbnail_url: Optional[str]
    description: str


@dataclass
class VideoMetrics:
    """Structured container for video performance metrics."""
    video_id: str
    title: str
    published_at: datetime
    duration: str
    view_count: int
    like_count: int
    comment_count: int
    tags: List[str]
    category_id: str
    thumbnail_url: str
    description: str


class YouTubeAPIError(Exception):
    """Custom exception for YouTube API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, quota_exceeded: bool = False):
        super().__init__(message)
        self.status_code = status_code
        self.quota_exceeded = quota_exceeded


class RateLimiter:
    """Intelligent rate limiter with exponential backoff."""

    def __init__(self, calls_per_second: float = 10.0, burst_capacity: int = 100):
        self.calls_per_second = calls_per_second
        self.burst_capacity = burst_capacity
        self.tokens = burst_capacity
        self.last_update = time.time()

    async def acquire(self) -> None:
        """Acquire permission to make an API call."""
        current_time = time.time()
        elapsed = current_time - self.last_update

        # Add tokens based on elapsed time
        self.tokens = min(
            self.burst_capacity,
            self.tokens + elapsed * self.calls_per_second
        )
        self.last_update = current_time

        if self.tokens < 1:
            wait_time = (1 - self.tokens) / self.calls_per_second
            logger.info("rate_limit_wait", wait_time=wait_time)
            await asyncio.sleep(wait_time)
            self.tokens = 0
        else:
            self.tokens -= 1


class EnhancedYouTubeDataCollector:
    """
    Enterprise-grade YouTube Data Collector with advanced features:
    - Async/await support for high performance
    - Intelligent rate limiting and quota management
    - Comprehensive error handling and retry logic
    - Multi-level caching with TTL
    - Structured logging and monitoring
    - Data validation and sanitization
    """

    BASE_URL = "https://www.googleapis.com/youtube/v3"
    DEFAULT_QUOTA_LIMIT = 10000  # Daily quota limit
    CACHE_TTL = 3600  # 1 hour cache TTL

    def __init__(
        self,
        api_key: str,
        quota_limit: int = DEFAULT_QUOTA_LIMIT,
        enable_caching: bool = True,
        cache_size: int = 1000
    ):
        """
        Initialize the YouTube Data Collector.

        Args:
            api_key: YouTube Data API v3 key
            quota_limit: Daily quota limit for API calls
            enable_caching: Whether to enable response caching
            cache_size: Maximum number of cached responses
        """
        self.api_key = api_key
        self.quota_limit = quota_limit
        self.quota_used = 0
        self.rate_limiter = RateLimiter()

        # Initialize caching
        if enable_caching:
            self.cache = TTLCache(maxsize=cache_size, ttl=self.CACHE_TTL)
        else:
            self.cache = None

        # Session for connection pooling
        self._session: Optional[aiohttp.ClientSession] = None

        logger.info(
            "youtube_collector_initialized",
            quota_limit=quota_limit,
            caching_enabled=enable_caching,
            cache_size=cache_size if enable_caching else 0
        )

    async def __aenter__(self):
        """Async context manager entry."""
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(limit=100, limit_per_host=10)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._session:
            await self._session.close()

    def _generate_cache_key(self, endpoint: str, params: Dict) -> str:
        """Generate a unique cache key for the request."""
        # Remove API key from cache key for security
        cache_params = {k: v for k, v in params.items() if k != 'key'}
        cache_string = f"{endpoint}:{json.dumps(cache_params, sort_keys=True)}"
        return hashlib.md5(cache_string.encode()).hexdigest()

    def _check_quota(self, cost: int) -> None:
        """Check if the request would exceed quota limits."""
        if self.quota_used + cost > self.quota_limit:
            raise YouTubeAPIError(
                f"Quota limit exceeded. Used: {self.quota_used}, Limit: {self.quota_limit}",
                quota_exceeded=True
            )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((aiohttp.ClientError, YouTubeAPIError))
    )
    async def _make_request(
        self,
        endpoint: str,
        params: Dict,
        quota_cost: int = 1
    ) -> APIResponse:
        """
        Make an authenticated request to the YouTube API.

        Args:
            endpoint: API endpoint (e.g., 'channels', 'videos')
            params: Request parameters
            quota_cost: Quota cost for this request

        Returns:
            APIResponse object with structured response data
        """
        # Check quota before making request
        self._check_quota(quota_cost)

        # Apply rate limiting
        await self.rate_limiter.acquire()

        # Check cache first
        cache_key = self._generate_cache_key(endpoint, params)
        if self.cache and cache_key in self.cache:
            logger.info("cache_hit", endpoint=endpoint, cache_key=cache_key[:8])
            return self.cache[cache_key]

        # Prepare request
        url = f"{self.BASE_URL}/{endpoint}"
        params['key'] = self.api_key

        start_time = time.time()

        try:
            async with self._session.get(url, params=params) as response:
                response_time = time.time() - start_time

                # Log request details
                logger.info(
                    "api_request",
                    endpoint=endpoint,
                    status_code=response.status,
                    response_time_ms=round(response_time * 1000, 2),
                    quota_cost=quota_cost
                )

                if response.status == 200:
                    data = await response.json()

                    # Update quota usage
                    self.quota_used += quota_cost

                    # Create successful response
                    api_response = APIResponse(
                        success=True,
                        data=data,
                        status_code=response.status,
                        quota_cost=quota_cost
                    )

                    # Cache successful response
                    if self.cache:
                        self.cache[cache_key] = api_response

                    return api_response

                elif response.status == 403:
                    error_data = await response.json()
                    error_message = error_data.get('error', {}).get('message', 'Quota exceeded')

                    logger.error(
                        "quota_exceeded",
                        error_message=error_message,
                        quota_used=self.quota_used
                    )

                    raise YouTubeAPIError(
                        f"Quota exceeded: {error_message}",
                        status_code=403,
                        quota_exceeded=True
                    )

                else:
                    error_text = await response.text()
                    logger.error(
                        "api_error",
                        status_code=response.status,
                        error_text=error_text[:200]
                    )

                    raise YouTubeAPIError(
                        f"API request failed: {response.status}",
                        status_code=response.status
                    )

        except aiohttp.ClientError as e:
            logger.error("network_error", error=str(e))
            raise YouTubeAPIError(f"Network error: {str(e)}")

    async def get_channel_info(self, channel_id: str) -> ChannelMetrics:
        """
        Get comprehensive channel information.

        Args:
            channel_id: YouTube channel ID

        Returns:
            ChannelMetrics object with structured channel data
        """
        params = {
            'part': 'snippet,statistics,brandingSettings,contentDetails',
            'id': channel_id
        }

        response = await self._make_request('channels', params, quota_cost=1)

        if not response.success or not response.data.get('items'):
            raise YouTubeAPIError(f"Channel not found: {channel_id}")

        channel_data = response.data['items'][0]
        snippet = channel_data['snippet']
        statistics = channel_data['statistics']

        return ChannelMetrics(
            channel_id=channel_id,
            title=snippet.get('title', ''),
            subscriber_count=int(statistics.get('subscriberCount', 0)),
            video_count=int(statistics.get('videoCount', 0)),
            view_count=int(statistics.get('viewCount', 0)),
            custom_url=snippet.get('customUrl'),
            country=snippet.get('country'),
            published_at=datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00')),
            thumbnail_url=snippet.get('thumbnails', {}).get('high', {}).get('url'),
            description=snippet.get('description', '')[:500]  # Truncate for storage
        )

    async def get_channel_videos(
        self,
        channel_id: str,
        max_results: int = 50,
        published_after: Optional[datetime] = None
    ) -> List[VideoMetrics]:
        """
        Get detailed video information for a channel.

        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to retrieve
            published_after: Only get videos published after this date

        Returns:
            List of VideoMetrics objects
        """
        # First, get the channel's upload playlist
        channel_info = await self.get_channel_info(channel_id)

        # Get upload playlist ID
        params = {
            'part': 'contentDetails',
            'id': channel_id
        }

        response = await self._make_request('channels', params, quota_cost=1)
        uploads_playlist_id = response.data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Get videos from upload playlist
        video_ids = await self._get_playlist_video_ids(
            uploads_playlist_id,
            max_results,
            published_after
        )

        if not video_ids:
            return []

        # Get detailed video information
        return await self._get_videos_details(video_ids)

    async def _get_playlist_video_ids(
        self,
        playlist_id: str,
        max_results: int,
        published_after: Optional[datetime] = None
    ) -> List[str]:
        """Get video IDs from a playlist."""
        video_ids = []
        next_page_token = None

        while len(video_ids) < max_results:
            params = {
                'part': 'contentDetails,snippet',
                'playlistId': playlist_id,
                'maxResults': min(50, max_results - len(video_ids))
            }

            if next_page_token:
                params['pageToken'] = next_page_token

            response = await self._make_request('playlistItems', params, quota_cost=1)

            for item in response.data.get('items', []):
                video_id = item['contentDetails']['videoId']

                # Check publish date filter
                if published_after:
                    published_at = datetime.fromisoformat(
                        item['snippet']['publishedAt'].replace('Z', '+00:00')
                    )
                    if published_at < published_after:
                        continue

                video_ids.append(video_id)

                if len(video_ids) >= max_results:
                    break

            next_page_token = response.data.get('nextPageToken')
            if not next_page_token:
                break

        return video_ids[:max_results]

    async def _get_videos_details(self, video_ids: List[str]) -> List[VideoMetrics]:
        """Get detailed information for multiple videos."""
        videos = []

        # Process videos in batches of 50 (API limit)
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i + 50]

            params = {
                'part': 'snippet,statistics,contentDetails',
                'id': ','.join(batch_ids)
            }

            response = await self._make_request('videos', params, quota_cost=1)

            for video_data in response.data.get('items', []):
                try:
                    snippet = video_data['snippet']
                    statistics = video_data['statistics']
                    content_details = video_data['contentDetails']

                    videos.append(VideoMetrics(
                        video_id=video_data['id'],
                        title=snippet.get('title', ''),
                        published_at=datetime.fromisoformat(
                            snippet['publishedAt'].replace('Z', '+00:00')
                        ),
                        duration=content_details.get('duration', 'PT0S'),
                        view_count=int(statistics.get('viewCount', 0)),
                        like_count=int(statistics.get('likeCount', 0)),
                        comment_count=int(statistics.get('commentCount', 0)),
                        tags=snippet.get('tags', []),
                        category_id=snippet.get('categoryId', ''),
                        thumbnail_url=snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                        description=snippet.get('description', '')[:500]  # Truncate
                    ))

                except (KeyError, ValueError) as e:
                    logger.warning(
                        "video_parsing_error",
                        video_id=video_data.get('id', 'unknown'),
                        error=str(e)
                    )
                    continue

        logger.info(
            "videos_collected",
            requested_count=len(video_ids),
            collected_count=len(videos)
        )

        return videos

    def get_quota_usage(self) -> Dict[str, Union[int, float]]:
        """Get current quota usage statistics."""
        return {
            'quota_used': self.quota_used,
            'quota_limit': self.quota_limit,
            'quota_remaining': self.quota_limit - self.quota_used,
            'quota_percentage': (self.quota_used / self.quota_limit) * 100
        }

    async def health_check(self) -> Dict[str, bool]:
        """Perform a health check of the API connection."""
        try:
            # Make a minimal API call
            params = {
                'part': 'snippet',
                'id': 'UCuAXFkgsw1L7xaCfnd5JJOw',  # YouTube's own channel
                'maxResults': 1
            }

            response = await self._make_request('channels', params, quota_cost=1)

            return {
                'api_accessible': response.success,
                'quota_available': self.quota_used < self.quota_limit * 0.9,
                'cache_enabled': self.cache is not None
            }

        except Exception as e:
            logger.error("health_check_failed", error=str(e))
            return {
                'api_accessible': False,
                'quota_available': False,
                'cache_enabled': self.cache is not None
            }


# Convenience functions for backward compatibility
async def collect_channel_data(
    api_key: str,
    channel_id: str,
    max_videos: int = 50,
    published_after: Optional[datetime] = None
) -> Tuple[ChannelMetrics, List[VideoMetrics]]:
    """
    Convenience function to collect comprehensive channel data.

    Args:
        api_key: YouTube Data API v3 key
        channel_id: YouTube channel ID
        max_videos: Maximum number of videos to collect
        published_after: Only collect videos published after this date

    Returns:
        Tuple of (ChannelMetrics, List[VideoMetrics])
    """
    async with EnhancedYouTubeDataCollector(api_key) as collector:
        channel_info = await collector.get_channel_info(channel_id)
        videos = await collector.get_channel_videos(
            channel_id,
            max_videos,
            published_after
        )

        return channel_info, videos


if __name__ == "__main__":
    # Example usage
    async def main():
        api_key = os.getenv('YOUTUBE_API_KEY')
        if not api_key:
            print("Please set YOUTUBE_API_KEY environment variable")
            return

        channel_id = "UCuTITJp_8VXjjthWdPdmwKA"  # Example channel

        try:
            channel_info, videos = await collect_channel_data(
                api_key,
                channel_id,
                max_videos=10
            )

            print(f"Channel: {channel_info.title}")
            print(f"Subscribers: {channel_info.subscriber_count:,}")
            print(f"Videos collected: {len(videos)}")

            for video in videos[:3]:
                print(f"- {video.title}: {video.view_count:,} views")

        except YouTubeAPIError as e:
            print(f"YouTube API Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    asyncio.run(main())