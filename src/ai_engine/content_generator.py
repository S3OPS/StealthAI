"""
AI Engine Module
Interfaces with free AI tools for content generation
"""

import requests
import logging
from typing import List, Dict, Any, Optional
import json

logger = logging.getLogger(__name__)


class AIEngine:
    """
    AI Engine for content generation using free tools.
    Supports local models via Ollama and other free APIs.
    """
    
    def __init__(self, endpoint: str = "http://localhost:11434", default_model: str = "llama2"):
        """
        Initialize AI engine.
        
        Args:
            endpoint: Ollama API endpoint
            default_model: Default model to use
        """
        self.endpoint = endpoint
        self.default_model = default_model
        self.fallback_models = ["mistral", "neural-chat", "llama2"]
        
    def generate_content(self, prompt: str, model: Optional[str] = None, 
                        max_length: int = 500) -> str:
        """
        Generate content using AI model.
        
        Args:
            prompt: Text prompt for generation
            model: Model to use (defaults to default_model)
            max_length: Maximum length of generated content
            
        Returns:
            Generated text content
        """
        model = model or self.default_model
        
        try:
            response = self._call_ollama(prompt, model, max_length)
            return response
        except Exception as e:
            logger.error(f"Error with model {model}: {str(e)}")
            # Try fallback models
            for fallback in self.fallback_models:
                if fallback != model:
                    try:
                        return self._call_ollama(prompt, fallback, max_length)
                    except:
                        continue
            
            # If all fails, return a basic template
            logger.warning("All AI models failed, using template")
            return self._generate_template(prompt)
    
    def _call_ollama(self, prompt: str, model: str, max_length: int) -> str:
        """Call Ollama API for generation"""
        try:
            url = f"{self.endpoint}/api/generate"
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_length
                }
            }
            
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '')
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API call failed: {str(e)}")
            raise
    
    def _generate_template(self, prompt: str) -> str:
        """Generate template-based content when AI is unavailable"""
        return f"Content based on: {prompt[:100]}..."
    
    def generate_video_script(self, topic: str, keywords: List[str], 
                             duration_minutes: int = 10) -> Dict[str, Any]:
        """
        Generate a faceless video script.
        
        Args:
            topic: Main topic for the video
            keywords: SEO keywords to include
            duration_minutes: Target video duration
            
        Returns:
            Dictionary with script sections
        """
        prompt = f"""Create a {duration_minutes}-minute faceless video script about {topic}.
Include these keywords naturally: {', '.join(keywords)}.
Format: Introduction, Main Points (3-5), Conclusion.
Make it engaging and suitable for voiceover narration."""

        script_text = self.generate_content(prompt, max_length=1500)
        
        return {
            'topic': topic,
            'duration': duration_minutes,
            'keywords': keywords,
            'script': script_text,
            'sections': self._parse_script_sections(script_text)
        }
    
    def _parse_script_sections(self, script: str) -> Dict[str, str]:
        """Parse script into sections"""
        sections = {
            'intro': '',
            'main': '',
            'conclusion': ''
        }
        
        # Simple parsing - can be enhanced
        parts = script.split('\n\n')
        if len(parts) >= 3:
            sections['intro'] = parts[0]
            sections['main'] = '\n\n'.join(parts[1:-1])
            sections['conclusion'] = parts[-1]
        else:
            sections['main'] = script
        
        return sections
    
    def generate_product_review(self, product_name: str, features: List[str],
                                price_range: str) -> str:
        """
        Generate a product review for affiliate marketing.
        
        Args:
            product_name: Name of the product
            features: List of product features
            price_range: Price range (e.g., "$50-$100")
            
        Returns:
            Product review text
        """
        prompt = f"""Write an honest, helpful review of {product_name}.
Key features: {', '.join(features)}.
Price range: {price_range}.
Include pros, cons, and who would benefit from this product.
Keep it natural and authentic."""

        return self.generate_content(prompt, max_length=800)
    
    def generate_youtube_metadata(self, topic: str, keywords: List[str]) -> Dict[str, Any]:
        """
        Generate YouTube video metadata (title, description, tags).
        
        Args:
            topic: Video topic
            keywords: SEO keywords
            
        Returns:
            Dictionary with title, description, tags
        """
        title_prompt = f"Create a compelling YouTube video title about {topic} using keywords: {', '.join(keywords[:3])}. Max 60 characters."
        title = self.generate_content(title_prompt, max_length=100).strip().split('\n')[0][:60]
        
        desc_prompt = f"""Create a YouTube video description for a video about {topic}.
Include keywords: {', '.join(keywords)}.
Include relevant hashtags and call-to-action.
Make it SEO-friendly."""
        description = self.generate_content(desc_prompt, max_length=500)
        
        tags = keywords[:15]  # YouTube allows max 500 characters of tags
        
        return {
            'title': title,
            'description': description,
            'tags': tags,
            'category': 22  # People & Blogs - can be customized
        }
    
    def optimize_for_conversion(self, content: str, call_to_action: str) -> str:
        """
        Optimize content for conversion with affiliate links.
        
        Args:
            content: Original content
            call_to_action: CTA to include
            
        Returns:
            Optimized content
        """
        prompt = f"""Optimize this content for conversion:

{content}

Add this call-to-action naturally: {call_to_action}
Make it persuasive but authentic."""

        return self.generate_content(prompt, max_length=800)
