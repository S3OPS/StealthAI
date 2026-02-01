#!/bin/bash
# StealthAI Payment System Startup Script

echo "╔════════════════════════════════════════════════════════╗"
echo "║        StealthAI Payment System Startup               ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cat > .env << EOL
# Stripe Configuration - Get keys from: https://dashboard.stripe.com/apikeys
STRIPE_SECRET_KEY=REPLACE_WITH_YOUR_STRIPE_SECRET_KEY
STRIPE_PUBLISHABLE_KEY=REPLACE_WITH_YOUR_STRIPE_PUBLISHABLE_KEY
STRIPE_WEBHOOK_SECRET=REPLACE_WITH_YOUR_WEBHOOK_SECRET

# Cryptocurrency Wallet Addresses
BTC_WALLET_ADDRESS=REPLACE_WITH_YOUR_BITCOIN_ADDRESS
ETH_WALLET_ADDRESS=REPLACE_WITH_YOUR_ETHEREUM_ADDRESS

# Server Configuration
API_HOST=0.0.0.0
API_PORT=5000
EOL
    echo "✅ Created .env file. Please update with your API keys."
    echo ""
fi

# Start payment API server
echo "🚀 Starting payment API server..."
echo "   API will be available at: http://localhost:5000"
echo "   Landing page at: landing_page/index.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd src/payment
python -m api_server

# Deactivate virtual environment on exit
deactivate
