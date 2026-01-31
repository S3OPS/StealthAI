"""
Signal Compression Module
Efficiently compresses and prioritizes data signals for AI processing
"""

from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class SignalCompressor:
    """
    Compresses input signals to focus on high-value data points.
    Reduces noise and prioritizes converting signals.
    """
    
    def __init__(self, compression_ratio: float = 0.3, threshold: float = 0.7):
        """
        Initialize signal compressor.
        
        Args:
            compression_ratio: Percentage of data to retain (0.3 = keep top 30%)
            threshold: Minimum signal strength to consider (0.7 = 70% confidence)
        """
        self.compression_ratio = compression_ratio
        self.threshold = threshold
        
    def compress_signals(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Compress signals by filtering and ranking based on conversion potential.
        
        Args:
            signals: List of signal dictionaries with 'value', 'strength', 'metadata'
            
        Returns:
            Compressed list of high-value signals
        """
        if not signals:
            return []
        
        # Filter by threshold
        filtered = [s for s in signals if s.get('strength', 0) >= self.threshold]
        
        if not filtered:
            logger.warning("No signals met threshold, using top signals")
            filtered = sorted(signals, key=lambda x: x.get('strength', 0), reverse=True)
            filtered = filtered[:max(1, int(len(signals) * self.compression_ratio))]
        
        # Sort by strength and keep top percentage
        filtered.sort(key=lambda x: x.get('strength', 0), reverse=True)
        keep_count = max(1, int(len(filtered) * self.compression_ratio))
        
        compressed = filtered[:keep_count]
        
        logger.info(f"Compressed {len(signals)} signals to {len(compressed)} high-value signals")
        return compressed
    
    def calculate_signal_strength(self, data: Dict[str, Any]) -> float:
        """
        Calculate signal strength based on conversion indicators.
        
        Args:
            data: Signal data with metrics
            
        Returns:
            Signal strength score (0-1)
        """
        factors = {
            'engagement_rate': data.get('engagement', 0) * 0.3,
            'click_through': data.get('ctr', 0) * 0.3,
            'conversion_rate': data.get('conversion', 0) * 0.4
        }
        
        strength = sum(factors.values())
        return min(1.0, max(0.0, strength))
    
    def prioritize_keywords(self, keywords: List[str], metrics: Dict[str, float]) -> List[Tuple[str, float]]:
        """
        Prioritize keywords based on conversion potential.
        
        Args:
            keywords: List of keywords to evaluate
            metrics: Dictionary mapping keywords to performance metrics
            
        Returns:
            List of (keyword, score) tuples sorted by priority
        """
        scored = [(kw, metrics.get(kw, 0.0)) for kw in keywords]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Apply compression
        keep_count = max(1, int(len(scored) * self.compression_ratio))
        return scored[:keep_count]
