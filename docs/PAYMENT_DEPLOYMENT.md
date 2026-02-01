# Payment System Deployment Guide

Complete guide for deploying the StealthAI payment system and landing page.

## 🚀 Quick Deployment (5 Minutes)

### Option 1: Local Testing

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Start payment server
./start_payment_system.sh

# 4. Open landing page
open landing_page/index.html
```

### Option 2: Production Deployment

Choose your preferred hosting platform below.

---

## 📋 Prerequisites

1. **Stripe Account** (FREE)
   - Sign up at https://stripe.com
   - Get your API keys from Dashboard > Developers > API keys
   - No monthly fees, just 2.9% + 30¢ per transaction

2. **Cryptocurrency Wallets** (Optional)
   - Bitcoin wallet address
   - Ethereum wallet address

3. **Domain Name** (Optional but recommended)
   - Can use free subdomains from hosting providers

---

## 🌐 Frontend Deployment (Landing Page)

### Option A: GitHub Pages (FREE, Easiest)

```bash
# 1. Create gh-pages branch
git checkout -b gh-pages

# 2. Copy landing page to root
cp -r landing_page/* .

# 3. Update API URL in assets/js/main.js
# Change API_BASE_URL to your deployed API URL

# 4. Commit and push
git add .
git commit -m "Deploy landing page"
git push origin gh-pages

# 5. Enable GitHub Pages in repository settings
# Settings > Pages > Source: gh-pages branch
```

Your landing page will be at: `https://yourusername.github.io/StealthAI`

### Option B: Netlify (FREE)

1. Install Netlify CLI:
```bash
npm install -g netlify-cli
```

2. Deploy:
```bash
cd landing_page
netlify deploy --prod
```

3. Follow prompts and your site will be live!

### Option C: Vercel (FREE)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
cd landing_page
vercel --prod
```

### Option D: Cloudflare Pages (FREE)

1. Push to GitHub
2. Go to Cloudflare Pages
3. Connect your repository
4. Set build settings:
   - Build command: (none)
   - Build output directory: `landing_page`
5. Deploy!

---

## 🔧 Backend Deployment (API Server)

### Option A: Railway (FREE Tier)

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd src/payment && python api_server.py",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

3. Create `Procfile`:
```
web: cd src/payment && python api_server.py
```

4. Deploy:
```bash
railway login
railway init
railway up
```

5. Add environment variables in Railway dashboard:
   - `STRIPE_SECRET_KEY`
   - `STRIPE_WEBHOOK_SECRET`
   - `BTC_WALLET_ADDRESS`
   - `ETH_WALLET_ADDRESS`

### Option B: Render (FREE Tier)

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: stealthai-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: cd src/payment && python api_server.py
    envVars:
      - key: STRIPE_SECRET_KEY
        sync: false
      - key: STRIPE_WEBHOOK_SECRET
        sync: false
```

2. Push to GitHub
3. Go to Render.com > New Web Service
4. Connect repository
5. Add environment variables
6. Deploy!

### Option C: Fly.io (FREE Tier)

1. Install Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Create `fly.toml`:
```toml
app = "stealthai-api"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

3. Deploy:
```bash
fly launch
fly secrets set STRIPE_SECRET_KEY=your_key
fly secrets set STRIPE_WEBHOOK_SECRET=your_secret
fly deploy
```

### Option D: DigitalOcean App Platform ($5/month)

1. Push to GitHub
2. Create new App in DigitalOcean
3. Connect repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `cd src/payment && python api_server.py`
5. Add environment variables
6. Deploy!

---

## 🔐 Environment Configuration

### Required Environment Variables

```bash
# Stripe (Required for credit card payments)
STRIPE_SECRET_KEY=sk_live_your_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Cryptocurrency (Optional)
BTC_WALLET_ADDRESS=your_bitcoin_wallet_address
ETH_WALLET_ADDRESS=your_ethereum_wallet_address

# Server (Optional)
API_HOST=0.0.0.0
API_PORT=5000
```

### Getting Stripe Keys

1. Go to https://dashboard.stripe.com/apikeys
2. Copy "Publishable key" → `STRIPE_PUBLISHABLE_KEY`
3. Click "Reveal test key" → `STRIPE_SECRET_KEY`
4. For production, use live keys instead of test keys

### Setting Up Webhooks

1. Go to https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Enter your endpoint URL: `https://your-api-url.com/webhook/stripe`
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
5. Copy "Signing secret" → `STRIPE_WEBHOOK_SECRET`

---

## 🧪 Testing

### Test Locally

1. Start API server:
```bash
./start_payment_system.sh
```

2. Open landing page:
```bash
# In another terminal
cd landing_page
python -m http.server 8000
```

3. Visit http://localhost:8000

### Test Stripe Integration

Use Stripe test cards:
- Success: `4242 4242 4242 4242`
- Requires authentication: `4000 0025 0000 3155`
- Declined: `4000 0000 0000 9995`

Use any future expiration date and any 3-digit CVC.

### Test Cryptocurrency

For testing, use testnet addresses or generate a test payment with a small amount.

---

## 📊 Monitoring

### Check API Health

```bash
curl https://your-api-url.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "stripe_available": true
}
```

### View Logs

**Railway:**
```bash
railway logs
```

**Render:**
Check Logs tab in dashboard

**Fly.io:**
```bash
fly logs
```

---

## 🔒 Security Best Practices

1. **Use HTTPS Only**
   - All hosting platforms provide free SSL
   - Never send API keys over HTTP

2. **Validate Webhook Signatures**
   - Already implemented in `webhook_handler.py`
   - Stripe signature verification prevents fraud

3. **Environment Variables**
   - Never commit API keys to git
   - Use platform environment variable management

4. **CORS Configuration**
   - Update CORS settings in `api_server.py`
   - Only allow your frontend domain

5. **Rate Limiting**
   - Consider adding rate limiting for production
   - Most platforms provide this built-in

---

## 🎯 Post-Deployment Checklist

- [ ] Frontend deployed and accessible
- [ ] Backend API deployed and accessible
- [ ] Stripe keys configured (live keys for production)
- [ ] Webhook endpoint added to Stripe dashboard
- [ ] Test payment flow end-to-end
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active (should be automatic)
- [ ] Update landing page with actual API URL
- [ ] Test license generation and activation
- [ ] Monitor first real payment

---

## 💰 Cost Summary

| Service | Cost | Notes |
|---------|------|-------|
| Stripe | FREE | 2.9% + 30¢ per transaction only |
| GitHub Pages | FREE | Static site hosting |
| Netlify | FREE | 100GB bandwidth/month |
| Railway | FREE | 500 hours/month |
| Render | FREE | 750 hours/month |
| Fly.io | FREE | 3 shared VMs |
| **Total** | **$0-5/month** | Scales with usage |

---

## 🚨 Troubleshooting

### Payment API Not Starting

```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies
pip install -r requirements.txt

# Check for errors
python src/payment/api_server.py
```

### Stripe Webhook Not Working

1. Check webhook URL is publicly accessible
2. Verify webhook secret in environment variables
3. Check Stripe dashboard for webhook delivery attempts
4. Review API logs for errors

### License Activation Fails

```bash
# Test license generation
python -c "
from src.payment.license_manager import LicenseManager
lm = LicenseManager()
license = lm.create_license('pro', 'test@example.com', 'test-payment-id')
print(license)
"
```

---

## 📞 Support

For deployment issues:
1. Check platform documentation
2. Review application logs
3. Test locally first
4. Check GitHub Issues

---

**Your payment system is ready for production!** 🎉

Choose your deployment platform and go live in under an hour.
