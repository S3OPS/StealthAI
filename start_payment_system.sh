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
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_secret_here

# Cryptocurrency Wallet Addresses
BTC_WALLET_ADDRESS=your_bitcoin_address
ETH_WALLET_ADDRESS=your_ethereum_address

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
