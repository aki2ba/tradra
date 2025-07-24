import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import time

load_dotenv()

class YouTubeClient:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YouTube API key not found. Please set YOUTUBE_API_KEY in .env file")
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def search_videos(self, query, max_results=50):
        """Search for videos with given query"""
        try:
            request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                videoDuration='short',  # For short videos
                maxResults=max_results,
                order='relevance'
            )
            response = request.execute()
            return response.get('items', [])
        except HttpError as e:
            print(f"HTTP error occurred: {e}")
            return []
    
    def get_video_details(self, video_ids):
        """Get detailed information for videos"""
        try:
            # Convert single ID to list
            if isinstance(video_ids, str):
                video_ids = [video_ids]
            
            # YouTube API allows up to 50 IDs per request
            video_details = []
            for i in range(0, len(video_ids), 50):
                batch_ids = video_ids[i:i+50]
                request = self.youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(batch_ids)
                )
                response = request.execute()
                video_details.extend(response.get('items', []))
                
                # Rate limiting
                time.sleep(0.1)
            
            return video_details
        except HttpError as e:
            print(f"HTTP error occurred: {e}")
            return []
    
    def get_video_comments(self, video_id, max_results=100):
        """Get comments for a video"""
        try:
            comments = []
            page_token = None
            
            while len(comments) < max_results:
                request = self.youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=min(100, max_results - len(comments)),
                    order='relevance',
                    pageToken=page_token
                )
                response = request.execute()
                
                comments.extend(response.get('items', []))
                page_token = response.get('nextPageToken')
                
                if not page_token:
                    break
                    
                # Rate limiting
                time.sleep(0.1)
            
            return comments
        except HttpError as e:
            print(f"HTTP error occurred: {e}")
            return []
    
    def filter_videos_by_views(self, videos, min_views=1000000):
        """Filter videos by minimum view count"""
        filtered_videos = []
        for video in videos:
            view_count = int(video['statistics'].get('viewCount', 0))
            if view_count >= min_views:
                filtered_videos.append(video)
        return filtered_videos
    
    def filter_comments_by_likes(self, comments, min_likes=1000):
        """Filter comments by minimum like count"""
        filtered_comments = []
        for comment in comments:
            like_count = int(comment['snippet']['topLevelComment']['snippet'].get('likeCount', 0))
            if like_count >= min_likes:
                filtered_comments.append(comment)
        return filtered_comments