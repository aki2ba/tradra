#!/usr/bin/env python3
"""
YouTube Short Video Analysis Tool

Usage: python main.py "keyword1 keyword2 keyword3" [output_filename.csv]

This tool analyzes YouTube short videos based on specified keywords and criteria:
- Minimum views: 1,000,000 (1 million)
- Minimum comment likes: 1,000

Output: CSV file with video URLs and popular comments
"""

import os
import sys
from video_analyzer import VideoAnalyzer

def parse_keywords(keyword_string):
    """Parse space-separated keywords from quoted string"""
    return keyword_string.split()

def main():
    print("YouTube Short Video Analysis Tool")
    print("=" * 50)
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py \"keyword1 keyword2 keyword3\" [output_filename.csv]")
        print("Example: python main.py \"神谷 参政党 政治\" results.csv")
        sys.exit(1)
    
    keywords_string = sys.argv[1]
    keywords = parse_keywords(keywords_string)
    
    output_filename = sys.argv[2] if len(sys.argv) > 2 else 'youtube_analysis_results.csv'
    
    print(f"Keywords: {', '.join(keywords)}")
    print("Minimum video views: 1,000,000")
    print("Minimum comment likes: 1,000")
    print(f"Output file: {output_filename}")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Error: .env file not found!")
        print("Please create a .env file with your YouTube API key:")
        print("YOUTUBE_API_KEY=your_api_key_here")
        print("\nYou can copy .env.example to .env and fill in your API key.")
        sys.exit(1)
    
    try:
        # Initialize analyzer with custom keywords
        analyzer = VideoAnalyzer(keywords=keywords)
        
        # Run analysis
        results = analyzer.analyze_videos()
        
        if results:
            # Save to CSV
            df = analyzer.save_to_csv(results, filename=output_filename)
            print(f"\nAnalysis completed successfully!")
            print(f"Results saved to: {output_filename}")
        else:
            print("No results found matching the criteria.")
            
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()