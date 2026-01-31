#!/usr/bin/env python3
"""
Revenue Tracking Example
Monitor and analyze revenue progress
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from analytics import RevenueTracker, RevenueMetric
from datetime import datetime, timedelta

def main():
    print("Revenue Tracking Example")
    print("=" * 50)
    
    # Initialize tracker
    tracker = RevenueTracker(quick_target=310, main_target=8700)
    
    # Simulate some revenue data
    print("\n[*] Adding sample revenue data...")
    
    # Add metrics for last 7 days
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
        
        # Amazon affiliate
        amazon_metric = RevenueMetric(
            date=date,
            source='amazon',
            clicks=50 + (i * 10),
            conversions=3 + i,
            revenue=15.50 + (i * 5),
            campaign='tech-gadgets'
        )
        tracker.add_metric(amazon_metric)
        
        # YouTube
        youtube_metric = RevenueMetric(
            date=date,
            source='youtube',
            clicks=100 + (i * 20),
            conversions=2 + i,
            revenue=8.25 + (i * 3),
            campaign='video-series'
        )
        tracker.add_metric(youtube_metric)
    
    # Get progress report
    print("\n" + "=" * 50)
    print("Revenue Progress Report")
    print("=" * 50)
    
    report = tracker.get_progress_report()
    
    print(f"\nTotal Revenue: ${report['total_revenue']:.2f}")
    print(f"\nQuick Target ($310):")
    print(f"  Progress: {report['quick_progress']:.1f}%")
    print(f"  Remaining: ${report['targets']['quick_remaining']:.2f}")
    
    print(f"\nMain Target ($8,700):")
    print(f"  Progress: {report['main_progress']:.1f}%")
    print(f"  Remaining: ${report['targets']['main_remaining']:.2f}")
    
    print(f"\nRevenue by Source:")
    print(f"  Amazon: ${report['revenue_by_source']['amazon']:.2f}")
    print(f"  YouTube: ${report['revenue_by_source']['youtube']:.2f}")
    
    print(f"\nConversion Metrics:")
    print(f"  Total Clicks: {report['metrics']['total_clicks']}")
    print(f"  Total Conversions: {report['metrics']['total_conversions']}")
    print(f"  Conversion Rate: {report['metrics']['conversion_rate']:.2f}%")
    
    # Daily breakdown
    print("\n" + "=" * 50)
    print("Daily Breakdown (Last 7 Days)")
    print("=" * 50)
    
    daily = tracker.get_daily_breakdown(days=7)
    for day in daily:
        print(f"{day['date']}: ${day['revenue']:.2f} ({day['conversions']} conversions)")
    
    # Predictions
    print("\n" + "=" * 50)
    print("Revenue Predictions")
    print("=" * 50)
    
    predictions = tracker.predict_target_date()
    print(f"\nAverage Daily Revenue: ${predictions['avg_daily_revenue']:.2f}")
    print(f"Quick Target Date: {predictions['quick_target_date']}")
    print(f"Main Target Date: {predictions['main_target_date']}")
    
    # Top campaigns
    print("\n" + "=" * 50)
    print("Top Campaigns")
    print("=" * 50)
    
    top_campaigns = tracker.get_top_campaigns(limit=3)
    for idx, campaign in enumerate(top_campaigns, 1):
        print(f"\n{idx}. {campaign['campaign']}")
        print(f"   Revenue: ${campaign['revenue']:.2f}")
        print(f"   Conversions: {campaign['conversions']}")
        print(f"   Clicks: {campaign['clicks']}")
    
    print("\n" + "=" * 50)
    print("✓ Revenue tracking complete!")

if __name__ == "__main__":
    main()
