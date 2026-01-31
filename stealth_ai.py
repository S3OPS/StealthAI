#!/usr/bin/env python3
"""
StealthAI - Main Execution Engine
Faceless AI automation for revenue generation
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core import SignalCompressor, MicroStacker, MicroTask, TaskPriority
from ai_engine import AIEngine
from integrations import AmazonAffiliate, YouTubeAutomation
from analytics import RevenueTracker, RevenueMetric

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stealth_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class StealthAI:
    """
    Main StealthAI engine - orchestrates the entire automation system.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize StealthAI system.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self._initialize_components()
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Get default configuration"""
        return {
            "amazon_affiliate": {
                "tracking_id": "your-affiliate-id-20"
            },
            "youtube": {
                "api_key": "YOUR_API_KEY"
            },
            "ai_tools": {
                "ollama_endpoint": "http://localhost:11434",
                "default_model": "llama2"
            },
            "signal_compression": {
                "compression_ratio": 0.3,
                "signal_threshold": 0.7
            },
            "micro_stacking": {
                "max_stack_depth": 5,
                "parallel_tasks": 3
            },
            "revenue_targets": {
                "quick_target": 310,
                "main_target": 8700
            }
        }
    
    def _initialize_components(self):
        """Initialize all system components"""
        # Core components
        self.compressor = SignalCompressor(
            compression_ratio=self.config['signal_compression']['compression_ratio'],
            threshold=self.config['signal_compression']['signal_threshold']
        )
        
        self.stacker = MicroStacker(
            max_depth=self.config['micro_stacking']['max_stack_depth'],
            parallel_tasks=self.config['micro_stacking']['parallel_tasks']
        )
        
        # AI Engine
        self.ai_engine = AIEngine(
            endpoint=self.config['ai_tools']['ollama_endpoint'],
            default_model=self.config['ai_tools']['default_model']
        )
        
        # Integrations
        self.amazon = AmazonAffiliate(
            tracking_id=self.config['amazon_affiliate']['tracking_id']
        )
        
        self.youtube = YouTubeAutomation(
            api_key=self.config['youtube']['api_key'],
            channel_id=self.config['youtube'].get('channel_id')
        )
        
        # Analytics
        self.revenue = RevenueTracker(
            quick_target=self.config['revenue_targets']['quick_target'],
            main_target=self.config['revenue_targets']['main_target']
        )
        
        logger.info("StealthAI system initialized successfully")
    
    def generate_faceless_content(self, topic: str, keywords: List[str],
                                  product_asins: List[str] = None) -> dict:
        """
        Generate faceless video content with affiliate integration.
        
        Args:
            topic: Content topic
            keywords: SEO keywords
            product_asins: Amazon product ASINs to promote
            
        Returns:
            Complete content package
        """
        logger.info(f"Generating faceless content for: {topic}")
        
        # Compress signals to focus on high-value keywords
        keyword_signals = [
            {'value': kw, 'strength': 0.8, 'metadata': {'type': 'keyword'}}
            for kw in keywords
        ]
        compressed_keywords = self.compressor.compress_signals(keyword_signals)
        top_keywords = [s['value'] for s in compressed_keywords]
        
        # Generate video script
        script = self.ai_engine.generate_video_script(
            topic=topic,
            keywords=top_keywords,
            duration_minutes=10
        )
        
        # Generate YouTube metadata
        metadata = self.ai_engine.generate_youtube_metadata(
            topic=topic,
            keywords=top_keywords
        )
        
        # Optimize metadata
        optimized_metadata = self.youtube.optimize_metadata(
            title=metadata['title'],
            description=metadata['description'],
            keywords=top_keywords
        )
        
        # Generate product recommendations if ASINs provided
        product_content = ""
        if product_asins:
            products = [
                {'name': f'Product {i+1}', 'url': asin}
                for i, asin in enumerate(product_asins)
            ]
            product_content = self.amazon.create_product_showcase(
                products=products,
                title="Recommended Products"
            )
        
        return {
            'topic': topic,
            'script': script,
            'metadata': optimized_metadata,
            'keywords': top_keywords,
            'products': product_content,
            'thumbnail_text': self.youtube.optimize_thumbnail_text(
                metadata['title'],
                top_keywords
            )
        }
    
    def create_content_pipeline(self, topics: List[str], keywords_per_topic: dict,
                               products_per_topic: dict = None) -> List[dict]:
        """
        Create a complete content pipeline using micro-stacking.
        
        Args:
            topics: List of content topics
            keywords_per_topic: Dictionary mapping topics to keywords
            products_per_topic: Dictionary mapping topics to product ASINs
            
        Returns:
            List of generated content packages
        """
        logger.info(f"Creating content pipeline for {len(topics)} topics")
        
        products_per_topic = products_per_topic or {}
        
        # Create micro tasks for each topic
        for idx, topic in enumerate(topics):
            keywords = keywords_per_topic.get(topic, [])
            products = products_per_topic.get(topic, [])
            
            task = MicroTask(
                id=f"content_{idx}_{topic[:20]}",
                function=self.generate_faceless_content,
                args=(topic, keywords, products),
                kwargs={},
                priority=TaskPriority.HIGH
            )
            self.stacker.add_task(task)
        
        # Execute all tasks
        results = self.stacker.execute_stack()
        
        # Extract results
        content_packages = [
            result for result in results.values()
            if isinstance(result, dict) and 'script' in result
        ]
        
        logger.info(f"Generated {len(content_packages)} content packages")
        return content_packages
    
    def run_quick_revenue_strategy(self) -> dict:
        """
        Execute strategy to reach quick $310 target.
        
        Returns:
            Strategy execution report
        """
        logger.info("Executing quick revenue strategy ($310 target)")
        
        # High-converting product niches
        quick_niches = [
            {
                'topic': 'Tech Gadgets Under $50',
                'keywords': ['budget tech', 'affordable gadgets', 'tech deals'],
                'products': ['B08N5WRWNW', 'B07ZPKN6YR']  # Example ASINs
            },
            {
                'topic': 'Home Office Setup Essentials',
                'keywords': ['work from home', 'home office', 'productivity'],
                'products': ['B07MQNJP3J', 'B08F2K1YTJ']
            }
        ]
        
        # Generate content for quick niches
        topics = [n['topic'] for n in quick_niches]
        keywords_map = {n['topic']: n['keywords'] for n in quick_niches}
        products_map = {n['topic']: n['products'] for n in quick_niches}
        
        content_packages = self.create_content_pipeline(
            topics=topics,
            keywords_per_topic=keywords_map,
            products_per_topic=products_map
        )
        
        # Generate upload schedule
        schedule = self.youtube.create_upload_schedule(
            video_count=len(content_packages),
            frequency='daily'
        )
        
        return {
            'strategy': 'quick_revenue',
            'target': 310,
            'content_count': len(content_packages),
            'upload_schedule': schedule,
            'estimated_days': len(schedule),
            'content_packages': content_packages
        }
    
    def run_main_revenue_engine(self) -> dict:
        """
        Execute main engine to reach $8.7K target.
        
        Returns:
            Engine execution report
        """
        logger.info("Running main revenue engine ($8.7K target)")
        
        # Diversified content strategy
        main_niches = [
            {
                'topic': 'Best Tech Products 2024',
                'keywords': ['tech reviews', '2024 gadgets', 'best tech'],
                'products': ['B0BSHF7VVK', 'B08N5WRWNW', 'B07ZPKN6YR']
            },
            {
                'topic': 'Home Automation Guide',
                'keywords': ['smart home', 'home automation', 'iot'],
                'products': ['B08MQLDNTK', 'B07YTK2VT1']
            },
            {
                'topic': 'Gaming Setup on a Budget',
                'keywords': ['budget gaming', 'gaming setup', 'pc gaming'],
                'products': ['B08HR5SXPS', 'B07MQNJP3J']
            },
            {
                'topic': 'Photography Gear for Beginners',
                'keywords': ['photography tips', 'camera gear', 'photography'],
                'products': ['B07VGRWFV8', 'B08F2K1YTJ']
            }
        ]
        
        topics = [n['topic'] for n in main_niches]
        keywords_map = {n['topic']: n['keywords'] for n in main_niches}
        products_map = {n['topic']: n['products'] for n in main_niches}
        
        content_packages = self.create_content_pipeline(
            topics=topics,
            keywords_per_topic=keywords_map,
            products_per_topic=products_map
        )
        
        # Create video series
        series = self.youtube.create_video_series(
            topic="Tech & Lifestyle",
            num_videos=len(content_packages)
        )
        
        # Generate schedule (every 2 days for sustained growth)
        schedule = self.youtube.create_upload_schedule(
            video_count=len(content_packages),
            frequency='every2days'
        )
        
        return {
            'strategy': 'main_engine',
            'target': 8700,
            'content_count': len(content_packages),
            'series': series,
            'upload_schedule': schedule,
            'estimated_days': len(schedule) * 2,
            'content_packages': content_packages
        }
    
    def get_status_report(self) -> dict:
        """
        Get current system status and revenue progress.
        
        Returns:
            Status report
        """
        progress = self.revenue.get_progress_report()
        predictions = self.revenue.predict_target_date()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'revenue_progress': progress,
            'predictions': predictions,
            'system_status': 'operational'
        }
    
    def shutdown(self):
        """Shutdown the system gracefully"""
        logger.info("Shutting down StealthAI system")
        self.stacker.shutdown()


def main():
    """Main execution function"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                    STEALTH AI SYSTEM                      ║
    ║          Faceless Revenue Generation Engine              ║
    ║                                                           ║
    ║  Signal Compression + Micro-Stacking Architecture         ║
    ║  Target: $310 Quick → $8.7K Main                          ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize system
    stealth = StealthAI()
    
    try:
        # Show current status
        print("\n[*] System Status:")
        status = stealth.get_status_report()
        print(f"    Revenue Progress: ${status['revenue_progress']['total_revenue']:.2f}")
        print(f"    Quick Target: {status['revenue_progress']['quick_progress']:.1f}% complete")
        print(f"    Main Target: {status['revenue_progress']['main_progress']:.1f}% complete")
        
        # Execute quick revenue strategy
        print("\n[*] Executing Quick Revenue Strategy ($310 target)...")
        quick_result = stealth.run_quick_revenue_strategy()
        print(f"    Generated {quick_result['content_count']} content packages")
        print(f"    Upload schedule: {quick_result['estimated_days']} days")
        
        # Execute main revenue engine
        print("\n[*] Running Main Revenue Engine ($8.7K target)...")
        main_result = stealth.run_main_revenue_engine()
        print(f"    Generated {main_result['content_count']} content packages")
        print(f"    Series created with {len(main_result['series'])} videos")
        print(f"    Upload schedule: {main_result['estimated_days']} days")
        
        # Final status
        print("\n[*] Execution Complete!")
        print(f"    Total content packages: {quick_result['content_count'] + main_result['content_count']}")
        print(f"    System ready for deployment")
        
        # Show sample content
        if quick_result['content_packages']:
            sample = quick_result['content_packages'][0]
            print(f"\n[*] Sample Content Package:")
            print(f"    Topic: {sample['topic']}")
            print(f"    Title: {sample['metadata']['title']}")
            print(f"    Keywords: {', '.join(sample['keywords'][:3])}")
            print(f"    Thumbnail: {sample['thumbnail_text']}")
        
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}", exc_info=True)
        print(f"\n[!] Error: {str(e)}")
    finally:
        stealth.shutdown()
        print("\n[*] StealthAI shutdown complete")


if __name__ == "__main__":
    from typing import List
    main()
