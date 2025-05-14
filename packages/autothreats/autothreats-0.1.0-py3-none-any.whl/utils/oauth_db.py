"""
Database operations for OAuth authentication
"""

import logging
import time
import uuid
from typing import Dict, Any, Optional

# Set up logger
logger = logging.getLogger(__name__)

# In-memory storage for OAuth states (for CSRF protection)
# In a production environment, this should be stored in a persistent database
oauth_states = {}

# In-memory storage for OAuth users
# In a production environment, this should be stored in a persistent database
oauth_users = {}

# In-memory storage for OAuth tokens
# In a production environment, this should be stored in a persistent database
oauth_tokens = {}

def store_oauth_state(state: str, expiry: int = 600) -> None:
    """
    Store OAuth state for CSRF protection
    
    Args:
        state: State parameter
        expiry: Expiry time in seconds (default: 10 minutes)
    """
    oauth_states[state] = {
        'created_at': int(time.time()),
        'expires_at': int(time.time()) + expiry
    }

def validate_oauth_state(state: str) -> bool:
    """
    Validate OAuth state
    
    Args:
        state: State parameter
        
    Returns:
        True if state is valid, False otherwise
    """
    state_data = oauth_states.get(state)
    
    if not state_data:
        return False
    
    # Check if state has expired
    if state_data['expires_at'] < int(time.time()):
        # Remove expired state
        oauth_states.pop(state, None)
        return False
    
    # Remove used state to prevent replay attacks
    oauth_states.pop(state, None)
    
    return True

async def find_or_create_oauth_user(provider: str, provider_user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find or create a user from OAuth data
    
    Args:
        provider: OAuth provider (e.g., 'github')
        provider_user_id: User ID from the provider
        user_data: User data from the provider
        
    Returns:
        User object
    """
    # Create a unique ID for the OAuth user
    oauth_id = f"{provider}:{provider_user_id}"
    
    # Check if user already exists
    existing_user = next((u for u in oauth_users.values() if u.get('oauth_id') == oauth_id), None)
    
    if existing_user:
        # Update existing user data
        existing_user.update({
            'username': user_data.get('login') or user_data.get('username'),
            'email': user_data.get('email'),
            'avatar': user_data.get('avatar_url'),
            'name': user_data.get('name'),
            'updated_at': int(time.time())
        })
        return existing_user
    
    # Create new user
    new_user = {
        'id': len(oauth_users) + 1,
        'oauth_id': oauth_id,
        'provider': provider,
        'provider_user_id': provider_user_id,
        'username': user_data.get('login') or user_data.get('username'),
        'email': user_data.get('email'),
        'avatar': user_data.get('avatar_url'),
        'name': user_data.get('name'),
        'created_at': int(time.time()),
        'updated_at': int(time.time())
    }
    
    # Store user
    oauth_users[new_user['id']] = new_user
    
    return new_user

async def store_oauth_token(user_id: int, provider: str, token_data: Dict[str, Any]) -> str:
    """
    Store OAuth token
    
    Args:
        user_id: User ID
        provider: OAuth provider (e.g., 'github')
        token_data: Token data from the provider
        
    Returns:
        JWT token for the user
    """
    # Create a unique token ID
    token_id = str(uuid.uuid4())
    
    # Calculate expiry time
    expires_in = token_data.get('expires_in', 3600)  # Default to 1 hour
    expires_at = int(time.time()) + expires_in
    
    # Store token data
    oauth_tokens[token_id] = {
        'user_id': user_id,
        'provider': provider,
        'access_token': token_data.get('access_token'),
        'refresh_token': token_data.get('refresh_token'),
        'token_type': token_data.get('token_type', 'bearer'),
        'scope': token_data.get('scope', ''),
        'created_at': int(time.time()),
        'expires_at': expires_at
    }
    
    # In a real application, this would create a JWT token
    # For now, we'll just return the token ID
    return token_id

async def get_oauth_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Get OAuth user by ID
    
    Args:
        user_id: User ID
        
    Returns:
        User object if found, None otherwise
    """
    return oauth_users.get(user_id)

async def validate_oauth_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Validate OAuth token
    
    Args:
        token: JWT token
        
    Returns:
        User ID if token is valid, None otherwise
    """
    # In a real application, this would validate the JWT token
    # For now, we'll just check if the token exists
    token_data = oauth_tokens.get(token)
    
    if not token_data:
        return None
    
    # Check if token has expired
    if token_data['expires_at'] < int(time.time()):
        return None
    
    # Get user
    user = await get_oauth_user_by_id(token_data['user_id'])
    
    if not user:
        return None
    
    return {
        'user_id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'exp': token_data['expires_at']
    }