"""
Webhook Handler
Processes payment webhooks and automates license generation
"""

import logging
from typing import Dict, Any, Callable, Optional
from .license_manager import LicenseManager

logger = logging.getLogger(__name__)


class WebhookHandler:
    """
    Handles payment webhooks for automated license provisioning.
    """
    
    def __init__(self, license_manager: Optional[LicenseManager] = None):
        """
        Initialize webhook handler.
        
        Args:
            license_manager: License manager instance
        """
        self.license_manager = license_manager or LicenseManager()
        self.handlers = {}
    
    def register_handler(self, event_type: str, handler: Callable) -> None:
        """
        Register a custom handler for an event type.
        
        Args:
            event_type: Webhook event type
            handler: Handler function
        """
        self.handlers[event_type] = handler
        logger.info(f"Registered handler for {event_type}")
    
    def handle_stripe_webhook(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle Stripe webhook event.
        
        Args:
            event: Stripe webhook event data
            
        Returns:
            Processing result
        """
        event_type = event.get('type')
        
        logger.info(f"Processing Stripe webhook: {event_type}")
        
        # Check for custom handler
        if event_type in self.handlers:
            return self.handlers[event_type](event)
        
        # Default handlers
        if event_type == 'checkout.session.completed':
            return self._handle_checkout_completed(event)
        elif event_type == 'customer.subscription.created':
            return self._handle_subscription_created(event)
        elif event_type == 'customer.subscription.deleted':
            return self._handle_subscription_deleted(event)
        elif event_type == 'invoice.payment_succeeded':
            return self._handle_payment_succeeded(event)
        elif event_type == 'invoice.payment_failed':
            return self._handle_payment_failed(event)
        else:
            logger.warning(f"Unhandled webhook event: {event_type}")
            return {'status': 'ignored', 'event_type': event_type}
    
    def _handle_checkout_completed(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle successful checkout session"""
        session = event['data']['object']
        
        customer_email = session.get('customer_email')
        payment_intent = session.get('payment_intent')
        metadata = session.get('metadata', {})
        plan = metadata.get('plan', 'pro')
        
        # Generate license
        try:
            license_data = self.license_manager.create_license(
                plan=plan,
                customer_email=customer_email,
                payment_id=payment_intent or session['id'],
                duration_days=30
            )
            
            logger.info(f"Generated license for checkout: {license_data['key']}")
            
            # Here you would send email with license key
            # self._send_license_email(customer_email, license_data)
            
            return {
                'status': 'success',
                'license_key': license_data['key'],
                'email': customer_email
            }
            
        except Exception as e:
            logger.error(f"Error generating license: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def _handle_subscription_created(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle new subscription"""
        subscription = event['data']['object']
        
        customer_id = subscription.get('customer')
        subscription_id = subscription.get('id')
        
        logger.info(f"New subscription created: {subscription_id}")
        
        # Subscription licenses are created in checkout_completed
        return {'status': 'acknowledged', 'subscription_id': subscription_id}
    
    def _handle_subscription_deleted(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle subscription cancellation"""
        subscription = event['data']['object']
        
        subscription_id = subscription.get('id')
        customer_id = subscription.get('customer')
        
        logger.info(f"Subscription cancelled: {subscription_id}")
        
        # Here you would deactivate associated licenses
        # For now, licenses will expire naturally
        
        return {'status': 'acknowledged', 'subscription_id': subscription_id}
    
    def _handle_payment_succeeded(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle successful recurring payment"""
        invoice = event['data']['object']
        
        subscription_id = invoice.get('subscription')
        customer_email = invoice.get('customer_email')
        
        logger.info(f"Payment succeeded for subscription: {subscription_id}")
        
        # Extend license for another month
        # You would look up license by subscription_id and extend it
        
        return {'status': 'acknowledged', 'subscription_id': subscription_id}
    
    def _handle_payment_failed(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle failed recurring payment"""
        invoice = event['data']['object']
        
        subscription_id = invoice.get('subscription')
        customer_email = invoice.get('customer_email')
        attempt_count = invoice.get('attempt_count', 0)
        
        logger.warning(f"Payment failed for subscription: {subscription_id} (attempt {attempt_count})")
        
        # Send notification about failed payment
        # After certain attempts, Stripe will cancel the subscription
        
        return {'status': 'acknowledged', 'subscription_id': subscription_id}
    
    def handle_crypto_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle cryptocurrency payment confirmation.
        
        Args:
            payment_data: Crypto payment data
            
        Returns:
            Processing result
        """
        transaction_hash = payment_data.get('transaction_hash')
        plan = payment_data.get('plan', 'pro')
        customer_email = payment_data.get('email')
        
        logger.info(f"Processing crypto payment: {transaction_hash}")
        
        try:
            # Generate license
            license_data = self.license_manager.create_license(
                plan=plan,
                customer_email=customer_email,
                payment_id=transaction_hash,
                duration_days=30
            )
            
            logger.info(f"Generated license for crypto payment: {license_data['key']}")
            
            return {
                'status': 'success',
                'license_key': license_data['key'],
                'email': customer_email
            }
            
        except Exception as e:
            logger.error(f"Error generating license for crypto payment: {str(e)}")
            return {'status': 'error', 'error': str(e)}
