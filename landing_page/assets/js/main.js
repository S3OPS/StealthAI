// StealthAI Landing Page JavaScript

// Configuration
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000'
    : 'https://api.stealthai.com';  // Update with your deployed API URL

// IMPORTANT: Replace with your actual Stripe publishable key before deploying!
// Get your key from: https://dashboard.stripe.com/apikeys
// Test key format: pk_test_... | Live key format: pk_live_...
const stripe = Stripe('pk_test_REPLACE_WITH_YOUR_ACTUAL_STRIPE_KEY');  // TODO: REPLACE THIS!

// FAQ Toggle
function toggleFAQ(element) {
    const faqItem = element.parentElement;
    faqItem.classList.toggle('active');
}

// Start Free Trial
function startTrial() {
    // Redirect to activation flow or show trial license
    alert('Free trial will be implemented with license generation!');
    // In production: Generate trial license key
}

// Select Payment Plan
async function selectPlan(plan) {
    const planName = plan.charAt(0).toUpperCase() + plan.slice(1);
    
    // Show loading state
    const button = event.target;
    const originalText = button.textContent;
    button.textContent = 'Processing...';
    button.disabled = true;
    
    try {
        // Show payment method selection
        const paymentMethod = await showPaymentMethodSelection(planName);
        
        if (paymentMethod === 'stripe') {
            await processStripePayment(plan);
        } else if (paymentMethod === 'crypto') {
            await processCryptoPayment(plan);
        }
    } catch (error) {
        console.error('Payment error:', error);
        alert('Payment failed. Please try again.');
    } finally {
        button.textContent = originalText;
        button.disabled = false;
    }
}

// Show Payment Method Selection
function showPaymentMethodSelection(planName) {
    return new Promise((resolve) => {
        const choice = confirm(
            `Purchase ${planName} Plan\n\n` +
            'Choose payment method:\n' +
            'OK = Credit Card (Stripe)\n' +
            'Cancel = Cryptocurrency'
        );
        resolve(choice ? 'stripe' : 'crypto');
    });
}

// Process Stripe Payment
async function processStripePayment(plan) {
    try {
        // Create checkout session
        const response = await fetch(`${API_BASE_URL}/api/create-checkout-session`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                plan: plan,
                email: prompt('Enter your email address:') || ''
            }),
        });
        
        if (!response.ok) {
            throw new Error('Failed to create checkout session');
        }
        
        const session = await response.json();
        
        // Redirect to Stripe Checkout
        const result = await stripe.redirectToCheckout({
            sessionId: session.session_id,
        });
        
        if (result.error) {
            throw new Error(result.error.message);
        }
    } catch (error) {
        console.error('Stripe payment error:', error);
        throw error;
    }
}

// Process Cryptocurrency Payment
async function processCryptoPayment(plan) {
    try {
        // Choose cryptocurrency
        const currency = confirm('Bitcoin (OK) or Ethereum (Cancel)?') ? 'BTC' : 'ETH';
        
        // Create crypto payment request
        const response = await fetch(`${API_BASE_URL}/api/crypto-payment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                plan: plan,
                currency: currency
            }),
        });
        
        if (!response.ok) {
            throw new Error('Failed to create crypto payment');
        }
        
        const paymentData = await response.json();
        
        // Show crypto payment modal
        showCryptoPaymentModal(paymentData, plan);
        
    } catch (error) {
        console.error('Crypto payment error:', error);
        throw error;
    }
}

// Show Crypto Payment Modal
function showCryptoPaymentModal(paymentData, plan) {
    const modal = document.getElementById('cryptoModal');
    const detailsDiv = document.getElementById('cryptoPaymentDetails');
    
    detailsDiv.innerHTML = `
        <div style="text-align: center;">
            <h3>Send ${paymentData.currency} Payment</h3>
            <p style="margin: 1rem 0;">Amount: <strong>${paymentData.crypto_amount} ${paymentData.currency}</strong></p>
            <p style="margin: 1rem 0; color: var(--text-secondary);">(≈ $${paymentData.usd_amount} USD)</p>
            
            <div style="background: white; padding: 1rem; border-radius: 0.5rem; margin: 1.5rem 0;">
                <div style="font-family: monospace; word-break: break-all; color: #000; font-size: 0.875rem;">
                    ${paymentData.address}
                </div>
            </div>
            
            <p style="color: var(--text-secondary); font-size: 0.875rem; margin: 1rem 0;">
                Scan QR code or copy address above
            </p>
            
            <div style="margin-top: 2rem;">
                <button onclick="copyToClipboard('${paymentData.address}')" class="btn btn-secondary">
                    Copy Address
                </button>
            </div>
            
            <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--border);">
                <p style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 1rem;">
                    After sending payment, enter transaction hash:
                </p>
                <input type="text" id="txHash" placeholder="Transaction Hash" 
                    style="width: 100%; padding: 0.75rem; background: var(--bg-dark); border: 1px solid var(--border); border-radius: 0.5rem; color: var(--text-primary); margin-bottom: 1rem;">
                <input type="email" id="userEmail" placeholder="Your Email" 
                    style="width: 100%; padding: 0.75rem; background: var(--bg-dark); border: 1px solid var(--border); border-radius: 0.5rem; color: var(--text-primary); margin-bottom: 1rem;">
                <button onclick="verifyCryptoPayment('${paymentData.payment_id}', '${plan}')" class="btn btn-primary btn-block">
                    Verify Payment
                </button>
            </div>
        </div>
    `;
    
    modal.style.display = 'block';
}

// Copy to Clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Address copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Verify Crypto Payment
async function verifyCryptoPayment(paymentId, plan) {
    const txHash = document.getElementById('txHash').value;
    const email = document.getElementById('userEmail').value;
    
    if (!txHash || !email) {
        alert('Please enter transaction hash and email');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/verify-crypto-payment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                payment_id: paymentId,
                transaction_hash: txHash,
                email: email,
                plan: plan
            }),
        });
        
        if (!response.ok) {
            throw new Error('Payment verification failed');
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            alert(`Payment verified! Your license key: ${result.license_key}\n\nCheck your email for details.`);
            closeCryptoModal();
        } else {
            alert('Payment not yet confirmed. Please wait for blockchain confirmation.');
        }
    } catch (error) {
        console.error('Verification error:', error);
        alert('Error verifying payment. Please contact support.');
    }
}

// Close Crypto Modal
function closeCryptoModal() {
    document.getElementById('cryptoModal').style.display = 'none';
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('cryptoModal');
    if (event.target === modal) {
        closeCryptoModal();
    }
}

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Check for success redirect
window.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session_id');
    
    if (sessionId) {
        // Payment successful - show success message
        alert('Payment successful! Check your email for license key.');
        // Could also fetch session details and show license key
    }
});

// Form Validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Analytics (placeholder - integrate with your analytics service)
function trackEvent(category, action, label) {
    console.log('Event:', category, action, label);
    // Integrate with Google Analytics, Mixpanel, etc.
}

// Track button clicks
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('btn')) {
        trackEvent('Button', 'Click', e.target.textContent);
    }
});
