"""
Revenue Analytics Module
Tracks conversions and revenue generation
"""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import json

logger = logging.getLogger(__name__)


@dataclass
class RevenueMetric:
    """Revenue tracking metric"""
    date: str
    source: str  # 'amazon', 'youtube', 'other'
    clicks: int
    conversions: int
    revenue: float
    campaign: str = ""


class RevenueTracker:
    """
    Tracks revenue generation and conversion metrics.
    Monitors progress toward revenue targets.
    """
    
    def __init__(self, quick_target: float = 310, main_target: float = 8700):
        """
        Initialize revenue tracker.
        
        Args:
            quick_target: Initial revenue target ($310)
            main_target: Main revenue target ($8700)
        """
        self.quick_target = quick_target
        self.main_target = main_target
        self.metrics: List[RevenueMetric] = []
        
    def add_metric(self, metric: RevenueMetric):
        """Add a revenue metric"""
        self.metrics.append(metric)
        logger.info(f"Added metric: {metric.source} - ${metric.revenue}")
    
    def get_total_revenue(self, source: str = None, 
                         days: int = None) -> float:
        """
        Calculate total revenue.
        
        Args:
            source: Filter by source (optional)
            days: Only count last N days (optional)
            
        Returns:
            Total revenue
        """
        filtered_metrics = self.metrics
        
        if source:
            filtered_metrics = [m for m in filtered_metrics if m.source == source]
        
        if days:
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            filtered_metrics = [m for m in filtered_metrics if m.date >= cutoff_date]
        
        return sum(m.revenue for m in filtered_metrics)
    
    def get_progress_report(self) -> Dict[str, Any]:
        """
        Generate progress report toward targets.
        
        Returns:
            Progress report with metrics
        """
        total_revenue = self.get_total_revenue()
        
        quick_progress = min(100, (total_revenue / self.quick_target) * 100)
        main_progress = min(100, (total_revenue / self.main_target) * 100)
        
        # Calculate by source
        amazon_revenue = self.get_total_revenue(source='amazon')
        youtube_revenue = self.get_total_revenue(source='youtube')
        
        # Calculate conversion rates
        total_clicks = sum(m.clicks for m in self.metrics)
        total_conversions = sum(m.conversions for m in self.metrics)
        conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        
        report = {
            'total_revenue': total_revenue,
            'quick_target': self.quick_target,
            'main_target': self.main_target,
            'quick_progress': quick_progress,
            'main_progress': main_progress,
            'revenue_by_source': {
                'amazon': amazon_revenue,
                'youtube': youtube_revenue
            },
            'metrics': {
                'total_clicks': total_clicks,
                'total_conversions': total_conversions,
                'conversion_rate': conversion_rate
            },
            'targets': {
                'quick_remaining': max(0, self.quick_target - total_revenue),
                'main_remaining': max(0, self.main_target - total_revenue)
            }
        }
        
        return report
    
    def get_daily_breakdown(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get daily revenue breakdown.
        
        Args:
            days: Number of days to include
            
        Returns:
            List of daily metrics
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        recent_metrics = [m for m in self.metrics if m.date >= cutoff_date]
        
        # Group by date
        daily_data = {}
        for metric in recent_metrics:
            if metric.date not in daily_data:
                daily_data[metric.date] = {
                    'date': metric.date,
                    'revenue': 0,
                    'clicks': 0,
                    'conversions': 0
                }
            daily_data[metric.date]['revenue'] += metric.revenue
            daily_data[metric.date]['clicks'] += metric.clicks
            daily_data[metric.date]['conversions'] += metric.conversions
        
        return sorted(daily_data.values(), key=lambda x: x['date'])
    
    def predict_target_date(self) -> Dict[str, str]:
        """
        Predict when targets will be reached based on current trend.
        
        Returns:
            Predicted dates for reaching targets
        """
        if len(self.metrics) < 2:
            return {
                'quick_target_date': 'Insufficient data',
                'main_target_date': 'Insufficient data'
            }
        
        # Calculate average daily revenue from last 7 days
        daily_breakdown = self.get_daily_breakdown(days=7)
        if not daily_breakdown:
            avg_daily = 0
        else:
            avg_daily = sum(d['revenue'] for d in daily_breakdown) / len(daily_breakdown)
        
        if avg_daily <= 0:
            return {
                'quick_target_date': 'No revenue trend',
                'main_target_date': 'No revenue trend'
            }
        
        total_revenue = self.get_total_revenue()
        
        # Calculate days to reach targets
        quick_remaining = max(0, self.quick_target - total_revenue)
        main_remaining = max(0, self.main_target - total_revenue)
        
        days_to_quick = int(quick_remaining / avg_daily) if avg_daily > 0 else 999
        days_to_main = int(main_remaining / avg_daily) if avg_daily > 0 else 999
        
        quick_date = (datetime.now() + timedelta(days=days_to_quick)).strftime('%Y-%m-%d')
        main_date = (datetime.now() + timedelta(days=days_to_main)).strftime('%Y-%m-%d')
        
        return {
            'quick_target_date': quick_date if total_revenue < self.quick_target else 'Achieved',
            'main_target_date': main_date if total_revenue < self.main_target else 'Achieved',
            'avg_daily_revenue': avg_daily
        }
    
    def get_top_campaigns(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get top performing campaigns.
        
        Args:
            limit: Number of campaigns to return
            
        Returns:
            List of top campaigns by revenue
        """
        # Group by campaign
        campaigns = {}
        for metric in self.metrics:
            campaign = metric.campaign or 'uncategorized'
            if campaign not in campaigns:
                campaigns[campaign] = {
                    'campaign': campaign,
                    'revenue': 0,
                    'clicks': 0,
                    'conversions': 0
                }
            campaigns[campaign]['revenue'] += metric.revenue
            campaigns[campaign]['clicks'] += metric.clicks
            campaigns[campaign]['conversions'] += metric.conversions
        
        # Sort by revenue
        sorted_campaigns = sorted(
            campaigns.values(),
            key=lambda x: x['revenue'],
            reverse=True
        )
        
        return sorted_campaigns[:limit]
    
    def export_metrics(self, filepath: str):
        """
        Export metrics to JSON file.
        
        Args:
            filepath: Path to save metrics
        """
        data = {
            'targets': {
                'quick': self.quick_target,
                'main': self.main_target
            },
            'metrics': [asdict(m) for m in self.metrics],
            'summary': self.get_progress_report()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Exported metrics to {filepath}")
    
    def import_metrics(self, filepath: str):
        """
        Import metrics from JSON file.
        
        Args:
            filepath: Path to metrics file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.quick_target = data['targets']['quick']
        self.main_target = data['targets']['main']
        
        self.metrics = [
            RevenueMetric(**m) for m in data['metrics']
        ]
        
        logger.info(f"Imported {len(self.metrics)} metrics from {filepath}")
