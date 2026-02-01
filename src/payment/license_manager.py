"""
License Manager
Generates and validates StealthAI licenses
"""

import os
import json
import hashlib
import secrets
import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class LicenseManager:
    """
    Manages license generation, validation, and storage for StealthAI.
    """
    
    def __init__(self, license_file: Optional[str] = None):
        """
        Initialize license manager.
        
        Args:
            license_file: Path to license database file
        """
        self.license_file = license_file or os.path.join(
            os.path.dirname(__file__), '..', '..', 'licenses.json'
        )
        self.licenses = self._load_licenses()
    
    def _load_licenses(self) -> Dict[str, Any]:
        """Load licenses from file"""
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading licenses: {str(e)}")
                return {}
        return {}
    
    def _save_licenses(self) -> None:
        """Save licenses to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.license_file), exist_ok=True)
            
            with open(self.license_file, 'w') as f:
                json.dump(self.licenses, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving licenses: {str(e)}")
    
    def generate_license_key(self) -> str:
        """
        Generate a unique license key.
        Format: XXXX-XXXX-XXXX-XXXX
        
        Returns:
            License key string
        """
        # Generate 16 random characters
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        parts = []
        
        for _ in range(4):
            part = ''.join(secrets.choice(chars) for _ in range(4))
            parts.append(part)
        
        return '-'.join(parts)
    
    def create_license(self, plan: str, customer_email: str,
                      payment_id: str, duration_days: int = 30) -> Dict[str, Any]:
        """
        Create a new license.
        
        Args:
            plan: Plan name ('trial', 'pro', 'enterprise')
            customer_email: Customer email address
            payment_id: Payment transaction ID
            duration_days: License duration in days
            
        Returns:
            License data
        """
        license_key = self.generate_license_key()
        
        now = datetime.utcnow()
        expires_at = now + timedelta(days=duration_days)
        
        license_data = {
            'key': license_key,
            'plan': plan,
            'email': customer_email,
            'payment_id': payment_id,
            'created_at': now.isoformat(),
            'expires_at': expires_at.isoformat(),
            'status': 'active',
            'activations': [],
            'max_activations': self._get_max_activations(plan)
        }
        
        self.licenses[license_key] = license_data
        self._save_licenses()
        
        logger.info(f"Created license {license_key} for {customer_email}")
        
        return license_data
    
    def validate_license(self, license_key: str, machine_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a license key.
        
        Args:
            license_key: License key to validate
            machine_id: Optional machine ID for activation check
            
        Returns:
            Validation result
        """
        if license_key not in self.licenses:
            return {
                'valid': False,
                'error': 'Invalid license key'
            }
        
        license_data = self.licenses[license_key]
        
        # Check status
        if license_data['status'] != 'active':
            return {
                'valid': False,
                'error': f"License is {license_data['status']}"
            }
        
        # Check expiration
        expires_at = datetime.fromisoformat(license_data['expires_at'])
        if datetime.utcnow() > expires_at:
            license_data['status'] = 'expired'
            self._save_licenses()
            return {
                'valid': False,
                'error': 'License has expired'
            }
        
        # Check machine activation if provided
        if machine_id:
            activations = license_data.get('activations', [])
            max_activations = license_data.get('max_activations', 1)
            
            if machine_id not in activations:
                if len(activations) >= max_activations:
                    return {
                        'valid': False,
                        'error': f'Maximum activations ({max_activations}) reached'
                    }
        
        return {
            'valid': True,
            'license': license_data,
            'days_remaining': (expires_at - datetime.utcnow()).days
        }
    
    def activate_license(self, license_key: str, machine_id: str) -> Dict[str, Any]:
        """
        Activate a license on a machine.
        
        Args:
            license_key: License key
            machine_id: Unique machine identifier
            
        Returns:
            Activation result
        """
        # Validate first
        validation = self.validate_license(license_key, machine_id)
        if not validation['valid']:
            return validation
        
        license_data = self.licenses[license_key]
        activations = license_data.get('activations', [])
        
        if machine_id not in activations:
            activations.append(machine_id)
            license_data['activations'] = activations
            license_data['last_activated'] = datetime.utcnow().isoformat()
            self._save_licenses()
            
            logger.info(f"Activated license {license_key} on machine {machine_id}")
        
        return {
            'success': True,
            'license_key': license_key,
            'plan': license_data['plan'],
            'expires_at': license_data['expires_at'],
            'activations': len(activations),
            'max_activations': license_data['max_activations']
        }
    
    def deactivate_license(self, license_key: str, machine_id: str) -> Dict[str, Any]:
        """
        Deactivate a license from a machine.
        
        Args:
            license_key: License key
            machine_id: Machine identifier to remove
            
        Returns:
            Deactivation result
        """
        if license_key not in self.licenses:
            return {
                'success': False,
                'error': 'Invalid license key'
            }
        
        license_data = self.licenses[license_key]
        activations = license_data.get('activations', [])
        
        if machine_id in activations:
            activations.remove(machine_id)
            license_data['activations'] = activations
            self._save_licenses()
            
            logger.info(f"Deactivated license {license_key} from machine {machine_id}")
            
            return {
                'success': True,
                'license_key': license_key,
                'activations': len(activations)
            }
        
        return {
            'success': False,
            'error': 'Machine not activated'
        }
    
    def revoke_license(self, license_key: str) -> Dict[str, Any]:
        """
        Revoke a license (sets status to 'revoked').
        
        Args:
            license_key: License key to revoke
            
        Returns:
            Revocation result
        """
        if license_key not in self.licenses:
            return {
                'success': False,
                'error': 'Invalid license key'
            }
        
        self.licenses[license_key]['status'] = 'revoked'
        self._save_licenses()
        
        logger.info(f"Revoked license {license_key}")
        
        return {
            'success': True,
            'license_key': license_key,
            'status': 'revoked'
        }
    
    def get_license_info(self, license_key: str) -> Optional[Dict[str, Any]]:
        """
        Get license information.
        
        Args:
            license_key: License key
            
        Returns:
            License data or None
        """
        return self.licenses.get(license_key)
    
    def list_licenses(self, status: Optional[str] = None) -> list:
        """
        List all licenses, optionally filtered by status.
        
        Args:
            status: Filter by status ('active', 'expired', 'revoked')
            
        Returns:
            List of licenses
        """
        licenses = list(self.licenses.values())
        
        if status:
            licenses = [l for l in licenses if l['status'] == status]
        
        return licenses
    
    def _get_max_activations(self, plan: str) -> int:
        """Get maximum activations allowed for plan"""
        max_activations = {
            'trial': 1,
            'pro': 3,
            'enterprise': 10
        }
        return max_activations.get(plan, 1)
    
    @staticmethod
    def generate_machine_id() -> str:
        """
        Generate a unique machine identifier.
        
        Returns:
            Machine ID string
        """
        # Use hostname and MAC address for uniqueness
        import socket
        import uuid
        
        hostname = socket.gethostname()
        mac = uuid.getnode()
        
        # Create hash
        data = f"{hostname}:{mac}"
        hash_obj = hashlib.sha256(data.encode())
        
        return hash_obj.hexdigest()[:16].upper()
