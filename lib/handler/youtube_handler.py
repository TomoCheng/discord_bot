import json
import os
import requests
from lib.utils.logger import log
from youtube_search import YoutubeSearch
from dotenv import load_dotenv

load_dotenv()


class YoutubeHandler:
    """YoutubeHandler"""

    def __init__(self):
        self.yt_url_base = 'https://www.googleapis.com/youtube/v3/'
        self.yt_video_url_base = 'https://www.youtube.com/watch?v='
        self.token = os.environ.get("youtube_api_token")

    def search_youtube_video(self, search_text):
        """Search youtube by text

        Args:
            `search_text`: Text for search.

        Returns:
            Url of the first video in search results
        """
        results = YoutubeSearch(search_text, max_results=1).to_json()
        videos = json.loads(results)['videos']
        first_video_id = videos[0]['id']
        video_url = f'https://www.youtube.com/watch?v={first_video_id}'
        print(
            f'[youtube_handler] search text: {search_text}, video_url:'
            f' {video_url}'
        )
        return video_url

    def combine_youtube_video_url(self, video_id):
        return f'{self.yt_video_url_base}{video_id}'

    def combine_url_and_get(self, method, params):
        """Combine URL and GET

        Args:
            `method`: method of Youtbe V3 api. ex.'channels' or 'playlistItems'
            `params`: params of this method.   ex.'part=contentDetails'

        Returns:
            response of get
        """
        url = f"{self.yt_url_base}{method}?{params}&key={self.token}"
        request = requests.get(url)
        log(
            '[youtube_lib]',
            f'get {method}: {request.status_code} {request.text}',
        )
        if request.status_code == 200:
            return request
        else:
            return None

    def get_video_info(self, video_id, part="snippet"):
        """Get video info from Youtube.

        Args:
            `video_id`: Video ID.
            `part`: Part to get.

        Returns:
            Video info.
        """

        params = f"part={part}&id={video_id}"
        request = self.combine_url_and_get("videos", params)
        ##print(request.text)
        if request is not None:
            return json.loads(request.text)
        else:
            return None
