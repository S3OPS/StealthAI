"""
Stripe Payment Handler
Manages Stripe checkout sessions and subscriptions
"""

import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Stripe will be imported when needed to avoid requiring it for basic StealthAI operations
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    logger.warning("Stripe module not available. Install with: pip install stripe")


class StripeHandler:
    """
    Handles Stripe payment processing for StealthAI.
    Uses FREE Stripe tier - no monthly fees, just 2.9% + 30¢ per transaction.
    """
    
    def __init__(self, api_key: Optional[str] = None, webhook_secret: Optional[str] = None):
        """
        Initialize Stripe handler.
        
        Args:
            api_key: Stripe secret API key (or from environment)
            webhook_secret: Stripe webhook signing secret
        """
        if not STRIPE_AVAILABLE:
            raise ImportError("Stripe is not installed. Run: pip install stripe")
        
        self.api_key = api_key or os.getenv('STRIPE_SECRET_KEY')
        self.webhook_secret = webhook_secret or os.getenv('STRIPE_WEBHOOK_SECRET')
        
        if self.api_key:
            stripe.api_key = self.api_key
        else:
            logger.warning("No Stripe API key configured")
    
    def create_checkout_session(self, plan: str, success_url: str, 
                               cancel_url: str, customer_email: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a Stripe checkout session for a pricing plan.
        
        Args:
            plan: Plan name ('pro' or 'enterprise')
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect if payment is cancelled
            customer_email: Pre-fill customer email
            
        Returns:
            Session data including checkout URL
        """
        if not self.api_key:
            raise ValueError("Stripe API key not configured")
        
        # Pricing configuration
        prices = {
            'pro': {
                'amount': 9700,  # $97.00
                'name': 'StealthAI Pro',
                'description': 'Unlimited AI content generation with signal compression'
            },
            'enterprise': {
                'amount': 29700,  # $297.00
                'name': 'StealthAI Enterprise',
                'description': 'White-label solution with API access'
            }
        }
        
        if plan not in prices:
            raise ValueError(f"Invalid plan: {plan}. Must be 'pro' or 'enterprise'")
        
        price_config = prices[plan]
        
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': price_config['name'],
                            'description': price_config['description'],
                        },
                        'unit_amount': price_config['amount'],
                        'recurring': {
                            'interval': 'month'
                        }
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=customer_email,
                metadata={
                    'plan': plan,
                    'product': 'stealthai'
                }
            )
            
            logger.info(f"Created checkout session for {plan} plan: {session.id}")
            
            return {
                'session_id': session.id,
                'url': session.url,
                'plan': plan,
                'amount': price_config['amount']
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating checkout session: {str(e)}")
            raise
    
    def create_payment_intent(self, amount: int, currency: str = 'usd',
                             metadata: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Create a one-time payment intent.
        
        Args:
            amount: Amount in cents
            currency: Currency code (default: usd)
            metadata: Additional metadata
            
        Returns:
            Payment intent data
        """
        if not self.api_key:
            raise ValueError("Stripe API key not configured")
        
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata=metadata or {}
            )
            
            logger.info(f"Created payment intent: {intent.id}")
            
            return {
                'client_secret': intent.client_secret,
                'intent_id': intent.id,
                'amount': amount,
                'currency': currency
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating payment intent: {str(e)}")
            raise
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> Dict[str, Any]:
        """
        Verify Stripe webhook signature and parse event.
        
        Args:
            payload: Raw request body
            signature: Stripe-Signature header value
            
        Returns:
            Parsed webhook event
        """
        if not self.webhook_secret:
            raise ValueError("Webhook secret not configured")
        
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            
            logger.info(f"Verified webhook event: {event['type']}")
            return event
            
        except ValueError as e:
            logger.error(f"Invalid webhook payload: {str(e)}")
            raise
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid webhook signature: {str(e)}")
            raise
    
    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Retrieve subscription details.
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            Subscription data
        """
        if not self.api_key:
            raise ValueError("Stripe API key not configured")
        
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            return {
                'id': subscription.id,
                'status': subscription.status,
                'current_period_end': subscription.current_period_end,
                'customer': subscription.customer,
                'plan': subscription.items.data[0].price.id if subscription.items.data else None
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving subscription: {str(e)}")
            raise
    
    def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Cancel a subscription.
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            Cancelled subscription data
        """
        if not self.api_key:
            raise ValueError("Stripe API key not configured")
        
        try:
            subscription = stripe.Subscription.delete(subscription_id)
            
            logger.info(f"Cancelled subscription: {subscription_id}")
            
            return {
                'id': subscription.id,
                'status': subscription.status,
                'cancelled_at': subscription.canceled_at
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error cancelling subscription: {str(e)}")
            raise
    
    def list_customer_subscriptions(self, customer_id: str) -> list:
        """
        List all subscriptions for a customer.
        
        Args:
            customer_id: Stripe customer ID
            
        Returns:
            List of subscriptions
        """
        if not self.api_key:
            raise ValueError("Stripe API key not configured")
        
        try:
            subscriptions = stripe.Subscription.list(customer=customer_id)
            
            return [{
                'id': sub.id,
                'status': sub.status,
                'plan': sub.items.data[0].price.id if sub.items.data else None,
                'current_period_end': sub.current_period_end
            } for sub in subscriptions.data]
            
        except stripe.error.StripeError as e:
            logger.error(f"Error listing subscriptions: {str(e)}")
            raise
