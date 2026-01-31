#!/usr/bin/env python3
"""
Quick Start Example - Generate your first content package
"""

from stealth_ai import StealthAI

def main():
    print("StealthAI Quick Start Example")
    print("=" * 50)
    
    # Initialize system
    print("\n[1] Initializing StealthAI...")
    stealth = StealthAI()
    
    # Generate single content package
    print("\n[2] Generating content package...")
    content = stealth.generate_faceless_content(
        topic="Top 5 Budget Tech Gadgets 2024",
        keywords=["budget tech", "affordable gadgets", "tech deals", "best budget tech"],
        product_asins=["B08N5WRWNW", "B07ZPKN6YR", "B08F2K1YTJ"]
    )
    
    # Display results
    print("\n[3] Content Package Generated!")
    print(f"\nTopic: {content['topic']}")
    print(f"\nYouTube Title: {content['metadata']['title']}")
    print(f"\nThumbnail Text: {content['thumbnail_text']}")
    print(f"\nKeywords: {', '.join(content['keywords'])}")
    print(f"\nVideo Description (first 200 chars):\n{content['metadata']['description'][:200]}...")
    
    print(f"\n\nScript Preview (first 300 chars):\n{content['script']['script'][:300]}...")
    
    if content['products']:
        print(f"\n\nAffiliate Products Showcase:\n{content['products'][:200]}...")
    
    print("\n" + "=" * 50)
    print("✓ Content package ready for production!")
    print("\nNext steps:")
    print("  1. Record voiceover using the script")
    print("  2. Create video using stock footage")
    print("  3. Upload to YouTube with generated metadata")
    print("  4. Monitor revenue in the analytics dashboard")

if __name__ == "__main__":
    main()
