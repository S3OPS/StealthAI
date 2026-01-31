"""
YouTube Integration
Automates video metadata and content management
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class YouTubeAutomation:
    """
    YouTube automation for faceless video channels.
    Manages video metadata, scheduling, and optimization.
    """
    
    def __init__(self, api_key: str, channel_id: str = None):
        """
        Initialize YouTube automation.
        
        Args:
            api_key: YouTube Data API key
            channel_id: YouTube channel ID
        """
        self.api_key = api_key
        self.channel_id = channel_id
        self.api_base = "https://www.googleapis.com/youtube/v3"
        
    def optimize_metadata(self, title: str, description: str, 
                         keywords: List[str]) -> Dict[str, Any]:
        """
        Optimize video metadata for maximum reach.
        
        Args:
            title: Video title
            description: Video description
            keywords: SEO keywords
            
        Returns:
            Optimized metadata
        """
        # Optimize title (max 100 chars, front-load keywords)
        optimized_title = self._optimize_title(title, keywords)
        
        # Optimize description with keywords and structure
        optimized_desc = self._optimize_description(description, keywords)
        
        # Generate tags (max 500 chars total)
        tags = self._generate_tags(keywords)
        
        return {
            'title': optimized_title,
            'description': optimized_desc,
            'tags': tags,
            'categoryId': '22',  # People & Blogs - adjust as needed
            'defaultLanguage': 'en',
            'defaultAudioLanguage': 'en'
        }
    
    def _optimize_title(self, title: str, keywords: List[str]) -> str:
        """Optimize video title for SEO"""
        # Ensure title is under 100 characters
        if len(title) <= 100:
            return title
        
        # Try to include top keyword and truncate
        top_keyword = keywords[0] if keywords else ""
        if top_keyword and top_keyword.lower() not in title.lower():
            title = f"{top_keyword} - {title}"
        
        return title[:97] + "..." if len(title) > 100 else title
    
    def _optimize_description(self, description: str, keywords: List[str]) -> str:
        """Optimize video description for SEO"""
        # YouTube description best practices
        optimized = description
        
        # Add keyword-rich opening
        if keywords:
            keyword_intro = f"Learn about {', '.join(keywords[:3])} in this comprehensive guide.\n\n"
            if not any(kw.lower() in description[:100].lower() for kw in keywords[:3]):
                optimized = keyword_intro + optimized
        
        # Add timestamps section placeholder
        if "Timestamps:" not in optimized:
            optimized += "\n\n⏱️ Timestamps:\n0:00 - Introduction\n"
        
        # Add hashtags (3-5 is optimal)
        hashtags = [f"#{kw.replace(' ', '')}" for kw in keywords[:5]]
        if optimized.count('#') < 3:
            optimized += f"\n\n{' '.join(hashtags)}"
        
        # Add call to action
        if "subscribe" not in optimized.lower():
            optimized += "\n\n👍 Like this video and subscribe for more content!"
        
        return optimized
    
    def _generate_tags(self, keywords: List[str]) -> List[str]:
        """Generate optimized tags from keywords"""
        tags = []
        total_length = 0
        max_length = 400  # Leave some buffer under 500
        
        # Add exact keywords
        for kw in keywords:
            tag_length = len(kw) + 1  # +1 for separator
            if total_length + tag_length <= max_length:
                tags.append(kw)
                total_length += tag_length
            else:
                break
        
        # Add variations of top keywords
        if keywords and total_length < max_length:
            variations = [
                f"{keywords[0]} tutorial",
                f"{keywords[0]} guide",
                f"how to {keywords[0]}"
            ]
            for var in variations:
                if total_length + len(var) + 1 <= max_length:
                    tags.append(var)
                    total_length += len(var) + 1
        
        return tags
    
    def create_upload_schedule(self, video_count: int, 
                              start_date: datetime = None,
                              frequency: str = "daily") -> List[Dict[str, Any]]:
        """
        Create an upload schedule for batch content.
        
        Args:
            video_count: Number of videos to schedule
            start_date: Start date (defaults to tomorrow)
            frequency: Upload frequency (daily, every2days, weekly)
            
        Returns:
            List of scheduled upload slots
        """
        if start_date is None:
            start_date = datetime.now() + timedelta(days=1)
        
        interval_days = {
            'daily': 1,
            'every2days': 2,
            'weekly': 7
        }.get(frequency, 1)
        
        schedule = []
        for i in range(video_count):
            upload_date = start_date + timedelta(days=i * interval_days)
            schedule.append({
                'video_number': i + 1,
                'upload_date': upload_date.isoformat(),
                'publish_time': '09:00:00',  # Optimal upload time
                'status': 'scheduled'
            })
        
        logger.info(f"Created schedule for {video_count} videos")
        return schedule
    
    def generate_playlist_config(self, theme: str, video_titles: List[str]) -> Dict[str, Any]:
        """
        Generate playlist configuration for content organization.
        
        Args:
            theme: Playlist theme
            video_titles: List of video titles for the playlist
            
        Returns:
            Playlist configuration
        """
        return {
            'title': f"{theme} - Complete Guide",
            'description': f"Everything you need to know about {theme}. Watch the full series!",
            'privacy_status': 'public',
            'video_count': len(video_titles),
            'videos': video_titles
        }
    
    def optimize_thumbnail_text(self, title: str, keywords: List[str]) -> str:
        """
        Generate optimal thumbnail text overlay.
        
        Args:
            title: Video title
            keywords: Keywords to emphasize
            
        Returns:
            Thumbnail text (short, punchy)
        """
        # Extract key phrases (max 3-4 words for thumbnail)
        words = title.split()
        
        # Try to find keyword in title
        thumbnail_text = ""
        for kw in keywords:
            if kw.lower() in title.lower():
                # Found keyword, use it
                thumbnail_text = kw.upper()
                break
        
        if not thumbnail_text:
            # Use first 2-3 words of title
            thumbnail_text = ' '.join(words[:3]).upper()
        
        # Limit to 20 characters for readability
        if len(thumbnail_text) > 20:
            thumbnail_text = thumbnail_text[:17] + "..."
        
        return thumbnail_text
    
    def create_video_series(self, topic: str, num_videos: int) -> List[Dict[str, str]]:
        """
        Create a video series structure.
        
        Args:
            topic: Series topic
            num_videos: Number of videos in series
            
        Returns:
            List of video concepts
        """
        series = []
        
        # Generate series structure
        video_types = [
            "Introduction to",
            "Getting Started with",
            "Advanced Techniques in",
            "Common Mistakes in",
            "Best Practices for",
            "Tips and Tricks for",
            "Complete Guide to",
            "Case Studies:"
        ]
        
        for i in range(num_videos):
            video_type = video_types[i % len(video_types)]
            series.append({
                'number': i + 1,
                'title': f"{video_type} {topic} (Part {i + 1})",
                'concept': f"Cover aspect {i + 1} of {topic}",
                'position': i
            })
        
        return series
    
    def analyze_best_upload_time(self, target_audience: str = "US") -> Dict[str, str]:
        """
        Suggest best upload times based on audience.
        
        Args:
            target_audience: Target audience region
            
        Returns:
            Recommended upload schedule
        """
        schedules = {
            'US': {
                'best_days': ['Thursday', 'Friday', 'Saturday'],
                'best_time': '14:00-16:00 EST',
                'reason': 'Peak engagement for US audience'
            },
            'UK': {
                'best_days': ['Wednesday', 'Thursday', 'Friday'],
                'best_time': '13:00-15:00 GMT',
                'reason': 'Peak engagement for UK audience'
            },
            'Global': {
                'best_days': ['Friday', 'Saturday', 'Sunday'],
                'best_time': '09:00-11:00 EST',
                'reason': 'Balanced for global audience'
            }
        }
        
        return schedules.get(target_audience, schedules['Global'])
    
    def create_end_screen_elements(self, related_videos: List[str] = None) -> Dict[str, Any]:
        """
        Create end screen configuration for videos.
        
        Args:
            related_videos: List of related video IDs
            
        Returns:
            End screen configuration
        """
        elements = []
        
        # Subscribe button
        elements.append({
            'type': 'subscribe',
            'position': 'top_right',
            'duration': 20,
            'start_time': -20  # Last 20 seconds
        })
        
        # Best for viewer video
        elements.append({
            'type': 'best_for_viewer',
            'position': 'top_left',
            'duration': 20,
            'start_time': -20
        })
        
        # Related videos if provided
        if related_videos:
            for idx, video_id in enumerate(related_videos[:2]):
                elements.append({
                    'type': 'video',
                    'video_id': video_id,
                    'position': f'bottom_{["left", "right"][idx]}',
                    'duration': 20,
                    'start_time': -20
                })
        
        return {
            'elements': elements,
            'duration': 20
        }
