import asyncio
import datetime
import json
import logging
import os
import time
import traceback
import uuid

import aiohttp_cors
from aiohttp import web

from autothreats import db  # Import db directly from autothreats
from autothreats.utils.oauth_db import (
    find_or_create_oauth_user,
    get_oauth_user_by_id,
    store_oauth_state,
    store_oauth_token,
    validate_oauth_state,
    validate_oauth_token,
)
from autothreats.utils.oauth_handler import get_github_auth_url, process_github_callback
from autothreats.utils.simple_extensions import load_and_run_extensions


# Function to get client IP from request
def get_client_ip(request):
    """Get client IP address from request"""
    peername = request.transport.get_extra_info("peername")
    if peername is not None:
        host, _ = peername
        return host
    return None


# Import the orchestrator and agent decorators
from autothreats.simplified_orchestrator import SimplifiedOrchestrator
from autothreats.utils.agent_decorators import register_agents


# Create orchestrator function
async def create_orchestrator(workspace, enable_agentic=True):
    """
    Create and initialize an orchestrator with the given workspace.

    Args:
        workspace: The shared workspace to use
        enable_agentic: Whether to enable agentic improvements

    Returns:
        Initialized orchestrator
    """
    # Create configuration
    config = {
        "system": {"enable_agentic_improvements": enable_agentic},
        "workspace_id": workspace.model.id,
    }

    # Create orchestrator
    orchestrator = SimplifiedOrchestrator(config)

    # Set the workspace
    orchestrator.workspace = workspace

    # Register agents with the workspace
    register_agents(workspace)

    # Initialize the orchestrator
    await orchestrator.initialize()

    return orchestrator


# Initialize orchestrator function (for backward compatibility)
async def initialize_orchestrator():
    """Initialize the orchestrator (legacy function)"""
    global orchestrator

    # Import the workspace
    from autothreats.simplified_base import SharedWorkspace

    # Create a workspace
    workspace = SharedWorkspace("api_workspace")
    await workspace.start()

    # Create and initialize the orchestrator
    orchestrator = await create_orchestrator(workspace)

    return orchestrator


# Create a router for API endpoints
routes = web.RouteTableDef()

# Set up logger
logger = logging.getLogger(__name__)

# Default system user ID
DEFAULT_SYSTEM_USER_ID = "system"

# Dictionary to store job statuses
job_statuses = {}

# Dictionary to store SSE clients
sse_clients = {}

# Dictionary to store job results
job_results = {}

# Initialize orchestrator (will be set later)
orchestrator = None


@routes.get("/")
async def index(request):
    """Root endpoint"""
    return web.Response(text="Simplified Threat Canvas API Server")


@routes.get("/api/health")
async def health_check(request):
    """Health check endpoint"""
    return web.json_response(
        {
            "status": "ok",
            "version": "1.0.0",
            "orchestrator_initialized": orchestrator is not None,
        }
    )


@routes.get("/api/analysis/progress")
async def get_analysis_progress(request):
    """Get analysis progress"""
    # Check authentication
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return web.json_response({"error": "Authentication required"}, status=401)

    # Extract token
    token = auth_header.replace("Bearer ", "")

    # Validate token (simple validation for now)
    if not token.startswith("jwt-token-") and token != "mock-jwt-token":
        try:
            # Try OAuth token validation
            token_data = await validate_oauth_token(token)
            if not token_data:
                return web.json_response(
                    {"error": "Invalid or expired token"}, status=401
                )
        except Exception:
            return web.json_response({"error": "Invalid or expired token"}, status=401)

    # Get job ID from query parameters
    job_id = request.query.get("jobId")

    if not job_id:
        return web.json_response({"error": "Job ID is required"}, status=400)

    # Check if job exists in job_statuses
    if job_id in job_statuses:
        return web.json_response(job_statuses[job_id])

    # Return error for non-existent jobs (except "latest")
    if job_id != "latest":
        return web.json_response(
            {"error": f"Job with ID {job_id} not found"}, status=404
        )

    # Return mock progress data for "latest"
    return web.json_response(
        {
            "job_id": job_id,
            "id": job_id,
            "status": "running",
            "progress_percentage": 50,
            "current_stage": "Analyzing code",
            "start_time": int(time.time()) - 60,  # Started 1 minute ago
        }
    )


@routes.get("/api/threat-model")
async def get_threat_model(request):
    """Get threat model"""
    # Check authentication
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return web.json_response({"error": "Authentication required"}, status=401)

    # Extract token
    token = auth_header.replace("Bearer ", "")

    # Validate token (simple validation for now)
    if not token.startswith("jwt-token-") and token != "mock-jwt-token":
        try:
            # Try OAuth token validation
            token_data = await validate_oauth_token(token)
            if not token_data:
                return web.json_response(
                    {"error": "Invalid or expired token"}, status=401
                )
        except Exception:
            return web.json_response({"error": "Invalid or expired token"}, status=401)

    # Get job ID from query parameters
    job_id = request.query.get("jobId")

    print(f"GET /api/threat-model - Job ID: {job_id}")

    if not job_id:
        print("Error: Job ID is required")
        return web.json_response({"error": "Job ID is required"}, status=400)

    # Check if the threat model file exists
    # Use absolute path to results directory
    output_dir = os.path.abspath("./results")
    print(f"Absolute path to results directory: {output_dir}")
    job_dir = os.path.join(output_dir, job_id)
    json_path = os.path.join(job_dir, f"threat_model_{job_id}.json")

    print(f"Looking for threat model at: {json_path}")
    print(f"Directory exists: {os.path.exists(job_dir)}")
    print(f"File exists: {os.path.exists(json_path)}")

    # List files in the job directory if it exists
    if os.path.exists(job_dir):
        print(f"Files in {job_dir}:")
        for file in os.listdir(job_dir):
            print(f"  - {file}")

    if os.path.exists(json_path):
        try:
            # Read the threat model from the file
            with open(json_path, "r") as f:
                threat_model = json.load(f)

            print(f"Successfully read threat model from file")
            return web.json_response(threat_model)
        except Exception as e:
            print(f"Error reading threat model file: {e}")
            return web.json_response(
                {"error": f"Error reading threat model: {str(e)}"}, status=500
            )
    else:
        # Check if the job exists in job_statuses
        print(f"Job exists in job_statuses: {job_id in job_statuses}")
        if job_id in job_statuses:
            # Print job status
            print(f"Job status: {job_statuses[job_id].get('status', 'unknown')}")
            print(f"Job data: {json.dumps(job_statuses[job_id], default=str)}")

            # Check if there's a threat_model_path in the job status
            threat_model_path = job_statuses[job_id].get("threat_model_path")
            if threat_model_path and os.path.exists(threat_model_path):
                print(f"Found threat model at alternate path: {threat_model_path}")
                try:
                    # Read the threat model from the alternate path
                    with open(threat_model_path, "r") as f:
                        threat_model = json.load(f)

                    print(f"Successfully read threat model from alternate path")
                    return web.json_response(threat_model)
                except Exception as e:
                    print(f"Error reading threat model from alternate path: {e}")

            # Job exists but threat model file doesn't exist yet
            print(f"Returning in-progress threat model")
            return web.json_response(
                {
                    "id": job_id,
                    "job_id": job_id,
                    "title": f"Threat Model for Job {job_id}",
                    "executive_summary": "Analysis in progress. Threat model not yet available.",
                    "vulnerabilities": [],
                    "threat_scenarios": [],
                    "metadata": {
                        "generated_at": time.time(),
                        "job_id": job_id,
                        "status": job_statuses[job_id].get("status", "unknown"),
                    },
                }
            )
        else:
            # Job doesn't exist
            print(f"Job not found in job_statuses")
            print(f"Available job IDs: {list(job_statuses.keys())}")
            return web.json_response(
                {"error": f"Analysis not found for job ID: {job_id}"}, status=404
            )


@routes.post("/api/analysis/run")
async def run_analysis(request):
    """Start a new analysis"""
    try:
        # Check authentication
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return web.json_response(
                {"error": "Authentication required", "success": False}, status=401
            )

        # Extract token
        token = auth_header.replace("Bearer ", "")

        # Validate token (simple validation for now)
        # In a real app, you would do more thorough validation
        if not token.startswith("jwt-token-") and token != "mock-jwt-token":
            try:
                # Try OAuth token validation
                token_data = await validate_oauth_token(token)
                if not token_data:
                    return web.json_response(
                        {"error": "Invalid or expired token", "success": False},
                        status=401,
                    )
            except Exception:
                return web.json_response(
                    {"error": "Invalid or expired token", "success": False}, status=401
                )

        # Parse the request data
        data = await request.json()

        # Generate a job ID
        job_id = str(uuid.uuid4())

        # Create a job status entry
        job_statuses[job_id] = {
            "job_id": job_id,
            "status": "running",
            "progress_percentage": 0,
            "current_stage": "Starting analysis",
            "start_time": int(time.time()),
            "output_dir": "./results",
        }

        # Start the analysis task in the background
        asyncio.create_task(run_analysis_task(job_id, data))

        # Return success response
        return web.json_response(
            {
                "success": True,
                "jobId": job_id,
                "message": "Analysis started successfully",
            }
        )
    except Exception as e:
        logger.error(f"Error starting analysis: {str(e)}")
        return web.json_response(
            {"success": False, "error": f"Error starting analysis: {str(e)}"},
            status=500,
        )


async def run_analysis_task(job_id: str, data: dict):
    """
    Run an analysis task in the background.

    Args:
        job_id: The ID of the job
        data: The job data
    """
    try:
        # Update job status
        job_statuses[job_id]["current_stage"] = "Initializing"
        job_statuses[job_id]["progress_percentage"] = 5

        # Create orchestrator config
        orchestrator_config = {
            "log_level": "INFO",
            "threat_detection": {
                "llm_provider": data.get("system", {}).get("llm_provider", "openai"),
                "openai_model": data.get("system", {}).get(
                    "openai_model", "gpt-4o-mini"
                ),
            },
            "enable_multi_stage": data.get("system", {}).get(
                "enable_multi_stage", False
            ),
            "enable_agentic": data.get("system", {}).get(
                "enable_agentic_improvements", True
            ),
            "system": {
                "debug_logging": data.get("system", {}).get("debug_logging", False),
                "lightweight": data.get("system", {}).get("lightweight", False),
                "max_scan_dirs": data.get("system", {}).get("max_scan_dirs", 1000),
            },
        }

        # Create job data
        job_data = {
            "job_id": job_id,
            "codebase_id": f"codebase_{job_id}",
            "codebase": {"files": {}},  # Will be populated from repository
            "context": {
                "lightweight": data.get("system", {}).get("lightweight", False),
                "enable_multi_stage": data.get("system", {}).get(
                    "enable_multi_stage", False
                ),
                "enable_redflag": data.get("security_tools", {}).get(
                    "enable_redflag", False
                ),
                "enable_codeshield": data.get("security_tools", {}).get(
                    "enable_codeshield", False
                ),
                "enable_agentic": data.get("system", {}).get(
                    "enable_agentic_improvements", True
                ),
            },
        }

        # Start monitoring progress
        await _monitor_progress(job_id, orchestrator_config, job_data)

    except Exception as e:
        # Update job status on error
        job_statuses[job_id]["status"] = "error"
        job_statuses[job_id]["error"] = str(e)
        job_statuses[job_id]["end_time"] = int(time.time())
        logger.error(f"Error running analysis task: {str(e)}")


@routes.post("/api/auth/login")
async def login(request):
    """Login endpoint"""
    try:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")

        # Validate input
        if not username or not password:
            return web.json_response(
                {"error": "Username and password are required"}, status=400
            )

        # Use database authentication
        from autothreats import db

        # Initialize the database if it hasn't been initialized yet
        try:
            db.init_db()
        except Exception as db_init_error:
            logger.error(f"Database initialization error: {str(db_init_error)}")
            logger.error(traceback.format_exc())
            # Fall back to mock authentication if database fails
            return web.json_response(
                {
                    "token": "mock-jwt-token",
                    "user_id": 1,
                    "username": username,
                    "expires_in": 3600,  # 1 hour
                    "auth_type": "password",
                }
            )

        # Authenticate the user
        try:
            user = db.authenticate_user(username, password)

            if not user:
                return web.json_response(
                    {"error": "Invalid username or password"}, status=401
                )
        except Exception as auth_error:
            logger.error(f"Authentication error: {str(auth_error)}")
            logger.error(traceback.format_exc())
            # Fall back to mock authentication if authentication fails
            return web.json_response(
                {
                    "token": "mock-jwt-token",
                    "user_id": 1,
                    "username": username,
                    "expires_in": 3600,  # 1 hour
                    "auth_type": "password",
                }
            )

        # Try to create an audit record for the login, but don't fail if it doesn't work
        try:
            client_ip = get_client_ip(request)
            db.create_audit_record(
                action=db.AUDIT_LOGIN,
                entity_type="user",
                entity_id=user["id"],
                user_id=user["id"],
                details={"username": username, "ip": client_ip},
                ip_address=client_ip,
            )
        except Exception as audit_error:
            logger.error(f"Audit record creation error: {str(audit_error)}")
            # Continue even if audit record creation fails

        # Return token and user info
        return web.json_response(
            {
                "token": f"jwt-token-{user['id']}",  # In a real app, you would generate a proper JWT
                "user_id": user["id"],
                "username": user["username"],
                "expires_in": 3600,  # 1 hour
                "auth_type": "password",
            }
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        logger.error(traceback.format_exc())
        # Fall back to mock authentication as a last resort
        return web.json_response(
            {
                "token": "mock-jwt-token",
                "user_id": 1,
                "username": username if "username" in locals() else "unknown",
                "expires_in": 3600,  # 1 hour
                "auth_type": "password",
            }
        )


@routes.get("/api/auth/github")
async def github_auth(request):
    """GitHub OAuth authorization endpoint"""
    try:
        # Generate state for CSRF protection
        state = str(uuid.uuid4())

        # Store state
        store_oauth_state(state)

        # Generate GitHub authorization URL
        auth_url, _ = await get_github_auth_url(state)

        # Return authorization URL
        return web.json_response({"auth_url": auth_url})
    except Exception as e:
        logger.error(f"GitHub auth error: {str(e)}")
        return web.json_response(
            {"error": f"An error occurred during GitHub authentication: {str(e)}"},
            status=500,
        )


@routes.get("/api/auth/github/callback")
async def github_callback(request):
    """GitHub OAuth callback endpoint"""
    try:
        # Get code and state from query parameters
        code = request.query.get("code")
        state = request.query.get("state")

        if not code or not state:
            return web.Response(
                text="<html><body><h1>Authentication Error</h1><p>Missing code or state parameter.</p></body></html>",
                content_type="text/html",
            )

        # Validate state
        if not validate_oauth_state(state):
            return web.Response(
                text="<html><body><h1>Authentication Error</h1><p>Invalid or expired state parameter.</p></body></html>",
                content_type="text/html",
            )

        # Process GitHub callback
        token_data, user_info = await process_github_callback(code, state)

        # Find or create user
        user = await find_or_create_oauth_user(
            provider="github",
            provider_user_id=str(user_info.get("id")),
            user_data=user_info,
        )

        # Store token
        jwt_token = await store_oauth_token(user["id"], "github", token_data)

        # Create HTML response with script to store token and redirect
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Successful</title>
            <script>
                // Store token in localStorage
                localStorage.setItem('threat_canvas_auth_token', '{jwt_token}');
                localStorage.setItem('threat_canvas_user', JSON.stringify({{
                    id: {user['id']},
                    username: '{user['username']}',
                    auth_type: 'github'
                }}));
                localStorage.setItem('threat_canvas_token_expiry', '{int(time.time()) + 3600 * 1000}');
                
                // Redirect to home page
                window.location.href = './';
            </script>
        </head>
        <body>
            <h1>Authentication Successful</h1>
            <p>You are being redirected...</p>
        </body>
        </html>
        """

        return web.Response(text=html, content_type="text/html")
    except Exception as e:
        logger.error(f"GitHub callback error: {str(e)}")
        return web.Response(
            text=f"<html><body><h1>Authentication Error</h1><p>{str(e)}</p></body></html>",
            content_type="text/html",
        )


@routes.get("/api/auth/user")
async def get_user(request):
    """Get user information"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return web.json_response(
                {"error": "Invalid authorization header"}, status=401
            )

        token = auth_header.replace("Bearer ", "")

        # Try to validate OAuth token
        try:
            token_data = await validate_oauth_token(token)

            if token_data:
                # Get user from OAuth database
                try:
                    user = await get_oauth_user_by_id(token_data["user_id"])

                    if user:
                        return web.json_response(
                            {
                                "id": user["id"],
                                "username": user["username"],
                                "email": user["email"],
                                "avatar": user["avatar"],
                                "name": user.get("name"),
                                "auth_type": "github",
                            }
                        )
                except Exception as oauth_user_error:
                    logger.error(f"Error getting OAuth user: {str(oauth_user_error)}")
                    logger.error(traceback.format_exc())
        except Exception as oauth_error:
            logger.error(f"Error validating OAuth token: {str(oauth_error)}")
            logger.error(traceback.format_exc())

        # For non-OAuth tokens, try to extract user ID from token
        # In a real app with proper JWT, you would decode and validate the token
        try:
            from autothreats import db

            # Initialize the database if it hasn't been initialized yet
            try:
                db.init_db()
            except Exception as db_init_error:
                logger.error(f"Database initialization error: {str(db_init_error)}")
                logger.error(traceback.format_exc())
                # Fall back to mock user if database initialization fails
                return web.json_response(
                    {
                        "id": "1",
                        "username": "admin",
                        "email": "admin@example.com",
                        "avatar": None,
                        "auth_type": "password",
                    }
                )

            # Extract user ID from token (our simple format is "jwt-token-{user_id}")
            if token.startswith("jwt-token-"):
                try:
                    user_id = token.replace("jwt-token-", "")
                    user = db.get_user_by_id(user_id)

                    if user:
                        return web.json_response(
                            {
                                "id": user["id"],
                                "username": user["username"],
                                "email": user["email"],
                                "avatar": None,
                                "auth_type": "password",
                            }
                        )
                except Exception as user_error:
                    logger.error(f"Error getting user from token: {str(user_error)}")
                    logger.error(traceback.format_exc())

            # If token is "mock-jwt-token", return mock user
            if token == "mock-jwt-token":
                return web.json_response(
                    {
                        "id": "1",
                        "username": "admin",
                        "email": "admin@example.com",
                        "avatar": None,
                        "auth_type": "password",
                    }
                )
        except Exception as db_error:
            logger.error(f"Database error: {str(db_error)}")
            logger.error(traceback.format_exc())

        # If we couldn't get a user, return unauthorized
        return web.json_response({"error": "Invalid or expired token"}, status=401)
    except Exception as e:
        logger.error(f"User info error: {str(e)}")
        logger.error(traceback.format_exc())
        return web.json_response(
            {"error": "An error occurred while getting user information"}, status=500
        )


@routes.post("/api/auth/register")
async def register(request):
    """Register a new user"""
    try:
        data = await request.json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Validate input
        if not username or not email or not password:
            return web.json_response(
                {"error": "Username, email, and password are required"}, status=400
            )

        # Use database to create a new user
        from autothreats import db

        # Initialize the database if it hasn't been initialized yet
        try:
            db.init_db()
        except Exception as db_init_error:
            logger.error(f"Database initialization error: {str(db_init_error)}")
            logger.error(traceback.format_exc())
            # Fall back to mock registration if database fails
            return web.json_response(
                {
                    "id": str(uuid.uuid4()),
                    "username": username,
                    "email": email,
                    "avatar": None,
                }
            )

        try:
            # Check if username already exists
            existing_user = db.get_user_by_username(username)
            if existing_user:
                return web.json_response(
                    {"error": "Username already exists"}, status=400
                )

            # Create the user
            user_id = db.create_user(username, password, email, role=db.ROLE_USER)

            if not user_id:
                return web.json_response({"error": "Failed to create user"}, status=500)

            # Get the created user
            user = db.get_user_by_id(user_id)
        except Exception as user_error:
            logger.error(f"User creation error: {str(user_error)}")
            logger.error(traceback.format_exc())
            # Fall back to mock registration if user creation fails
            return web.json_response(
                {
                    "id": str(uuid.uuid4()),
                    "username": username,
                    "email": email,
                    "avatar": None,
                }
            )

        # Try to create an audit record for the registration, but don't fail if it doesn't work
        try:
            client_ip = get_client_ip(request)
            db.create_audit_record(
                action=db.AUDIT_CREATE,
                entity_type="user",
                entity_id=user_id,
                user_id=user_id,
                details={"username": username, "email": email, "ip": client_ip},
                ip_address=client_ip,
            )
        except Exception as audit_error:
            logger.error(f"Audit record creation error: {str(audit_error)}")
            # Continue even if audit record creation fails

        return web.json_response(
            {"id": user_id, "username": username, "email": email, "avatar": None}
        )
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        logger.error(traceback.format_exc())
        # Fall back to mock registration as a last resort
        return web.json_response(
            {
                "id": str(uuid.uuid4()),
                "username": username if "username" in locals() else "unknown",
                "email": email if "email" in locals() else "unknown@example.com",
                "avatar": None,
            }
        )


@routes.post("/api/auth/logout")
async def logout(request):
    """Logout endpoint"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")

            # Extract user ID from token (our simple format is "jwt-token-{user_id}")
            if token.startswith("jwt-token-"):
                try:
                    from autothreats import db

                    # Initialize the database if it hasn't been initialized yet
                    try:
                        db.init_db()
                    except Exception as db_init_error:
                        logger.error(
                            f"Database initialization error during logout: {str(db_init_error)}"
                        )
                        logger.error(traceback.format_exc())
                        # Continue with logout even if database initialization fails

                    user_id = token.replace("jwt-token-", "")

                    # Try to create an audit record for the logout, but don't fail if it doesn't work
                    try:
                        client_ip = get_client_ip(request)
                        db.create_audit_record(
                            action=db.AUDIT_LOGOUT,
                            entity_type="user",
                            entity_id=user_id,
                            user_id=user_id,
                            details={"ip": client_ip},
                            ip_address=client_ip,
                        )
                    except Exception as audit_error:
                        logger.error(
                            f"Audit record creation error during logout: {str(audit_error)}"
                        )
                        logger.error(traceback.format_exc())
                        # Continue even if audit record creation fails
                except Exception as e:
                    logger.error(f"Error processing logout: {str(e)}")
                    logger.error(traceback.format_exc())

        # In a real app with proper token management, you would invalidate the token
        return web.json_response({"success": True})
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        logger.error(traceback.format_exc())
        # Always return success for logout, even if there was an error
        return web.json_response({"success": True})


@routes.get("/api/organization-parameters")
async def get_organization_parameters(request):
    """Get organization parameters"""
    # Return mock organization parameters
    return web.json_response(
        {
            "security_controls": {
                "multi_factor_authentication": {
                    "implemented": True,
                    "strength": "medium",
                    "description": "MFA is required for all administrative access",
                }
            },
            "compliance_requirements": ["PCI DSS", "GDPR"],
            "risk_tolerance": "medium",
        }
    )


@routes.post("/api/organization-parameters")
async def update_organization_parameters(request):
    """Update organization parameters"""
    try:
        # Parse the request data
        data = await request.json()

        # Validate the data
        if not isinstance(data, dict):
            return web.json_response({"error": "Invalid data format"}, status=400)

        # Save to YAML file
        import yaml

        params_path = os.path.join(".", "organization-parameters.yaml")

        with open(params_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

        return web.json_response(
            {"success": True, "message": "Organization parameters updated successfully"}
        )
    except Exception as e:
        logger.error(f"Error updating organization parameters: {str(e)}")
        return web.json_response(
            {
                "success": False,
                "error": f"Error updating organization parameters: {str(e)}",
            },
            status=500,
        )


@routes.get("/api/users")
async def get_users(request):
    """Get all users"""
    # In a real app, you would fetch users from the database
    # For now, just return mock data
    return web.json_response(
        [
            {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com",
                "avatar": None,
            },
            {"id": 2, "username": "user", "email": "user@example.com", "avatar": None},
        ]
    )


@routes.get("/api/events")
async def events(request):
    """SSE endpoint for real-time updates"""
    # Get job ID from query parameters
    job_id = request.query.get("jobId")
    if not job_id:
        return web.json_response({"error": "Job ID is required"}, status=400)

    # Set up SSE response
    response = web.StreamResponse()
    response.headers["Content-Type"] = "text/event-stream"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"

    await response.prepare(request)

    # Register client in sse_clients
    if job_id not in sse_clients:
        sse_clients[job_id] = set()
    sse_clients[job_id].add(response)

    # Get current job status or create a default one
    status_data = job_statuses.get(
        job_id,
        {
            "job_id": job_id,
            "status": "running",
            "progress_percentage": 50,
            "current_stage": "Analyzing code",
            "start_time": int(time.time()) - 60,  # Started 1 minute ago
        },
    )

    # Send initial status
    event_text = f"event: status\ndata: {json.dumps(status_data)}\n\n"
    await response.write(event_text.encode("utf-8"))

    # Keep connection alive
    try:
        for i in range(5):  # Send 5 updates and then stop
            await asyncio.sleep(2)
            progress = 50 + (i + 1) * 10
            event_data = json.dumps(
                {
                    "job_id": job_id,
                    "status": "running" if progress < 100 else "complete",
                    "progress_percentage": progress,
                    "current_stage": (
                        "Finalizing" if progress >= 90 else "Analyzing code"
                    ),
                }
            )
            event_text = f"event: status\ndata: {event_data}\n\n"
            await response.write(event_text.encode("utf-8"))
    except ConnectionResetError:
        # Remove client on connection reset
        if job_id in sse_clients and response in sse_clients[job_id]:
            sse_clients[job_id].remove(response)
        pass

    return response


@routes.get("/api/analyses")
async def get_analyses(request):
    """Get all analyses"""
    print("GET /api/analyses - Fetching all analyses")

    # Check authentication
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        print("Error: Authentication required")
        return web.json_response({"error": "Authentication required"}, status=401)

    # Extract token
    token = auth_header.replace("Bearer ", "")
    print(f"Token: {token[:10]}...")

    # Validate token (simple validation for now)
    if not token.startswith("jwt-token-") and token != "mock-jwt-token":
        try:
            # Try OAuth token validation
            token_data = await validate_oauth_token(token)
            if not token_data:
                print("Error: Invalid or expired token")
                return web.json_response(
                    {"error": "Invalid or expired token"}, status=401
                )
        except Exception as e:
            print(f"Error validating token: {e}")
            return web.json_response({"error": "Invalid or expired token"}, status=401)

    # Print job_statuses
    print(f"Number of jobs in job_statuses: {len(job_statuses)}")
    print(f"Job IDs: {list(job_statuses.keys())}")

    # Convert job_statuses to a list of analyses
    analyses = []
    for job_id, job_status in job_statuses.items():
        print(f"Processing job: {job_id}")
        print(f"Job status: {job_status.get('status', 'unknown')}")

        # Check if the job has a threat model
        threat_model_path = job_status.get("threat_model_path")
        print(f"Threat model path: {threat_model_path}")
        print(f"Path exists: {threat_model_path and os.path.exists(threat_model_path)}")

        threat_model = None

        if threat_model_path and os.path.exists(threat_model_path):
            try:
                with open(threat_model_path, "r") as f:
                    threat_model = json.load(f)
                print(f"Successfully read threat model from file")
            except Exception as e:
                print(f"Error reading threat model file: {e}")
        else:
            # Try to find the threat model in the results directory
            # Use absolute path to results directory
            output_dir = os.path.abspath("./results")
            print(f"Absolute path to results directory: {output_dir}")
            job_dir = os.path.join(output_dir, job_id)
            json_path = os.path.join(job_dir, f"threat_model_{job_id}.json")

            print(f"Trying alternate path: {json_path}")
            print(f"Path exists: {os.path.exists(json_path)}")

            if os.path.exists(json_path):
                try:
                    with open(json_path, "r") as f:
                        threat_model = json.load(f)
                    print(f"Successfully read threat model from alternate path")
                except Exception as e:
                    print(f"Error reading threat model from alternate path: {e}")

        # Create analysis object
        analysis = {
            "id": job_id,
            "name": f"Analysis {job_id[:8]}",
            "repository": job_status.get("repository", {}).get(
                "url", "Unknown repository"
            ),
            "status": job_status.get("status", "unknown"),
            "threat_count": (
                len(threat_model.get("vulnerabilities", [])) if threat_model else 0
            ),
            "critical_threats": (
                len(
                    [
                        v
                        for v in threat_model.get("vulnerabilities", [])
                        if v.get("severity") == "critical"
                    ]
                )
                if threat_model
                else 0
            ),
            "high_threats": (
                len(
                    [
                        v
                        for v in threat_model.get("vulnerabilities", [])
                        if v.get("severity") == "high"
                    ]
                )
                if threat_model
                else 0
            ),
            "medium_threats": (
                len(
                    [
                        v
                        for v in threat_model.get("vulnerabilities", [])
                        if v.get("severity") == "medium"
                    ]
                )
                if threat_model
                else 0
            ),
            "low_threats": (
                len(
                    [
                        v
                        for v in threat_model.get("vulnerabilities", [])
                        if v.get("severity") == "low"
                    ]
                )
                if threat_model
                else 0
            ),
            "owner_name": "admin",  # Default owner
            "owner_avatar": "",
            "collaborators": [],
            "tags": [{"id": 1, "name": "security"}, {"id": 2, "name": "threat-model"}],
            "created_at": datetime.datetime.fromtimestamp(
                job_status.get("start_time", time.time())
            ).isoformat(),
        }

        print(f"Created analysis object: {analysis['id']} - {analysis['name']}")
        analyses.append(analysis)

    # Sort analyses by created_at (newest first)
    analyses.sort(key=lambda x: x["created_at"], reverse=True)

    print(f"Returning {len(analyses)} analyses")
    return web.json_response(analyses)


@routes.get("/api/html-report")
async def get_html_report(request):
    """Get HTML report for a job"""
    # Get job ID from query parameters
    job_id = request.query.get("jobId")

    if not job_id:
        return web.json_response({"error": "Job ID is required"}, status=400)

    # Return a simple HTML report
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Threat Model Report - {job_id}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .section {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>Threat Model Report</h1>
        <div class="section">
            <h2>Executive Summary</h2>
            <p>This is a mock threat model report for job {job_id}.</p>
        </div>
        <div class="section">
            <h2>Vulnerabilities</h2>
            <p>No vulnerabilities found.</p>
        </div>
    </body>
    </html>
    """

    return web.Response(text=html, content_type="text/html")


@routes.post("/api/extensions/run")
async def run_extensions(request):
    """Run all loaded extensions on a codebase"""
    try:
        data = await request.json()
        job_id = data.get("jobId")
        task_type = data.get("taskType", "analyze_code")
        user_id = request.get("user_id")

        # If no user ID is provided, use default
        if user_id is None:
            user_id = DEFAULT_SYSTEM_USER_ID

        if not job_id:
            return web.json_response({"error": "Job ID is required"}, status=400)

        # Get the codebase from the job
        codebase_id = f"codebase_{job_id}"

        # Create audit record for extension execution
        client_ip = get_client_ip(request)
        db.create_audit_record(
            action=db.AUDIT_EXECUTE,
            entity_type="extensions",
            entity_id=job_id,
            user_id=user_id,
            details={"task_type": task_type},
            ip_address=client_ip,
        )

        # Check if we have the orchestrator initialized
        if orchestrator is None:
            await initialize_orchestrator()

        # Get the workspace from the orchestrator
        workspace = orchestrator.workspace

        # Load extensions if configured
        extension_dirs = orchestrator.config.get("extensions", {}).get(
            "directories", []
        )
        if not extension_dirs:
            # Default to examples/extensions if not configured
            extension_dirs = ["./examples/extensions"]

        logger.info(f"Loading and running extensions from: {extension_dirs}")

        # Run the extensions
        results = await load_and_run_extensions(
            workspace=workspace,
            extension_dirs=extension_dirs,
            task_type=task_type,
            task_data={"job_id": job_id, "codebase_id": codebase_id},
        )

        # Store the results in the job results
        if job_id not in job_results:
            job_results[job_id] = {}

        job_results[job_id]["extensions"] = results

        # Save the results to a file
        job_dir = os.path.join("./results", job_id)
        os.makedirs(job_dir, exist_ok=True)

        extensions_path = os.path.join(job_dir, f"extensions_results{job_id}.json")
        with open(extensions_path, "w") as f:
            json.dump(results, f, indent=2)

        logger.info(f"Saved extension results to: {extensions_path}")

        # Return the results
        return web.json_response({"success": True, "jobId": job_id, "results": results})

    except Exception as e:
        logger.error(f"Error running extensions: {str(e)}")
        logger.exception(e)

        return web.json_response(
            {"success": False, "error": f"Error running extensions: {str(e)}"},
            status=500,
        )


async def send_sse_event(job_id: str, event_type: str, data: dict):
    """
    Send an SSE event to all clients subscribed to a job.

    Args:
        job_id: The ID of the job
        event_type: The type of event
        data: The event data
    """
    if job_id not in sse_clients:
        return

    # Prepare the event data
    event_text = f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
    event_data = event_text.encode("utf-8")

    # Send to all clients
    clients_to_remove = set()
    for client in sse_clients[job_id]:
        try:
            await client.write(event_data)
        except Exception as e:
            # If there's an error, mark the client for removal
            clients_to_remove.add(client)
            logger.warning(f"Error sending SSE event to client: {str(e)}")

    # Remove disconnected clients
    sse_clients[job_id] -= clients_to_remove


async def _monitor_progress(job_id: str, orchestrator_config: dict, job_data: dict):
    """
    Monitor the progress of a job and update the job status.

    Args:
        job_id: The ID of the job
        orchestrator_config: The orchestrator configuration
        job_data: The job data
    """
    try:
        # Create and initialize the orchestrator using the class imported at module level
        # This allows it to be mocked in tests
        orchestrator = SimplifiedOrchestrator(orchestrator_config)
        await orchestrator.initialize()

        # Update job status
        job_statuses[job_id]["current_stage"] = "Running analysis"
        job_statuses[job_id]["progress_percentage"] = 15

        # Send status update via SSE
        await send_sse_event(job_id, "status", job_statuses[job_id])

        # Process the job
        results = await orchestrator.process_job(job_data)

        # Update job status
        job_statuses[job_id]["status"] = "complete"
        job_statuses[job_id]["progress_percentage"] = 100
        job_statuses[job_id]["current_stage"] = "Complete"
        job_statuses[job_id]["end_time"] = int(time.time())

        # Create output directory
        output_dir = job_statuses[job_id].get("output_dir", "./results")
        job_dir = os.path.join(output_dir, job_id)
        os.makedirs(job_dir, exist_ok=True)

        # Save threat model to file
        threat_model = {
            "id": job_id,
            "job_id": job_id,
            "title": f"Threat Model for Job {job_id}",
            "vulnerabilities": results.get("results", {})
            .get("threat_detection", {})
            .get("vulnerabilities", []),
            "threat_scenarios": results.get("results", {})
            .get("threat_detection", {})
            .get("threat_scenarios", []),
            "executive_summary": results.get("results", {}).get(
                "executive_summary", ""
            ),
            "generated_at": int(time.time()),
        }

        # Save JSON
        json_path = os.path.join(job_dir, f"threat_model_{job_id}.json")
        with open(json_path, "w") as f:
            json.dump(threat_model, f, indent=2)

        # Save HTML
        html_path = os.path.join(job_dir, f"threat_model_{job_id}.html")
        with open(html_path, "w") as f:
            f.write(
                f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Threat Model Report - {job_id}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1 {{ color: #333; }}
                    .section {{ margin-bottom: 20px; }}
                    .vulnerability {{ border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }}
                    .high {{ border-left: 5px solid #d9534f; }}
                    .medium {{ border-left: 5px solid #f0ad4e; }}
                    .low {{ border-left: 5px solid #5bc0de; }}
                </style>
            </head>
            <body>
                <h1>Threat Model Report</h1>
                <div class="section">
                    <h2>Executive Summary</h2>
                    <p>{threat_model["executive_summary"]}</p>
                </div>
                <div class="section">
                    <h2>Vulnerabilities</h2>
                    {"".join([f'''
                    <div class="vulnerability {vuln.get('severity', 'medium')}">
                        <h3>{vuln.get('type', 'Unknown')}</h3>
                        <p><strong>Severity:</strong> {vuln.get('severity', 'medium')}</p>
                        <p><strong>Location:</strong> {vuln.get('file_path', 'Unknown')}:{vuln.get('line', 'Unknown')}</p>
                        <p><strong>Description:</strong> {vuln.get('description', 'No description')}</p>
                        <p><strong>Remediation:</strong> {vuln.get('remediation', 'No remediation advice')}</p>
                    </div>
                    ''' for vuln in threat_model["vulnerabilities"]]) if threat_model["vulnerabilities"] else "<p>No vulnerabilities found.</p>"}
                </div>
            </body>
            </html>
            """
            )

        # Update job status with file paths
        job_statuses[job_id]["threat_model_path"] = json_path
        job_statuses[job_id]["html_report_path"] = html_path

        # Send final status update via SSE
        await send_sse_event(job_id, "status", job_statuses[job_id])
        await send_sse_event(job_id, "complete", {"message": "Analysis complete"})

        # Shutdown the orchestrator
        await orchestrator.shutdown()

    except Exception as e:
        # Update job status on error
        job_statuses[job_id]["status"] = "error"
        job_statuses[job_id]["error"] = str(e)
        job_statuses[job_id]["end_time"] = int(time.time())

        # Send error update via SSE
        await send_sse_event(job_id, "status", job_statuses[job_id])
        await send_sse_event(job_id, "error", {"message": str(e)})

        logger.error(f"Error monitoring job progress: {str(e)}")


async def create_app():
    """Create and configure the aiohttp web application"""
    global orchestrator

    app = web.Application()
    app.add_routes(routes)

    # Configure CORS
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            )
        },
    )

    # Apply CORS to all routes
    for route in list(app.router.routes()):
        cors.add(route)

    # Add middleware, configure app settings, etc. here if needed

    # Initialize the database if needed
    if hasattr(db, "init_db"):
        db.init_db()

    # Initialize the orchestrator if it hasn't been initialized yet
    if orchestrator is None:
        orchestrator = await initialize_orchestrator()
        app["orchestrator"] = orchestrator

    return app


if __name__ == "__main__":
    import asyncio

    async def run_app():
        # Create the application
        app = await create_app()

        # Run the application
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        await site.start()

        print("Server started at http://0.0.0.0:8080")

        # Keep the server running
        while True:
            await asyncio.sleep(3600)  # Sleep for an hour

    # Run the async application
    asyncio.run(run_app())
