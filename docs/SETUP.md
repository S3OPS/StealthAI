# StealthAI Setup Guide

This guide will help you set up and configure StealthAI for automated revenue generation.

## Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Amazon Associate Account**
   - Sign up at https://affiliate-program.amazon.com/
   - Complete the application process
   - Get your tracking ID (format: `username-20`)

3. **YouTube Account & API Access**
   - Create a Google Cloud Project
   - Enable YouTube Data API v3
   - Generate an API key

4. **Local AI Model** (Optional but recommended)
   - Install Ollama from https://ollama.ai/
   - Or use another compatible AI endpoint

## Installation Steps

### 1. Clone and Install

```bash
# Clone repository
git clone https://github.com/S3OPS/StealthAI.git
cd StealthAI

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Amazon Affiliate

1. Log into Amazon Associates
2. Navigate to Tools → Product Advertising API
3. Copy your tracking ID
4. (Optional) Register for Product Advertising API for advanced features

### 3. Configure YouTube API

1. Go to https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable YouTube Data API v3:
   - APIs & Services → Library
   - Search "YouTube Data API v3"
   - Click Enable
4. Create credentials:
   - APIs & Services → Credentials
   - Create Credentials → API Key
   - Copy the API key

### 4. Configure AI Tools

#### Option A: Ollama (Recommended)

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2

# Start Ollama server
ollama serve
```

#### Option B: Other AI Services
- Configure alternative endpoint in config.json
- Supported: Any OpenAI-compatible API

### 5. Create Configuration File

```bash
# Copy example config
cp config.example.json config.json

# Edit with your credentials
nano config.json  # or use your preferred editor
```

Example configuration:

```json
{
  "amazon_affiliate": {
    "tracking_id": "yourname-20",
    "access_key": "YOUR_ACCESS_KEY",
    "secret_key": "YOUR_SECRET_KEY",
    "region": "US"
  },
  "youtube": {
    "api_key": "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "channel_id": "UCxxxxxxxxxxxxxxxxxxxxxx"
  },
  "ai_tools": {
    "ollama_endpoint": "http://localhost:11434",
    "default_model": "llama2",
    "fallback_models": ["mistral", "neural-chat"]
  },
  "signal_compression": {
    "compression_ratio": 0.3,
    "signal_threshold": 0.7,
    "batch_size": 10
  },
  "micro_stacking": {
    "max_stack_depth": 5,
    "parallel_tasks": 3,
    "task_timeout": 300
  },
  "revenue_targets": {
    "quick_target": 310,
    "main_target": 8700
  }
}
```

## Verification

Test your setup:

```bash
# Run quick start example
python examples/quick_start.py
```

If successful, you should see:
```
✓ Content package ready for production!
```

## Troubleshooting

### Issue: "Ollama connection failed"
**Solution:** 
- Ensure Ollama is running: `ollama serve`
- Check endpoint in config.json
- Try: `curl http://localhost:11434/api/tags`

### Issue: "YouTube API error"
**Solution:**
- Verify API key is correct
- Check API is enabled in Google Cloud Console
- Verify quota limits haven't been exceeded

### Issue: "Import errors"
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "Amazon affiliate links not generating"
**Solution:**
- Verify tracking ID format (should end with -20)
- Check product ASINs are valid
- Ensure you've accepted Associates Operating Agreement

## Next Steps

1. **Test Content Generation**
   ```bash
   python examples/quick_start.py
   ```

2. **Generate Batch Content**
   ```bash
   python examples/batch_generation.py
   ```

3. **Track Revenue**
   ```bash
   python examples/revenue_tracking.py
   ```

4. **Run Full System**
   ```bash
   python stealth_ai.py
   ```

## Security Best Practices

1. **Never commit config.json**
   - Already in .gitignore
   - Contains sensitive API keys

2. **Use environment variables** (alternative)
   ```bash
   export AMAZON_TRACKING_ID="yourname-20"
   export YOUTUBE_API_KEY="your-key"
   ```

3. **Rotate API keys regularly**
   - YouTube: Regenerate in Cloud Console
   - Amazon: Update in Associates account

4. **Monitor API usage**
   - YouTube: Check quota in Cloud Console
   - Amazon: Monitor in Associates dashboard

## Performance Tuning

### For Faster Content Generation
```json
{
  "micro_stacking": {
    "parallel_tasks": 5  // Increase if you have more CPU cores
  }
}
```

### For Higher Quality Signals
```json
{
  "signal_compression": {
    "compression_ratio": 0.2,  // Keep only top 20%
    "signal_threshold": 0.8    // Higher threshold (80% confidence)
  }
}
```

### For Different AI Models
```json
{
  "ai_tools": {
    "default_model": "mistral",  // Faster alternative to llama2
    "fallback_models": ["llama2", "neural-chat"]
  }
}
```

## Support

If you encounter issues:

1. Check this guide first
2. Review example scripts in `/examples`
3. Check GitHub issues
4. Create new issue with:
   - Error message
   - Steps to reproduce
   - Your configuration (remove sensitive data)

## Updates

Keep StealthAI updated:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

**Ready to start generating revenue!** 🚀
