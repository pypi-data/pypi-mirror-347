"""
OAuth handler for Threat Canvas
"""

import aiohttp
import json
import logging
import uuid
from typing import Dict, Any, Optional, Tuple

from autothreats.config.oauth import OAUTH_PROVIDERS

# Set up logger
logger = logging.getLogger(__name__)

async def get_github_auth_url(state: str = None) -> str:
    """
    Generate GitHub authorization URL
    
    Args:
        state: Optional state parameter for CSRF protection
        
    Returns:
        GitHub authorization URL
    """
    if not state:
        state = str(uuid.uuid4())
        
    github_config = OAUTH_PROVIDERS.get('github', {})
    client_id = github_config.get('client_id')
    
    if not client_id:
        raise ValueError("GitHub client ID is not configured")
    
    auth_url = (
        f"{github_config['authorize_url']}?"
        f"client_id={client_id}&"
        f"redirect_uri={github_config['redirect_uri']}&"
        f"scope={github_config['scope']}&"
        f"state={state}"
    )
    
    return auth_url, state

async def exchange_code_for_token(code: str, state: str) -> Dict[str, Any]:
    """
    Exchange authorization code for access token
    
    Args:
        code: Authorization code from GitHub
        state: State parameter for verification
        
    Returns:
        Dictionary containing access token and other info
    """
    github_config = OAUTH_PROVIDERS.get('github', {})
    
    if not github_config:
        raise ValueError("GitHub OAuth is not configured")
    
    # Prepare request data
    data = {
        'client_id': github_config['client_id'],
        'client_secret': github_config['client_secret'],
        'code': code,
        'redirect_uri': github_config['redirect_uri'],
        'state': state
    }
    
    # Exchange code for token
    async with aiohttp.ClientSession() as session:
        async with session.post(
            github_config['token_url'],
            data=data,
            headers={'Accept': 'application/json'}
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                logger.error(f"GitHub token exchange failed: {error_text}")
                raise ValueError(f"Failed to exchange code for token: {response.status}")
            
            token_data = await response.json()
            
            if 'error' in token_data:
                logger.error(f"GitHub token exchange error: {token_data['error']}")
                raise ValueError(f"GitHub error: {token_data.get('error_description', token_data['error'])}")
            
            return token_data

async def get_github_user_info(access_token: str) -> Dict[str, Any]:
    """
    Get GitHub user information using access token
    
    Args:
        access_token: GitHub access token
        
    Returns:
        Dictionary containing user information
    """
    github_config = OAUTH_PROVIDERS.get('github', {})
    
    if not github_config:
        raise ValueError("GitHub OAuth is not configured")
    
    # Get user info
    async with aiohttp.ClientSession() as session:
        # Get basic user info
        async with session.get(
            github_config['user_url'],
            headers={
                'Authorization': f"token {access_token}",
                'Accept': 'application/json'
            }
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                logger.error(f"GitHub user info request failed: {error_text}")
                raise ValueError(f"Failed to get user info: {response.status}")
            
            user_data = await response.json()
        
        # Get user emails if not provided in basic info
        if not user_data.get('email'):
            async with session.get(
                'https://api.github.com/user/emails',
                headers={
                    'Authorization': f"token {access_token}",
                    'Accept': 'application/json'
                }
            ) as email_response:
                if email_response.status == 200:
                    emails = await email_response.json()
                    primary_email = next((e for e in emails if e.get('primary')), None)
                    if primary_email:
                        user_data['email'] = primary_email.get('email')
    
    return user_data

async def process_github_callback(code: str, state: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Process GitHub OAuth callback
    
    Args:
        code: Authorization code from GitHub
        state: State parameter for verification
        
    Returns:
        Tuple containing token data and user info
    """
    # Exchange code for token
    token_data = await exchange_code_for_token(code, state)
    
    # Get user info
    user_info = await get_github_user_info(token_data.get('access_token', ''))
    
    return token_data, user_info