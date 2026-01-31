"""
Amazon Affiliate Integration
Generates affiliate links and product recommendations
"""

import hashlib
import hmac
import base64
import time
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import quote, urlencode
import requests

logger = logging.getLogger(__name__)


class AmazonAffiliate:
    """
    Amazon Affiliate link generator and product recommender.
    Helps monetize content with affiliate links.
    """
    
    def __init__(self, tracking_id: str, access_key: str = None, 
                 secret_key: str = None, region: str = "US"):
        """
        Initialize Amazon Affiliate integration.
        
        Args:
            tracking_id: Amazon Associate tracking ID
            access_key: Product Advertising API access key (optional)
            secret_key: Product Advertising API secret key (optional)
            region: Amazon region (US, UK, CA, etc.)
        """
        self.tracking_id = tracking_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.base_url = self._get_base_url()
        
    def _get_base_url(self) -> str:
        """Get Amazon base URL for region"""
        region_urls = {
            'US': 'https://www.amazon.com',
            'UK': 'https://www.amazon.co.uk',
            'CA': 'https://www.amazon.ca',
            'DE': 'https://www.amazon.de',
            'FR': 'https://www.amazon.fr',
            'JP': 'https://www.amazon.co.jp'
        }
        return region_urls.get(self.region, region_urls['US'])
    
    def generate_affiliate_link(self, product_url: str, campaign: str = None) -> str:
        """
        Generate an affiliate link for a product.
        
        Args:
            product_url: Original Amazon product URL or ASIN
            campaign: Optional campaign tag for tracking
            
        Returns:
            Affiliate link with tracking ID
        """
        # Extract ASIN if full URL provided
        asin = self._extract_asin(product_url)
        
        if not asin:
            logger.warning(f"Could not extract ASIN from: {product_url}")
            return product_url
        
        # Build affiliate link
        params = {
            'tag': self.tracking_id
        }
        
        if campaign:
            params['campaign'] = campaign
        
        link = f"{self.base_url}/dp/{asin}?{urlencode(params)}"
        
        logger.info(f"Generated affiliate link for ASIN {asin}")
        return link
    
    def _extract_asin(self, url_or_asin: str) -> Optional[str]:
        """Extract ASIN from URL or validate ASIN"""
        # If it's already an ASIN (10 characters alphanumeric)
        if len(url_or_asin) == 10 and url_or_asin.isalnum():
            return url_or_asin
        
        # Try to extract from URL
        patterns = ['/dp/', '/gp/product/', '/ASIN/']
        for pattern in patterns:
            if pattern in url_or_asin:
                try:
                    start = url_or_asin.index(pattern) + len(pattern)
                    asin = url_or_asin[start:start+10]
                    if asin.isalnum():
                        return asin
                except:
                    continue
        
        return None
    
    def create_product_showcase(self, products: List[Dict[str, str]], 
                               title: str = "Recommended Products") -> str:
        """
        Create a formatted product showcase with affiliate links.
        
        Args:
            products: List of product dicts with 'name', 'url', 'description'
            title: Showcase title
            
        Returns:
            Formatted HTML/Markdown showcase
        """
        showcase = f"## {title}\n\n"
        
        for idx, product in enumerate(products, 1):
            affiliate_link = self.generate_affiliate_link(product['url'])
            showcase += f"{idx}. **{product['name']}**\n"
            showcase += f"   {product.get('description', '')}\n"
            showcase += f"   [Check Price on Amazon]({affiliate_link})\n\n"
        
        return showcase
    
    def get_product_recommendations(self, category: str, keywords: List[str],
                                   max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Get product recommendations based on category and keywords.
        Note: This is a simplified version. Full implementation would use 
        Product Advertising API.
        
        Args:
            category: Product category
            keywords: Search keywords
            max_results: Maximum number of results
            
        Returns:
            List of product recommendations
        """
        # Simplified product database - in production, use API
        sample_products = self._get_sample_products(category, keywords)
        
        recommendations = []
        for product in sample_products[:max_results]:
            recommendations.append({
                'name': product['name'],
                'asin': product['asin'],
                'category': category,
                'affiliate_link': self.generate_affiliate_link(product['asin']),
                'estimated_price': product.get('price', 'Check Amazon'),
                'keywords': keywords
            })
        
        logger.info(f"Generated {len(recommendations)} product recommendations")
        return recommendations
    
    def _get_sample_products(self, category: str, keywords: List[str]) -> List[Dict[str, Any]]:
        """Get sample products - placeholder for API integration"""
        # This would be replaced with actual Product Advertising API calls
        # For now, return template structure
        return [
            {
                'name': f"{category} Product - {kw}",
                'asin': f'B0{hash(kw) % 100000000:08d}',
                'price': '$XX.XX'
            }
            for kw in keywords[:5]
        ]
    
    def generate_comparison_table(self, products: List[Dict[str, Any]]) -> str:
        """
        Generate a product comparison table.
        
        Args:
            products: List of products to compare
            
        Returns:
            Markdown comparison table
        """
        if not products:
            return ""
        
        table = "| Product | Key Features | Price | Link |\n"
        table += "|---------|--------------|-------|------|\n"
        
        for product in products:
            name = product.get('name', 'Product')
            features = product.get('features', ['N/A'])[:2]
            features_str = ', '.join(features)
            price = product.get('estimated_price', 'Check Amazon')
            link = self.generate_affiliate_link(product.get('asin', product.get('url', '')))
            
            table += f"| {name} | {features_str} | {price} | [View]({link}) |\n"
        
        return table
    
    def optimize_for_seo(self, content: str, products: List[str]) -> str:
        """
        Optimize content with strategic affiliate link placement.
        
        Args:
            content: Original content
            products: List of product ASINs to link
            
        Returns:
            SEO-optimized content with affiliate links
        """
        optimized = content
        
        for asin in products:
            link = self.generate_affiliate_link(asin)
            # Add affiliate disclosure
            if 'affiliate' not in optimized.lower():
                disclosure = "\n\n*Disclosure: This post contains affiliate links. We may earn a commission at no extra cost to you.*\n\n"
                optimized = disclosure + optimized
        
        return optimized
    
    def track_conversions(self, campaign: str) -> Dict[str, Any]:
        """
        Track conversion metrics for a campaign.
        Note: Actual tracking requires Amazon Associates reporting API.
        
        Args:
            campaign: Campaign identifier
            
        Returns:
            Conversion metrics
        """
        # Placeholder - would integrate with Amazon reporting
        return {
            'campaign': campaign,
            'clicks': 0,
            'conversions': 0,
            'revenue': 0.0,
            'note': 'Integrate Amazon Associates reporting API for real data'
        }
