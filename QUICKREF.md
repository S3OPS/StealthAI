# StealthAI Quick Reference

## Quick Start Commands

```bash
# Run full system
python stealth_ai.py

# Run examples
python examples/quick_start.py
python examples/batch_generation.py
python examples/revenue_tracking.py
```

## Configuration Template

```json
{
  "amazon_affiliate": {
    "tracking_id": "yourname-20"
  },
  "youtube": {
    "api_key": "YOUR_API_KEY",
    "channel_id": "YOUR_CHANNEL_ID"
  },
  "ai_tools": {
    "ollama_endpoint": "http://localhost:11434",
    "default_model": "llama2"
  }
}
```

## Core Concepts

### Signal Compression
- Filters data to top 30% by default
- Focuses on high-converting signals
- Threshold: 0.7 (70% confidence minimum)

### Micro-Stacking
- Parallel task execution (3 workers default)
- Priority-based scheduling
- Dependency management

## Revenue Targets

| Target | Amount | Strategy |
|--------|--------|----------|
| Quick  | $310   | 2-5 days, high-converting niches |
| Main   | $8,700 | 30-60 days, diversified content |

## Content Pipeline

```
Topic → Signal Compression → AI Generation → Optimization → Output
```

## Output Files

- Video scripts (faceless narration)
- YouTube metadata (title, description, tags)
- Product showcases (affiliate links)
- Upload schedules
- Revenue tracking

## Integrations

### Amazon Affiliate
- Link generation: `affiliate.generate_affiliate_link(asin)`
- Product showcases
- Comparison tables
- SEO optimization

### YouTube
- Metadata optimization
- Upload scheduling
- Series creation
- Thumbnail text generation

### AI Content
- Script generation
- Product reviews
- Metadata creation
- Conversion optimization

## Analytics

Track:
- Total revenue
- Revenue by source (Amazon, YouTube)
- Conversion rates
- Campaign performance
- Predictive modeling

## Best Practices

1. **Start Small** - Run quick strategy first ($310)
2. **Test Content** - Generate 1-2 packages to validate
3. **Monitor Metrics** - Track what converts
4. **Scale Gradually** - Move to main engine after validation
5. **Optimize Continuously** - Refine based on data

## Common Issues

### "Ollama connection refused"
- Install Ollama: `curl https://ollama.ai/install.sh | sh`
- Start server: `ollama serve`
- Or system will use template fallback

### "YouTube API error"
- Verify API key in config.json
- Check quota limits in Google Cloud Console

### "Amazon links not working"
- Verify tracking ID format (ends with -20)
- Ensure Associates agreement accepted

## File Structure

```
StealthAI/
├── stealth_ai.py          # Main execution engine
├── config.json            # Your configuration (create from example)
├── requirements.txt       # Dependencies
├── src/
│   ├── core/             # Signal compression, micro-stacking
│   ├── ai_engine/        # Content generation
│   ├── integrations/     # Amazon, YouTube
│   └── analytics/        # Revenue tracking
├── examples/             # Example scripts
└── docs/                 # Documentation
```

## API Requirements

- Amazon Associate tracking ID (free)
- YouTube Data API v3 key (free)
- Ollama (optional, free)

## Next Steps

1. Configure API keys in `config.json`
2. Run `python examples/quick_start.py`
3. Review generated content
4. Execute full system: `python stealth_ai.py`
5. Monitor revenue in analytics

---

**For full documentation, see:**
- [Setup Guide](docs/SETUP.md)
- [Architecture](docs/ARCHITECTURE.md)
- [README](README.md)
