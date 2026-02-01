# StealthAI - Faceless Revenue Generation Engine

**Automated AI-powered content and monetization system using signal compression and micro-stacking architecture.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Dual Revenue Streams

1. **Content Revenue**: $310 quick (2-5 days) → $8,700/month sustained
2. **Software Sales**: $11K-$232K annually through automated licensing

## 🚀 Quick Start

### For Users (Content Generation)

```bash
# 1. Clone and install
git clone https://github.com/S3OPS/StealthAI.git
cd StealthAI
pip install -r requirements.txt

# 2. Activate your license
python stealth_ai.py --activate YOUR-LICENSE-KEY

# 3. Configure API keys
cp config.example.json config.json
# Edit config.json with your Amazon & YouTube keys

# 4. Run the system
python stealth_ai.py
```

### For Developers (Payment System)

```bash
# Start payment server & landing page
./start_payment_system.sh
```

## 🎯 Revenue Targets

- **Quick Target**: $310 (rapid deployment)
- **Main Target**: $8,700 (sustained engine)

## 🚀 Features

### Core Architecture
- **Signal Compression**: Filters and prioritizes high-value conversion signals
- **Micro-Stacking**: Parallel AI task execution with intelligent dependency management
- **Faceless Operation**: Fully automated, no personal branding required

### Integrations
- **Amazon Affiliate**: Automated affiliate link generation and product recommendations
- **YouTube API**: Video metadata optimization, scheduling, and series management
- **Free AI Tools**: Content generation via Ollama, LM Studio, or other local models

### Revenue System
- Real-time conversion tracking
- Multi-channel analytics
- Predictive revenue modeling
- Campaign performance optimization

## 📋 Requirements

- Python 3.8+
- Amazon Associate Account (with tracking ID)
- YouTube Data API v3 key
- Ollama or similar local AI model (optional, for AI content generation)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/S3OPS/StealthAI.git
cd StealthAI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your credentials:
```bash
cp config.example.json config.json
# Edit config.json with your API keys
```

## ⚙️ Configuration

Edit `config.json` with your credentials:

```json
{
  "amazon_affiliate": {
    "tracking_id": "your-affiliate-id-20"
  },
  "youtube": {
    "api_key": "YOUR_YOUTUBE_API_KEY",
    "channel_id": "YOUR_CHANNEL_ID"
  },
  "ai_tools": {
    "ollama_endpoint": "http://localhost:11434",
    "default_model": "llama2"
  }
}
```

### Amazon Affiliate Setup
1. Sign up at [Amazon Associates](https://affiliate-program.amazon.com/)
2. Get your tracking ID (format: `username-20`)
3. Add to config.json

### YouTube API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable YouTube Data API v3
3. Create API credentials (API key)
4. Add to config.json

### AI Tools Setup (Optional)
For local AI content generation:
1. Install [Ollama](https://ollama.ai/)
2. Pull a model: `ollama pull llama2`
3. Start Ollama server: `ollama serve`

## 🎬 Quick Start

### Run the complete system:
```bash
python stealth_ai.py
```

This will:
1. Generate faceless video content
2. Create optimized YouTube metadata
3. Generate Amazon affiliate product showcases
4. Create upload schedules
5. Track revenue progress

### Example Output:
```
[*] Executing Quick Revenue Strategy ($310 target)...
    Generated 2 content packages
    Upload schedule: 2 days

[*] Running Main Revenue Engine ($8.7K target)...
    Generated 4 content packages
    Series created with 4 videos
    Upload schedule: 8 days

[*] Sample Content Package:
    Topic: Tech Gadgets Under $50
    Title: Best Budget Tech Gadgets You Need in 2024
    Keywords: budget tech, affordable gadgets, tech deals
```

## 📚 Usage Examples

### Generate Single Content Package

```python
from stealth_ai import StealthAI

stealth = StealthAI()

# Generate faceless content
content = stealth.generate_faceless_content(
    topic="Best Budget Laptops 2024",
    keywords=["budget laptop", "cheap laptop", "affordable computing"],
    product_asins=["B08N5WRWNW", "B07ZPKN6YR"]
)

print(f"Title: {content['metadata']['title']}")
print(f"Description: {content['metadata']['description']}")
print(f"Script: {content['script']['script']}")
print(f"Products: {content['products']}")
```

### Create Content Pipeline

```python
# Define topics and keywords
topics = [
    "Smart Home Devices 2024",
    "Gaming Setup Essentials",
    "Photography Gear for Beginners"
]

keywords_map = {
    "Smart Home Devices 2024": ["smart home", "home automation", "iot"],
    "Gaming Setup Essentials": ["gaming setup", "pc gaming", "gaming gear"],
    "Photography Gear for Beginners": ["photography", "camera gear", "beginner photography"]
}

# Generate all content
content_packages = stealth.create_content_pipeline(
    topics=topics,
    keywords_per_topic=keywords_map
)
```

### Track Revenue

```python
from analytics import RevenueTracker, RevenueMetric
from datetime import datetime

tracker = RevenueTracker(quick_target=310, main_target=8700)

# Add revenue metric
metric = RevenueMetric(
    date=datetime.now().strftime('%Y-%m-%d'),
    source='amazon',
    clicks=150,
    conversions=8,
    revenue=45.50,
    campaign='tech-gadgets'
)
tracker.add_metric(metric)

# Get progress report
report = tracker.get_progress_report()
print(f"Total Revenue: ${report['total_revenue']}")
print(f"Progress to Quick Target: {report['quick_progress']:.1f}%")
```

## 🏗️ Architecture

### Signal Compression
Filters input data to focus on high-converting signals:
- Filters by strength threshold (default: 0.7)
- Compresses to top 30% of signals
- Prioritizes by conversion potential

### Micro-Stacking
Manages parallel AI task execution:
- Supports task dependencies
- Priority-based execution
- Parallel processing (configurable workers)
- Timeout management

### Content Generation Flow
```
Topic + Keywords → Signal Compression → AI Script Generation
                                      ↓
                    YouTube Metadata Optimization
                                      ↓
                    Amazon Affiliate Integration
                                      ↓
                    Complete Content Package
```

## 📊 Revenue Strategy

### Quick Strategy ($310 target)
- Focus: High-converting niche products
- Frequency: Daily uploads
- Duration: 2-5 days
- Content: Product reviews, comparisons

### Main Engine ($8.7K target)
- Focus: Diversified content series
- Frequency: Every 2 days
- Duration: 30-60 days
- Content: In-depth guides, series

## 💳 Payment System (NEW!)

StealthAI now includes a complete automated payment and licensing system!

### Features
- **Stripe Integration**: Accept credit cards (FREE tier, no monthly fees)
- **Cryptocurrency**: Bitcoin & Ethereum payments
- **Automated Licensing**: Instant license generation via webhooks
- **Professional Landing Page**: Dark-themed, mobile-responsive
- **3 Pricing Tiers**: Free trial, Pro ($97/mo), Enterprise ($297/mo)

### Quick Start

1. **Deploy Landing Page** (GitHub Pages, Netlify, Vercel - FREE)
2. **Deploy API Server** (Railway, Render, Fly.io - FREE)
3. **Configure Stripe** (Get API keys from dashboard.stripe.com)
4. **Start Selling!**

### Revenue Potential from Sales

| Scenario | Customers/Month | Revenue/Month | Revenue/Year |
|----------|-----------------|---------------|--------------|
| Conservative | 10 | $970 | $11,640 |
| Moderate | 50 | $4,850 | $58,200 |
| Aggressive | 200 | $19,400 | $232,800 |

**Total Revenue = Content ($8.7K) + Software Sales ($11K-$232K) = Dual Streams!**

### For End Users

Activate your license:
```bash
python stealth_ai.py --activate XXXX-XXXX-XXXX-XXXX
```

### For Developers

Deploy payment system:
```bash
./start_payment_system.sh
```

📖 **Full Guide**: See [docs/PAYMENT_DEPLOYMENT.md](docs/PAYMENT_DEPLOYMENT.md)

## 🔒 Security & Privacy

- API keys stored in local config.json (not committed)
- No data sent to third-party services (except configured APIs)
- All processing happens locally
- Affiliate disclosure included in generated content

## 📈 Performance Optimization

### Signal Compression Settings
```json
{
  "compression_ratio": 0.3,  // Keep top 30%
  "signal_threshold": 0.7    // Min 70% confidence
}
```

### Micro-Stacking Settings
```json
{
  "max_stack_depth": 5,      // Max batch size
  "parallel_tasks": 3,       // Concurrent workers
  "task_timeout": 300        // Task timeout (seconds)
}
```

## 🛠️ Advanced Features

### Custom AI Models
Configure alternative AI endpoints:
```json
{
  "ai_tools": {
    "ollama_endpoint": "http://localhost:11434",
    "default_model": "mistral",
    "fallback_models": ["llama2", "neural-chat"]
  }
}
```

### Custom Revenue Targets
```json
{
  "revenue_targets": {
    "quick_target": 500,
    "main_target": 10000
  }
}
```

## 📝 Content Types Generated

1. **Video Scripts** - Faceless narration-ready scripts
2. **YouTube Metadata** - Optimized titles, descriptions, tags
3. **Product Showcases** - Affiliate link compilations
4. **Upload Schedules** - Optimal posting times
5. **Thumbnail Text** - High-CTR overlay text

## 🎯 Use Cases

- Faceless YouTube channels
- Affiliate marketing automation
- Content series creation
- Product review channels
- Niche topic channels
- Tech review automation

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## ⚠️ Disclaimer

- This tool is for legitimate affiliate marketing
- Always follow Amazon Associates Operating Agreement
- Follow YouTube's Terms of Service
- Include proper affiliate disclosures
- Content should provide genuine value to viewers

## 🔗 Resources

- [Amazon Associates](https://affiliate-program.amazon.com/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Ollama](https://ollama.ai/)
- [FTC Affiliate Disclosure Guidelines](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)

## 💡 Tips for Success

1. **Start with Quick Strategy** - Reach $310 first to validate
2. **Quality Over Quantity** - Focus on high-converting niches
3. **Consistent Schedule** - Regular uploads build momentum
4. **Optimize Metadata** - Use provided optimization tools
5. **Track Everything** - Monitor which content converts
6. **Scale Gradually** - Move to main engine after proving concept

## 📞 Support

For issues or questions:
1. Check existing documentation
2. Review example code
3. Open an issue on GitHub

---

**Built with signal compression and micro-stacking for maximum efficiency** 🚀