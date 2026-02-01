"""
Payment API Server
Flask REST API for payment processing
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from .stripe_handler import StripeHandler, STRIPE_AVAILABLE
from .crypto_handler import CryptoHandler
from .license_manager import LicenseManager
from .webhook_handler import WebhookHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web integration

# Initialize payment handlers
license_manager = LicenseManager()
webhook_handler = WebhookHandler(license_manager)

# Initialize Stripe if available
stripe_handler = None
if STRIPE_AVAILABLE:
    try:
        stripe_handler = StripeHandler()
    except ImportError:
        logger.warning("Stripe handler not initialized")

crypto_handler = CryptoHandler()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'stripe_available': stripe_handler is not None
    })


@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create Stripe checkout session"""
    if not stripe_handler:
        return jsonify({'error': 'Stripe not configured'}), 503
    
    data = request.json
    plan = data.get('plan')
    email = data.get('email')
    
    if not plan:
        return jsonify({'error': 'Plan is required'}), 400
    
    try:
        # Get base URL from request
        base_url = request.host_url.rstrip('/')
        
        session_data = stripe_handler.create_checkout_session(
            plan=plan,
            success_url=f"{base_url}/success.html?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{base_url}",
            customer_email=email
        )
        
        return jsonify(session_data)
        
    except Exception as e:
        logger.error(f"Error creating checkout session: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/crypto-payment', methods=['POST'])
def create_crypto_payment():
    """Create cryptocurrency payment request"""
    data = request.json
    plan = data.get('plan')
    currency = data.get('currency', 'BTC')
    
    if not plan:
        return jsonify({'error': 'Plan is required'}), 400
    
    try:
        payment_request = crypto_handler.create_payment_request(plan, currency)
        return jsonify(payment_request)
        
    except Exception as e:
        logger.error(f"Error creating crypto payment: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/verify-crypto-payment', methods=['POST'])
def verify_crypto_payment():
    """Verify cryptocurrency payment"""
    data = request.json
    payment_id = data.get('payment_id')
    transaction_hash = data.get('transaction_hash')
    email = data.get('email')
    
    if not all([payment_id, transaction_hash, email]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        verification = crypto_handler.verify_payment(payment_id, transaction_hash)
        
        if verification['verified']:
            # Generate license
            result = webhook_handler.handle_crypto_payment({
                'transaction_hash': transaction_hash,
                'plan': data.get('plan', 'pro'),
                'email': email
            })
            
            return jsonify(result)
        else:
            return jsonify(verification), 400
            
    except Exception as e:
        logger.error(f"Error verifying crypto payment: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate-license', methods=['POST'])
def validate_license():
    """Validate a license key"""
    data = request.json
    license_key = data.get('license_key')
    machine_id = data.get('machine_id')
    
    if not license_key:
        return jsonify({'error': 'License key is required'}), 400
    
    try:
        result = license_manager.validate_license(license_key, machine_id)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error validating license: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/activate-license', methods=['POST'])
def activate_license():
    """Activate a license on a machine"""
    data = request.json
    license_key = data.get('license_key')
    machine_id = data.get('machine_id')
    
    if not all([license_key, machine_id]):
        return jsonify({'error': 'License key and machine ID are required'}), 400
    
    try:
        result = license_manager.activate_license(license_key, machine_id)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error activating license: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    if not stripe_handler:
        return jsonify({'error': 'Stripe not configured'}), 503
    
    payload = request.data
    signature = request.headers.get('Stripe-Signature')
    
    if not signature:
        return jsonify({'error': 'No signature provided'}), 400
    
    try:
        event = stripe_handler.verify_webhook_signature(payload, signature)
        result = webhook_handler.handle_stripe_webhook(event)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/api/license-info/<license_key>', methods=['GET'])
def get_license_info(license_key):
    """Get license information"""
    try:
        info = license_manager.get_license_info(license_key)
        
        if not info:
            return jsonify({'error': 'License not found'}), 404
        
        # Remove sensitive info
        safe_info = {
            'plan': info['plan'],
            'status': info['status'],
            'expires_at': info['expires_at'],
            'created_at': info['created_at']
        }
        
        return jsonify(safe_info)
        
    except Exception as e:
        logger.error(f"Error getting license info: {str(e)}")
        return jsonify({'error': str(e)}), 500


def run_server(host='0.0.0.0', port=5000, debug=False):
    """
    Run the payment API server.
    
    Args:
        host: Host to bind to
        port: Port to listen on
        debug: Enable debug mode
    """
    logger.info(f"Starting payment API server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server(debug=True)
