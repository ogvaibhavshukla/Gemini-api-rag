"""Unit tests for youtube_scraper.py (no network).

Run with: python -m unittest discover tests
"""
import unittest
from unittest import mock

import youtube_scraper
from youtube_scraper import YouTubeScraper

CHANNEL = "https://www.youtube.com/@TED"
OK_ROW = {"status": "OK", "videoId": "jNQXAC9IVRw", "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
          "title": "Me at the zoo", "text": "All right, so here we are", "lengthSeconds": 19}
FAILED_ROW = {"status": "FAILED", "videoId": "aqz-KE-bpKQ", "errorCode": "NO_CAPTIONS",
              "errorMessage": "This video has no captions"}


def _resp(status, payload):
    r = mock.Mock(status_code=status)
    r.json.return_value = payload
    return r


class ScrapeChannelTest(unittest.TestCase):
    def setUp(self):
        self.scraper = YouTubeScraper("test-token")

    @mock.patch.object(youtube_scraper.time, "sleep")
    @mock.patch.object(youtube_scraper.requests, "get")
    @mock.patch.object(youtube_scraper.requests, "post")
    def test_runs_transcript_actor_and_skips_failed_rows(self, post, get, _sleep):
        post.return_value = _resp(201, {"data": {"id": "run1", "defaultDatasetId": "ds1"}})
        get.side_effect = [
            _resp(200, {"data": {"status": "SUCCEEDED"}}),
            _resp(200, [FAILED_ROW, OK_ROW]),
        ]

        videos = self.scraper.scrape_channel(CHANNEL, max_videos=1)

        self.assertIn("/acts/shephouse~youtube-transcript-scraper-bulk/runs", post.call_args.args[0])
        self.assertEqual(post.call_args.kwargs["json"], {"startUrls": [{"url": CHANNEL}], "maxTranscripts": 1})
        self.assertEqual(videos, [OK_ROW])

    def test_format_video_data_maps_actor_fields(self):
        formatted = self.scraper.format_video_data([OK_ROW, FAILED_ROW])
        self.assertEqual(len(formatted), 1)
        self.assertEqual(formatted[0]["title"], "Me at the zoo")
        self.assertEqual(formatted[0]["video_id"], "jNQXAC9IVRw")
        self.assertEqual(formatted[0]["transcript"], "All right, so here we are")
        self.assertEqual(formatted[0]["duration"], 19)
        self.assertEqual(formatted[0]["description"], "")

    def test_format_video_data_keeps_legacy_field_names(self):
        legacy = {"id": "abc", "title": "t", "transcript": "legacy text", "duration": "1:00"}
        formatted = self.scraper.format_video_data([legacy])[0]
        self.assertEqual((formatted["video_id"], formatted["transcript"], formatted["duration"]),
                         ("abc", "legacy text", "1:00"))


if __name__ == "__main__":
    unittest.main()
