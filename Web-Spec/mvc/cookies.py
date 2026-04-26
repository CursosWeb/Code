"""
Cookie management module for MVC framework.
Handles HTTP cookie creation, parsing, and manipulation.
"""

import urllib.parse
from typing import Dict, Optional, Union
from datetime import datetime, timedelta
import time


class Cookie:
    """Represents an HTTP cookie with name, value, and attributes."""
    
    def __init__(self, name: str, value: str, **attributes):
        """
        Initialize a cookie.
        
        Args:
            name: Cookie name
            value: Cookie value
            **attributes: Additional cookie attributes (expires, max_age, domain, path, secure, httponly, samesite)
        """
        self.name = name
        self.value = value
        self.attributes = attributes
    
    def to_set_cookie_header(self) -> str:
        """
        Convert cookie to Set-Cookie header value.
        
        Returns:
            Set-Cookie header string
        """
        cookie_parts = [f"{self.name}={self.value}"]
        
        # Handle expires
        if 'expires' in self.attributes:
            expires = self.attributes['expires']
            if isinstance(expires, (datetime, timedelta)):
                if isinstance(expires, timedelta):
                    expires = datetime.now() + expires
                cookie_parts.append(f"Expires={expires.strftime('%a, %d %b %Y %H:%M:%S GMT')}")
            elif isinstance(expires, str):
                cookie_parts.append(f"Expires={expires}")
        
        # Handle max-age
        if 'max_age' in self.attributes:
            cookie_parts.append(f"Max-Age={self.attributes['max_age']}")
        
        # Handle domain
        if 'domain' in self.attributes:
            cookie_parts.append(f"Domain={self.attributes['domain']}")
        
        # Handle path
        if 'path' in self.attributes:
            cookie_parts.append(f"Path={self.attributes['path']}")
        
        # Handle secure
        if self.attributes.get('secure', False):
            cookie_parts.append("Secure")
        
        # Handle httponly
        if self.attributes.get('httponly', False):
            cookie_parts.append("HttpOnly")
        
        # Handle samesite
        if 'samesite' in self.attributes:
            samesite = self.attributes['samesite'].lower()
            if samesite in ['strict', 'lax', 'none']:
                cookie_parts.append(f"SameSite={samesite.title()}")
        
        return "; ".join(cookie_parts)


class CookieManager:
    """Manager for HTTP cookie operations."""
    
    @staticmethod
    def create_cookie(name: str, value: str, **attributes) -> Cookie:
        """
        Create a new cookie.
        
        Args:
            name: Cookie name
            value: Cookie value
            **attributes: Additional cookie attributes
                - expires: datetime, timedelta, or string
                - max_age: int (seconds)
                - domain: str
                - path: str
                - secure: bool
                - httponly: bool
                - samesite: str ('strict', 'lax', 'none')
        
        Returns:
            Cookie object
        """
        return Cookie(name, value, **attributes)
    
    @staticmethod
    def parse_cookies(cookie_header: str) -> Dict[str, str]:
        """
        Parse cookies from HTTP Cookie header.
        
        Args:
            cookie_header: Value of Cookie header from HTTP request
            
        Returns:
            Dictionary mapping cookie names to values
        """
        cookies = {}
        
        if not cookie_header:
            return cookies
        
        # Split by semicolon and process each cookie
        for cookie_part in cookie_header.split(';'):
            cookie_part = cookie_part.strip()
            if not cookie_part:
                continue
            
            # Split by first equals sign
            if '=' in cookie_part:
                name, value = cookie_part.split('=', 1)
                name = name.strip()
                value = value.strip()
                
                # URL decode the name and value
                try:
                    name = urllib.parse.unquote(name)
                    value = urllib.parse.unquote(value)
                except Exception:
                    # If decoding fails, use original values
                    pass
                
                cookies[name] = value
        
        return cookies
    
    @staticmethod
    def extract_cookies_from_request(headers: Dict[str, str]) -> Dict[str, str]:
        """
        Extract all cookies from HTTP request headers.
        
        Args:
            headers: HTTP request headers dictionary
            
        Returns:
            Dictionary mapping cookie names to values
        """
        # Look for Cookie header (case-insensitive)
        cookie_header = None
        for header_name, header_value in headers.items():
            if header_name.lower() == 'cookie':
                cookie_header = header_value
                break
        
        return CookieManager.parse_cookies(cookie_header) if cookie_header else {}
    
    @staticmethod
    def set_cookie_response(cookie: Cookie) -> Dict[str, str]:
        """
        Generate headers to set a cookie in HTTP response.
        
        Args:
            cookie: Cookie object to set
            
        Returns:
            Dictionary with Set-Cookie header
        """
        return {'Set-Cookie': cookie.to_set_cookie_header()}
    
    @staticmethod
    def delete_cookie(name: str, **attributes) -> Dict[str, str]:
        """
        Generate headers to delete a cookie.
        
        Args:
            name: Cookie name to delete
            **attributes: Additional attributes for deletion (domain, path)
            
        Returns:
            Dictionary with Set-Cookie header for deletion
        """
        # Create a cookie with empty value and expiration in the past
        deletion_cookie = Cookie(
            name=name,
            value='',
            expires=datetime(1970, 1, 1),  # Past date to ensure deletion
            max_age=0,  # Also set max-age to 0
            **attributes
        )
        
        return {'Set-Cookie': deletion_cookie.to_set_cookie_header()}
    
    @staticmethod
    def create_session_cookie(name: str, value: str, **attributes) -> Cookie:
        """
        Create a session cookie (expires when browser closes).
        
        Args:
            name: Cookie name
            value: Cookie value
            **attributes: Additional attributes (except expires and max_age)
            
        Returns:
            Cookie object for session
        """
        # Session cookies don't have expires or max-age
        if 'expires' in attributes:
            del attributes['expires']
        if 'max_age' in attributes:
            del attributes['max_age']
        
        return Cookie(name, value, **attributes)
    
    @staticmethod
    def create_persistent_cookie(name: str, value: str, days: int = 30, **attributes) -> Cookie:
        """
        Create a persistent cookie with expiration.
        
        Args:
            name: Cookie name
            value: Cookie value
            days: Number of days until expiration
            **attributes: Additional attributes
            
        Returns:
            Cookie object with expiration
        """
        expires = datetime.now() + timedelta(days=days)
        return Cookie(name, value, expires=expires, **attributes)


# Convenience functions for backward compatibility and ease of use

def create_cookie(name: str, value: str, **attributes) -> Cookie:
    """Create a new cookie. Convenience function."""
    return CookieManager.create_cookie(name, value, **attributes)


def extract_cookies(headers: Dict[str, str]) -> Dict[str, str]:
    """Extract cookies from request headers. Convenience function."""
    return CookieManager.extract_cookies_from_request(headers)


def set_cookie(cookie: Cookie) -> Dict[str, str]:
    """Generate headers to set a cookie. Convenience function."""
    return CookieManager.set_cookie_response(cookie)


def delete_cookie(name: str, **attributes) -> Dict[str, str]:
    """Generate headers to delete a cookie. Convenience function."""
    return CookieManager.delete_cookie(name, **attributes)
