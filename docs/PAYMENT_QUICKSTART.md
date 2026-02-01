# StealthAI Payment System - Quick Start

## Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install stripe flask flask-cors
```

### 2. Configure Stripe
Get free API keys from https://stripe.com/

Create `.env` file (**Important: Add to .gitignore!**):
```bash
STRIPE_API_KEY=your_test_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret
```

**Security Note:** Never commit `.env` to version control. Ensure `.env` is listed
in your `.gitignore` file.

### 3. Start Services
```bash
# Terminal 1: API Server
python src/payment/api_server.py

# Terminal 2: Landing Page  
cd landing_page && python -m http.server 8000

# Visit: http://localhost:8000
```

## Get Your License

**Free Trial:**
```bash
curl -X POST http://localhost:5000/api/payment/free-trial \
  -H "Content-Type: application/json" \
  -d '{"email": "your@email.com"}'
```

**Activate:**
```bash
python stealth_ai.py --activate XXXX-XXXX-XXXX-XXXX
```

## Full Documentation

Full implementation files and detailed guides are documented in this session.
To access complete setup and deployment instructions:

- Implementation Details: `docs/PAYMENT_SYSTEM.md`
- Session History: Review this GitHub Copilot session

Once implementation files are restored from session history, comprehensive
guides will be available covering setup, deployment, testing, and API usage.

## Revenue Potential

- 10 customers = $970/month
- 50 customers = $4,850/month
- 200 customers = $19,400/month

Plus StealthAI content revenue!
