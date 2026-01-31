#!/usr/bin/env python3
"""
Batch Content Generation Example
Create multiple content packages at once
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from stealth_ai import StealthAI

def main():
    print("Batch Content Generation Example")
    print("=" * 50)
    
    # Initialize system
    stealth = StealthAI()
    
    # Define content topics
    topics = [
        "Smart Home Devices You Actually Need",
        "Gaming Setup Essentials Under $500",
        "Photography Gear for Beginners 2024",
        "Best Productivity Tools for Remote Work"
    ]
    
    # Define keywords for each topic
    keywords_map = {
        "Smart Home Devices You Actually Need": [
            "smart home", "home automation", "smart devices", "iot gadgets"
        ],
        "Gaming Setup Essentials Under $500": [
            "budget gaming", "gaming setup", "affordable gaming", "pc gaming"
        ],
        "Photography Gear for Beginners 2024": [
            "photography", "camera gear", "beginner photography", "photo equipment"
        ],
        "Best Productivity Tools for Remote Work": [
            "productivity", "remote work", "work from home", "productivity tools"
        ]
    }
    
    # Define products for each topic
    products_map = {
        "Smart Home Devices You Actually Need": [
            "B08MQLDNTK", "B07YTK2VT1", "B08F2K1YTJ"
        ],
        "Gaming Setup Essentials Under $500": [
            "B08HR5SXPS", "B07MQNJP3J", "B08N5WRWNW"
        ],
        "Photography Gear for Beginners 2024": [
            "B07VGRWFV8", "B08F2K1YTJ", "B07ZPKN6YR"
        ],
        "Best Productivity Tools for Remote Work": [
            "B07MQNJP3J", "B08F2K1YTJ", "B08N5WRWNW"
        ]
    }
    
    print(f"\n[*] Generating {len(topics)} content packages...")
    
    # Generate all content packages
    content_packages = stealth.create_content_pipeline(
        topics=topics,
        keywords_per_topic=keywords_map,
        products_per_topic=products_map
    )
    
    print(f"\n✓ Generated {len(content_packages)} content packages!")
    
    # Display summary
    print("\n" + "=" * 50)
    print("Content Package Summary:")
    print("=" * 50)
    
    for idx, package in enumerate(content_packages, 1):
        print(f"\n{idx}. {package['topic']}")
        print(f"   Title: {package['metadata']['title']}")
        print(f"   Keywords: {', '.join(package['keywords'][:3])}")
        print(f"   Thumbnail: {package['thumbnail_text']}")
    
    # Create upload schedule
    print("\n" + "=" * 50)
    print("Upload Schedule (Daily):")
    print("=" * 50)
    
    schedule = stealth.youtube.create_upload_schedule(
        video_count=len(content_packages),
        frequency='daily'
    )
    
    for slot in schedule:
        print(f"Video {slot['video_number']}: {slot['upload_date']} at {slot['publish_time']}")
    
    print("\n" + "=" * 50)
    print("✓ Batch generation complete!")
    print(f"  Total packages: {len(content_packages)}")
    print(f"  Upload duration: {len(schedule)} days")

if __name__ == "__main__":
    main()
