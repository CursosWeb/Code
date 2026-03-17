"""
Session management module for MVC framework.
Handles HTTP sessions using cookies for session identification.
"""

import uuid
import time
from typing import Dict, Any, Optional
from model import Model
from cookies import CookieManager, create_cookie


class SessionManager:
    """Manages HTTP sessions using cookies for identification."""
    
    def __init__(self, storage_file: str = "sessions"):
        """
        Initialize session manager with storage.
        
        Args:
            storage_file: Storage file for session data
        """
        self.model = Model(storage_file)
        self.session_timeout = 3600  # 1 hour default timeout
    
    def set_session_timeout(self, seconds: int):
        """
        Set session timeout in seconds.
        
        Args:
            seconds: Session timeout in seconds
        """
        self.session_timeout = seconds
    
    def get_session(self, request_headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Get session data from request headers.
        
        Args:
            request_headers: HTTP request headers
            
        Returns:
            Session data dictionary or None if no valid session
        """
        # Extract cookies from request
        cookies = CookieManager.extract_cookies_from_request(request_headers)
        
        # Look for session cookie
        session_id = cookies.get('session_id')
        if not session_id:
            return None
        
        # Get session data from storage
        session_data = self.model.get(f"session_{session_id}")
        if not session_data:
            return None
        
        # Check if session has expired
        if self._is_session_expired(session_data):
            # Clean up expired session
            self.model.delete(f"session_{session_id}")
            return None
        
        # Update last access time
        session_data['last_access'] = time.time()
        self.model.set(f"session_{session_id}", session_data)
        
        return session_data.get('data', {})
    
    def start_session(self, initial_data: Optional[Dict[str, Any]] = None) -> tuple:
        """
        Start a new session and create session cookie.
        
        Args:
            initial_data: Initial data to store in session
            
        Returns:
            Tuple of (session_data, cookie_headers)
        """
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Create session data
        session_data = {
            'session_id': session_id,
            'created_at': time.time(),
            'last_access': time.time(),
            'data': initial_data or {}
        }
        
        # Store session
        self.model.set(f"session_{session_id}", session_data)
        
        # Create session cookie
        session_cookie = create_cookie(
            'session_id',
            session_id,
            httponly=True,
            secure=True,  # Recommended for security
            samesite='strict',
            max_age=self.session_timeout
        )
        
        # Get cookie headers
        cookie_headers = CookieManager.set_cookie_response(session_cookie)
        
        return session_data['data'], cookie_headers
    
    def update_session(self, request_headers: Dict[str, str], new_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update existing session with new data.
        
        Args:
            request_headers: HTTP request headers
            new_data: New data to merge into session
            
        Returns:
            Updated session data or None if no valid session
        """
        session_data = self.get_session(request_headers)
        if not session_data:
            return None
        
        # Get session ID from cookies
        cookies = CookieManager.extract_cookies_from_request(request_headers)
        session_id = cookies.get('session_id')
        
        if not session_id:
            return None
        
        # Get full session record
        full_session = self.model.get(f"session_{session_id}")
        if not full_session:
            return None
        
        # Update session data
        full_session['data'].update(new_data)
        full_session['last_access'] = time.time()
        
        # Store updated session
        self.model.set(f"session_{session_id}", full_session)
        
        return full_session['data']
    
    def destroy_session(self, request_headers: Dict[str, str]) -> Dict[str, str]:
        """
        Destroy session and create deletion cookie.
        
        Args:
            request_headers: HTTP request headers
            
        Returns:
            Cookie headers for session deletion
        """
        # Extract cookies to get session ID
        cookies = CookieManager.extract_cookies_from_request(request_headers)
        session_id = cookies.get('session_id')
        
        if session_id:
            # Delete session from storage
            self.model.delete(f"session_{session_id}")
        
        # Create deletion cookie
        return CookieManager.delete_cookie('session_id', path='/')
    
    def cleanup_expired_sessions(self):
        """Clean up all expired sessions."""
        all_sessions = self.model.get_all()
        current_time = time.time()
        
        for key, session_data in all_sessions.items():
            if key.startswith('session_') and self._is_session_expired(session_data):
                self.model.delete(key)
    
    def _is_session_expired(self, session_data: Dict[str, Any]) -> bool:
        """
        Check if a session has expired.
        
        Args:
            session_data: Session data dictionary
            
        Returns:
            True if session has expired, False otherwise
        """
        last_access = session_data.get('last_access', 0)
        return (current_time := time.time()) - last_access > self.session_timeout
    
    def get_all_active_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all active (non-expired) sessions.
        
        Returns:
            Dictionary of session_id -> session_data
        """
        all_sessions = self.model.get_all()
        active_sessions = {}
        
        for key, session_data in all_sessions.items():
            if key.startswith('session_') and not self._is_session_expired(session_data):
                session_id = key.replace('session_', '')
                active_sessions[session_id] = session_data
        
        return active_sessions


# Global session manager instance
_session_manager = None


def get_session_manager(storage_file: str = "sessions") -> SessionManager:
    """
    Get or create global session manager instance.
    
    Args:
        storage_file: Storage file for session data
        
    Returns:
        SessionManager instance
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager(storage_file)
    return _session_manager


# Convenience functions for backward compatibility and ease of use

def get_session(request_headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    Get session data from request. Convenience function.
    
    Args:
        request_headers: HTTP request headers
        
    Returns:
        Session data dictionary or None if no valid session
    """
    manager = get_session_manager()
    return manager.get_session(request_headers)


def start_session(initial_data: Optional[Dict[str, Any]] = None) -> tuple:
    """
    Start a new session. Convenience function.
    
    Args:
        initial_data: Initial data to store in session
        
    Returns:
        Tuple of (session_data, cookie_headers)
    """
    manager = get_session_manager()
    return manager.start_session(initial_data)


def update_session(request_headers: Dict[str, str], new_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update existing session. Convenience function.
    
    Args:
        request_headers: HTTP request headers
        new_data: New data to merge into session
        
    Returns:
        Updated session data or None if no valid session
    """
    manager = get_session_manager()
    return manager.update_session(request_headers, new_data)


def destroy_session(request_headers: Dict[str, str]) -> Dict[str, str]:
    """
    Destroy session. Convenience function.
    
    Args:
        request_headers: HTTP request headers
        
    Returns:
        Cookie headers for session deletion
    """
    manager = get_session_manager()
    return manager.destroy_session(request_headers)


def cleanup_sessions():
    """Clean up expired sessions. Convenience function."""
    manager = get_session_manager()
    manager.cleanup_expired_sessions()


def set_session_timeout(seconds: int):
    """
    Set session timeout. Convenience function.
    
    Args:
        seconds: Session timeout in seconds
    """
    manager = get_session_manager()
    manager.set_session_timeout(seconds)
