"""
OAuth configuration for Threat Canvas
"""

import os

# GitHub OAuth Configuration
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', '')
GITHUB_REDIRECT_URI = os.environ.get('GITHUB_REDIRECT_URI', 'http://localhost:8082/api/auth/github/callback')

# GitHub OAuth URLs
GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_USER_URL = 'https://api.github.com/user'

# OAuth settings
OAUTH_PROVIDERS = {
    'github': {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'authorize_url': GITHUB_AUTHORIZE_URL,
        'token_url': GITHUB_TOKEN_URL,
        'user_url': GITHUB_USER_URL,
        'redirect_uri': GITHUB_REDIRECT_URI,
        'scope': 'read:user user:email',
    }
}