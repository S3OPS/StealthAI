"""
Cryptocurrency Payment Handler
Supports Bitcoin and Ethereum payments
"""

import os
import logging
import hashlib
import time
from typing import Dict, Any, Optional
from decimal import Decimal

logger = logging.getLogger(__name__)


class CryptoHandler:
    """
    Handles cryptocurrency payments for StealthAI.
    Supports Bitcoin (BTC) and Ethereum (ETH).
    
    NOTE: Conversion rates are example values. In production, implement
    periodic updates from a crypto price API (e.g., CoinGecko, CoinMarketCap).
    See update_conversion_rates() method below for integration point.
    """
    
    def __init__(self, btc_address: Optional[str] = None, eth_address: Optional[str] = None):
        """
        Initialize crypto payment handler.
        
        Args:
            btc_address: Bitcoin wallet address
            eth_address: Ethereum wallet address
        """
        self.btc_address = btc_address or os.getenv('BTC_WALLET_ADDRESS')
        self.eth_address = eth_address or os.getenv('ETH_WALLET_ADDRESS')
        
        # USD to crypto conversion rates (EXAMPLE VALUES - update from API in production)
        # TODO: Implement periodic updates from CoinGecko API or similar
        self.conversion_rates = {
            'BTC': Decimal('45000.00'),  # Example rate - REPLACE WITH LIVE DATA
            'ETH': Decimal('2500.00')     # Example rate - REPLACE WITH LIVE DATA
        }
    
    def get_payment_address(self, currency: str) -> Dict[str, Any]:
        """
        Get payment address for cryptocurrency.
        
        Args:
            currency: 'BTC' or 'ETH'
            
        Returns:
            Payment address and QR code data
        """
        if currency == 'BTC':
            if not self.btc_address:
                raise ValueError("Bitcoin address not configured")
            address = self.btc_address
        elif currency == 'ETH':
            if not self.eth_address:
                raise ValueError("Ethereum address not configured")
            address = self.eth_address
        else:
            raise ValueError(f"Unsupported currency: {currency}")
        
        return {
            'currency': currency,
            'address': address,
            'qr_data': f"{currency.lower()}:{address}"
        }
    
    def calculate_crypto_amount(self, usd_amount: float, currency: str) -> Decimal:
        """
        Calculate cryptocurrency amount based on USD price.
        
        Args:
            usd_amount: Amount in USD
            currency: 'BTC' or 'ETH'
            
        Returns:
            Amount in cryptocurrency
        """
        if currency not in self.conversion_rates:
            raise ValueError(f"Unsupported currency: {currency}")
        
        rate = self.conversion_rates[currency]
        crypto_amount = Decimal(str(usd_amount)) / rate
        
        return crypto_amount.quantize(Decimal('0.00000001'))  # 8 decimal places
    
    def create_payment_request(self, plan: str, currency: str) -> Dict[str, Any]:
        """
        Create a cryptocurrency payment request.
        
        Args:
            plan: Plan name ('pro' or 'enterprise')
            currency: 'BTC' or 'ETH'
            
        Returns:
            Payment request data
        """
        # Plan pricing
        prices = {
            'pro': 97.00,
            'enterprise': 297.00
        }
        
        if plan not in prices:
            raise ValueError(f"Invalid plan: {plan}")
        
        usd_amount = prices[plan]
        crypto_amount = self.calculate_crypto_amount(usd_amount, currency)
        payment_address = self.get_payment_address(currency)
        
        # Generate unique payment ID
        payment_id = self._generate_payment_id(plan, currency)
        
        logger.info(f"Created crypto payment request: {payment_id}")
        
        return {
            'payment_id': payment_id,
            'plan': plan,
            'currency': currency,
            'usd_amount': usd_amount,
            'crypto_amount': float(crypto_amount),
            'address': payment_address['address'],
            'qr_data': payment_address['qr_data'],
            'expires_at': int(time.time()) + 3600  # 1 hour expiration
        }
    
    def verify_payment(self, payment_id: str, transaction_hash: str) -> Dict[str, Any]:
        """
        Verify cryptocurrency payment.
        Note: In production, this would check blockchain for confirmation.
        
        Args:
            payment_id: Payment request ID
            transaction_hash: Blockchain transaction hash
            
        Returns:
            Verification result
        """
        # Simplified verification - in production would check blockchain
        if not transaction_hash or len(transaction_hash) < 10:
            return {
                'verified': False,
                'error': 'Invalid transaction hash'
            }
        
        logger.info(f"Verified crypto payment: {payment_id} - {transaction_hash}")
        
        return {
            'verified': True,
            'payment_id': payment_id,
            'transaction_hash': transaction_hash,
            'confirmations': 0,  # Would be checked on blockchain
            'status': 'pending'  # Would update as confirmations increase
        }
    
    def check_confirmation_status(self, transaction_hash: str, currency: str) -> Dict[str, Any]:
        """
        Check confirmation status of a transaction.
        Note: In production, this would query blockchain API.
        
        Args:
            transaction_hash: Transaction hash
            currency: 'BTC' or 'ETH'
            
        Returns:
            Confirmation status
        """
        # Simplified - in production would use blockchain API
        logger.info(f"Checking {currency} transaction: {transaction_hash}")
        
        return {
            'transaction_hash': transaction_hash,
            'currency': currency,
            'confirmations': 0,
            'required_confirmations': 3 if currency == 'BTC' else 12,
            'status': 'pending',
            'confirmed': False
        }
    
    def _generate_payment_id(self, plan: str, currency: str) -> str:
        """Generate unique payment ID"""
        timestamp = str(int(time.time()))
        data = f"{plan}:{currency}:{timestamp}"
        hash_obj = hashlib.sha256(data.encode())
        return f"CRYPTO-{hash_obj.hexdigest()[:16].upper()}"
    
    def get_conversion_rate(self, currency: str) -> Decimal:
        """
        Get current USD to crypto conversion rate.
        Note: In production, this would fetch from a price API.
        
        Args:
            currency: 'BTC' or 'ETH'
            
        Returns:
            Conversion rate
        """
        if currency not in self.conversion_rates:
            raise ValueError(f"Unsupported currency: {currency}")
        
        return self.conversion_rates[currency]
    
    def update_conversion_rates(self, rates: Dict[str, float]) -> None:
        """
        Update conversion rates.
        In production, this would be called periodically from price API.
        
        Args:
            rates: Dictionary of currency rates
        """
        for currency, rate in rates.items():
            if currency in self.conversion_rates:
                self.conversion_rates[currency] = Decimal(str(rate))
                logger.info(f"Updated {currency} rate to ${rate}")
