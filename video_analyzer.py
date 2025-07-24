import pandas as pd
from youtube_client import YouTubeClient
import time

class VideoAnalyzer:
    def __init__(self, keywords=None):
        self.client = YouTubeClient()
        self.keywords = keywords if keywords else ["参政党", "選挙", "政治"]
        self.min_views = 1000000  # 100万回以上
        self.min_comment_likes = 1000  # 1000いいね以上
    
    def search_all_keywords(self, max_results_per_keyword=50):
        """Search videos for all keywords"""
        all_videos = []
        
        for keyword in self.keywords:
            print(f"Searching for keyword: {keyword}")
            videos = self.client.search_videos(keyword, max_results_per_keyword)
            
            # Add keyword info to each video
            for video in videos:
                video['search_keyword'] = keyword
            
            all_videos.extend(videos)
            time.sleep(1)  # Rate limiting
        
        return all_videos
    
    def analyze_videos(self):
        """Main analysis function"""
        print("Starting video analysis...")
        
        # Step 1: Search for videos
        print("Step 1: Searching for videos...")
        search_results = self.search_all_keywords()
        print(f"Found {len(search_results)} videos from search")
        
        if not search_results:
            print("No videos found")
            return []
        
        # Step 2: Get detailed video information
        print("Step 2: Getting video details...")
        video_ids = [video['id']['videoId'] for video in search_results if 'videoId' in video['id']]
        video_details = self.client.get_video_details(video_ids)
        print(f"Got details for {len(video_details)} videos")
        
        # Step 3: Filter by view count
        print("Step 3: Filtering by view count...")
        popular_videos = self.client.filter_videos_by_views(video_details, self.min_views)
        print(f"Found {len(popular_videos)} videos with {self.min_views:,}+ views")
        
        if not popular_videos:
            print("No videos meet the view count criteria")
            return []
        
        # Step 4: Get comments for each video
        print("Step 4: Getting comments...")
        results = []
        
        for i, video in enumerate(popular_videos):
            video_id = video['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_title = video['snippet']['title']
            view_count = int(video['statistics'].get('viewCount', 0))
            
            print(f"Processing video {i+1}/{len(popular_videos)}: {video_title}")
            
            # Get comments
            comments = self.client.get_video_comments(video_id, max_results=200)
            
            # Filter comments by likes
            popular_comments = self.client.filter_comments_by_likes(comments, self.min_comment_likes)
            
            print(f"  Found {len(popular_comments)} comments with {self.min_comment_likes}+ likes")
            
            # Add each popular comment as a result
            for comment in popular_comments:
                comment_data = comment['snippet']['topLevelComment']['snippet']
                results.append({
                    'video_url': video_url,
                    'video_title': video_title,
                    'video_views': view_count,
                    'comment_text': comment_data['textDisplay'],
                    'comment_likes': int(comment_data.get('likeCount', 0)),
                    'comment_author': comment_data['authorDisplayName'],
                    'comment_published': comment_data['publishedAt']
                })
            
            # Rate limiting
            time.sleep(1)
        
        print(f"Analysis complete. Found {len(results)} popular comments from popular videos.")
        return results
    
    def save_to_csv(self, results, filename='youtube_analysis_results.csv'):
        """Save results to CSV file"""
        if not results:
            print("No results to save")
            return
        
        df = pd.DataFrame(results)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Results saved to {filename}")
        print(f"Total entries: {len(df)}")
        
        # Display summary
        print("\nSummary:")
        print(f"Unique videos: {df['video_url'].nunique()}")
        print(f"Total comments: {len(df)}")
        print(f"Average comment likes: {df['comment_likes'].mean():.0f}")
        print(f"Max comment likes: {df['comment_likes'].max()}")
        
        return df