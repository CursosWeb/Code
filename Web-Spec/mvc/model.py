"""
Model component of MVC framework.
Manages state and data with shelve persistence.
"""

import shelve
import os
from typing import Any, Dict, Optional


class Model:
    """Generic model for managing application state with shelve persistence."""
    
    def __init__(self, storage_file: str = "app_state"):
        """
        Initialize the model with a storage file.
        
        Args:
            storage_file: Path to the file where state will be persisted (without extension)
        """
        self.storage_file = storage_file
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the state.
        
        Args:
            key: The key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            The value associated with the key, or default if not found
        """
        try:
            with shelve.open(self.storage_file) as db:
                return db.get(key, default)
        except Exception as e:
            print(f"Warning: Could not read from storage: {e}")
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the state.
        
        Args:
            key: The key to set
            value: The value to associate with the key
        """
        try:
            with shelve.open(self.storage_file) as db:
                db[key] = value
        except Exception as e:
            print(f"Warning: Could not write to storage: {e}")
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from the state.
        
        Args:
            key: The key to delete
            
        Returns:
            True if key was deleted, False if key didn't exist
        """
        try:
            with shelve.open(self.storage_file) as db:
                if key in db:
                    del db[key]
                    return True
                return False
        except Exception as e:
            print(f"Warning: Could not delete from storage: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the state.
        
        Args:
            key: The key to check
            
        Returns:
            True if key exists, False otherwise
        """
        try:
            with shelve.open(self.storage_file) as db:
                return key in db
        except Exception as e:
            print(f"Warning: Could not check storage: {e}")
            return False
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get a copy of the entire state.
        
        Returns:
            Dictionary containing all state data
        """
        try:
            with shelve.open(self.storage_file) as db:
                return dict(db)
        except Exception as e:
            print(f"Warning: Could not read all from storage: {e}")
            return {}
    
    def clear(self) -> None:
        """Clear all state data."""
        try:
            with shelve.open(self.storage_file) as db:
                db.clear()
        except Exception as e:
            print(f"Warning: Could not clear storage: {e}")
    
    def update(self, data: Dict[str, Any]) -> None:
        """
        Update multiple key-value pairs.
        
        Args:
            data: Dictionary of key-value pairs to update
        """
        try:
            with shelve.open(self.storage_file) as db:
                for key, value in data.items():
                    db[key] = value
        except Exception as e:
            print(f"Warning: Could not update storage: {e}")
