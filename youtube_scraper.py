"""
YouTube Channel Scraper using Apify API
Fetches video metadata and transcripts from a YouTube channel
"""

import os
import time
import requests
from typing import List, Dict, Optional


class YouTubeScraper:
    def __init__(self, api_token: str):
        """
        Initialize YouTube scraper with Apify API token

        Args:
            api_token: Apify API token
        """
        self.api_token = api_token
        self.base_url = "https://api.apify.com/v2"

    def scrape_channel(self, channel_url: str, max_videos: int = 10) -> List[Dict]:
        """
        Scrape videos from a YouTube channel

        Args:
            channel_url: URL of the YouTube channel
            max_videos: Maximum number of videos to scrape (from newest to oldest)

        Returns:
            List of video data dictionaries with title, url, and transcript
        """
        print(f"\n🎬 Scraping YouTube channel: {channel_url}")
        print(f"📊 Fetching up to {max_videos} videos...")

        # Using the YouTube Transcripts actor in channel mode
        # Actor ID: johnvc/YoutubeTranscripts (the API path uses "~")
        actor_id = "johnvc~YoutubeTranscripts"

        # Prepare input for the actor
        actor_input = {
            "channel": channel_url,
            "max_videos": max_videos,
            "channel_transcripts": True,  # Enable transcript fetching
            "include_extended_metadata": True,  # Adds upload_date
            "output_formats": ["text"],
        }

        # Run the actor
        run_url = f"{self.base_url}/acts/{actor_id}/runs"
        headers = {"Authorization": f"Bearer {self.api_token}"}

        print("⏳ Starting Apify actor...")
        response = requests.post(
            run_url,
            json=actor_input,
            headers=headers,
            params={"token": self.api_token}
        )

        if response.status_code != 201:
            raise Exception(f"Failed to start actor: {response.text}")

        run_data = response.json()
        run_id = run_data["data"]["id"]
        dataset_id = run_data["data"]["defaultDatasetId"]

        # Wait for the actor to finish
        print("⏳ Waiting for actor to complete...")
        self._wait_for_completion(run_id)

        # Get the results
        print("📥 Fetching results...")
        videos = self._get_dataset_items(dataset_id)
        # Keep transcript rows only (channel listing rows have no text)
        videos = [video for video in videos if video.get("text")]

        print(f"✅ Successfully scraped {len(videos)} videos!")
        return videos[:max_videos]

    def _wait_for_completion(self, run_id: str, timeout: int = 600):
        """
        Wait for actor run to complete

        Args:
            run_id: The run ID to monitor
            timeout: Maximum wait time in seconds
        """
        start_time = time.time()
        status_url = f"{self.base_url}/actor-runs/{run_id}"
        headers = {"Authorization": f"Bearer {self.api_token}"}

        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError("Actor run timed out")

            response = requests.get(
                status_url,
                headers=headers,
                params={"token": self.api_token}
            )

            if response.status_code != 200:
                raise Exception(f"Failed to get run status: {response.text}")

            status_data = response.json()
            status = status_data["data"]["status"]

            if status == "SUCCEEDED":
                print("✅ Actor completed successfully!")
                break
            elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
                raise Exception(f"Actor run {status}")

            time.sleep(5)  # Check every 5 seconds

    def _get_dataset_items(self, dataset_id: str) -> List[Dict]:
        """
        Get items from the dataset

        Args:
            dataset_id: The dataset ID

        Returns:
            List of dataset items
        """
        dataset_url = f"{self.base_url}/datasets/{dataset_id}/items"
        headers = {"Authorization": f"Bearer {self.api_token}"}

        response = requests.get(
            dataset_url,
            headers=headers,
            params={"token": self.api_token}
        )

        if response.status_code != 200:
            raise Exception(f"Failed to get dataset items: {response.text}")

        return response.json()

    def format_video_data(self, videos: List[Dict]) -> List[Dict]:
        """
        Format video data for processing

        Args:
            videos: Raw video data from Apify

        Returns:
            Formatted video data with title, url, and transcript
        """
        formatted_videos = []

        for video in videos:
            formatted_video = {
                "title": video.get("title", "Unknown Title"),
                "url": video.get("url", ""),
                "video_id": video.get("video_id", ""),
                "description": video.get("description", ""),
                "transcript": video.get("text", ""),
                "duration": video.get("video_duration_seconds", ""),
                "view_count": video.get("view_count") or 0,
                "published_date": video.get("upload_date", "")
            }
            formatted_videos.append(formatted_video)

        return formatted_videos
