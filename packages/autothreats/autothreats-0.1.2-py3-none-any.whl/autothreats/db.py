"""
Database module for Threat Canvas.
This module provides a SQLite database for storing user data, analysis jobs, system configuration,
and audit trails for evidence-grade auditing.
"""

import hashlib
import json
import logging
import os
import sqlite3
import time
import traceback
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Database file path
DB_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "threat_canvas.db"
)

# User roles
ROLE_ADMIN = "admin"
ROLE_USER = "user"

# Audit action types
AUDIT_CREATE = "create"
AUDIT_READ = "read"
AUDIT_UPDATE = "update"
AUDIT_DELETE = "delete"
AUDIT_LOGIN = "login"
AUDIT_LOGOUT = "logout"


def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT UNIQUE,
        role TEXT NOT NULL,
        created_at INTEGER NOT NULL,
        last_login INTEGER,
        settings TEXT
    )
    """
    )

    # Create jobs table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        status TEXT NOT NULL,
        progress_percentage INTEGER DEFAULT 0,
        current_stage TEXT,
        start_time INTEGER NOT NULL,
        end_time INTEGER,
        config TEXT NOT NULL,
        result_path TEXT,
        error TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
    )

    # Create system_config table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS system_config (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at INTEGER NOT NULL,
        updated_by TEXT,
        FOREIGN KEY (updated_by) REFERENCES users(id)
    )
    """
    )

    # Insert default admin user if not exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = ?", (ROLE_ADMIN,))
    if cursor.fetchone()[0] == 0:
        # Create default admin user
        create_user(
            username="admin",
            password="admin",  # This should be changed on first login
            email="admin@example.com",
            role=ROLE_ADMIN,
        )

    # Create audit_trail table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS audit_trail (
        id TEXT PRIMARY KEY,
        timestamp INTEGER NOT NULL,
        user_id TEXT,
        action TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        entity_id TEXT,
        details TEXT,
        ip_address TEXT,
        hash TEXT NOT NULL
    )
    """
    )

    # Create vulnerabilities table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS vulnerabilities (
        id TEXT PRIMARY KEY,
        job_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        severity TEXT NOT NULL,
        cwe TEXT,
        location TEXT,
        line_number INTEGER,
        recommendation TEXT,
        status TEXT NOT NULL,
        created_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL,
        created_by TEXT,
        updated_by TEXT,
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    )
    """
    )

    # Create threat_models table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS threat_models (
        id TEXT PRIMARY KEY,
        job_id TEXT NOT NULL,
        title TEXT NOT NULL,
        executive_summary TEXT,
        metadata TEXT,
        created_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL,
        created_by TEXT,
        updated_by TEXT,
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    )
    """
    )

    # Create agent_results table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS agent_results (
        id TEXT PRIMARY KEY,
        job_id TEXT NOT NULL,
        agent_id TEXT NOT NULL,
        result_data TEXT NOT NULL,
        created_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL,
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    )
    """
    )

    # Insert default system configuration if not exists
    default_config = {
        "api_server_port": 8080,
        "ui_server_port": 3000,
        "default_output_dir": "./results",
        "default_llm_provider": "openai",
        "default_openai_model": "gpt-4o-mini",
        "default_anthropic_model": "claude-3-sonnet-20240229",
        "enable_multi_stage_by_default": False,
        "enable_agentic_by_default": True,
        "enable_redflag_by_default": False,
        "enable_codeshield_by_default": False,
        "enable_audit_trail": True,
        "audit_retention_days": 90,
    }

    for key, value in default_config.items():
        cursor.execute("SELECT COUNT(*) FROM system_config WHERE key = ?", (key,))
        if cursor.fetchone()[0] == 0:
            set_system_config(key, value)

    conn.commit()
    conn.close()


def create_user(
    username: str, password: str, email: str = None, role: str = ROLE_USER
) -> str:
    """Create a new user in the database."""
    # Hash the password using SHA-256
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    user_id = str(uuid.uuid4())
    created_at = int(time.time())

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (id, username, password_hash, email, role, created_at, settings) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, password_hash, email, role, created_at, json.dumps({})),
        )
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        # User already exists
        return None
    finally:
        conn.close()


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get a user by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash, email, role, created_at, last_login, settings FROM users WHERE id = ?",
        (user_id,),
    )
    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            "id": user[0],
            "username": user[1],
            "password_hash": user[2],
            "email": user[3],
            "role": user[4],
            "created_at": user[5],
            "last_login": user[6],
            "settings": json.loads(user[7]) if user[7] else {},
        }

    return None


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Get a user by username."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash, email, role, created_at, last_login, settings FROM users WHERE username = ?",
        (username,),
    )
    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            "id": user[0],
            "username": user[1],
            "password_hash": user[2],
            "email": user[3],
            "role": user[4],
            "created_at": user[5],
            "last_login": user[6],
            "settings": json.loads(user[7]) if user[7] else {},
        }

    return None


def get_user(username: str) -> Optional[Dict[str, Any]]:
    """Get a user by username (legacy function, use get_user_by_username instead)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash, email, role, created_at, last_login, settings FROM users WHERE username = ?",
        (username,),
    )
    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            "id": user[0],
            "username": user[1],
            "password_hash": user[2],
            "email": user[3],
            "role": user[4],
            "created_at": user[5],
            "last_login": user[6],
            "settings": json.loads(user[7]) if user[7] else {},
        }

    return None


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate a user with username and password."""
    user = get_user_by_username(username)

    if not user:
        return None

    # Hash the password and compare with stored hash
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user["password_hash"] == password_hash:
        # Update last login time
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        last_login = int(time.time())
        cursor.execute(
            "UPDATE users SET last_login = ? WHERE id = ?", (last_login, user["id"])
        )
        conn.commit()
        conn.close()

        user["last_login"] = last_login
        return user

    return None


def create_job(user_id: Optional[str], config: Dict[str, Any]) -> str:
    """Create a new job in the database."""
    job_id = str(uuid.uuid4())
    start_time = int(time.time())

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO jobs (id, user_id, status, current_stage, start_time, config) VALUES (?, ?, ?, ?, ?, ?)",
        (job_id, user_id, "running", "Initializing", start_time, json.dumps(config)),
    )

    conn.commit()
    conn.close()

    return job_id


def update_job_status(
    job_id: str,
    status: str,
    progress_percentage: int = None,
    current_stage: str = None,
    end_time: int = None,
    result_path: str = None,
    error: str = None,
) -> bool:
    """Update the status of a job."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Build the update query dynamically based on provided parameters
    update_fields = ["status = ?"]
    params = [status]

    if progress_percentage is not None:
        update_fields.append("progress_percentage = ?")
        params.append(progress_percentage)

    if current_stage is not None:
        update_fields.append("current_stage = ?")
        params.append(current_stage)

    if end_time is not None:
        update_fields.append("end_time = ?")
        params.append(end_time)

    if result_path is not None:
        update_fields.append("result_path = ?")
        params.append(result_path)

    if error is not None:
        update_fields.append("error = ?")
        params.append(error)

    # Add job_id to params
    params.append(job_id)

    query = f"UPDATE jobs SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(query, params)

    success = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return success


def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    """Get a job by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, user_id, status, progress_percentage, current_stage, start_time, end_time, config, result_path, error FROM jobs WHERE id = ?",
        (job_id,),
    )

    job = cursor.fetchone()
    conn.close()

    if job:
        return {
            "id": job[0],
            "user_id": job[1],
            "status": job[2],
            "progress_percentage": job[3],
            "current_stage": job[4],
            "start_time": job[5],
            "end_time": job[6],
            "config": json.loads(job[7]) if job[7] else {},
            "result_path": job[8],
            "error": job[9],
        }

    return None


def get_latest_job() -> Optional[Dict[str, Any]]:
    """Get the most recent job."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, user_id, status, progress_percentage, current_stage, start_time, end_time, config, result_path, error FROM jobs ORDER BY start_time DESC LIMIT 1"
    )

    job = cursor.fetchone()
    conn.close()

    if job:
        return {
            "id": job[0],
            "user_id": job[1],
            "status": job[2],
            "progress_percentage": job[3],
            "current_stage": job[4],
            "start_time": job[5],
            "end_time": job[6],
            "config": json.loads(job[7]) if job[7] else {},
            "result_path": job[8],
            "error": job[9],
        }

    return None


def get_user_jobs(
    user_id: str, limit: int = 10, offset: int = 0
) -> List[Dict[str, Any]]:
    """Get jobs for a specific user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, user_id, status, progress_percentage, current_stage, start_time, end_time, config, result_path, error FROM jobs WHERE user_id = ? ORDER BY start_time DESC LIMIT ? OFFSET ?",
        (user_id, limit, offset),
    )

    jobs = cursor.fetchall()
    conn.close()

    return [
        {
            "id": job[0],
            "user_id": job[1],
            "status": job[2],
            "progress_percentage": job[3],
            "current_stage": job[4],
            "start_time": job[5],
            "end_time": job[6],
            "config": json.loads(job[7]) if job[7] else {},
            "result_path": job[8],
            "error": job[9],
        }
        for job in jobs
    ]


def set_system_config(key: str, value: Any, updated_by: str = None) -> bool:
    """Set a system configuration value."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    updated_at = int(time.time())
    value_json = json.dumps(value)

    try:
        cursor.execute(
            "INSERT OR REPLACE INTO system_config (key, value, updated_at, updated_by) VALUES (?, ?, ?, ?)",
            (key, value_json, updated_at, updated_by),
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error setting system config: {e}")
        return False
    finally:
        conn.close()


def get_system_config(key: str, default: Any = None) -> Any:
    """Get a system configuration value."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM system_config WHERE key = ?", (key,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return json.loads(result[0])

    return default


def get_all_system_config() -> Dict[str, Any]:
    """Get all system configuration values."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT key, value FROM system_config")
    results = cursor.fetchall()

    conn.close()

    return {key: json.loads(value) for key, value in results}


def create_audit_record(
    action: str,
    entity_type: str,
    entity_id: Optional[str] = None,
    user_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
) -> str:
    """Create an audit trail record for an action."""
    if not get_system_config("enable_audit_trail", True):
        return None

    audit_id = str(uuid.uuid4())
    timestamp = int(time.time())
    details_json = json.dumps(details) if details else None

    # Create a hash of the audit record for integrity verification
    hash_input = f"{audit_id}|{timestamp}|{user_id}|{action}|{entity_type}|{entity_id}|{details_json}|{ip_address}"
    hash_value = hashlib.sha256(hash_input.encode()).hexdigest()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO audit_trail (id, timestamp, user_id, action, entity_type, entity_id, details, ip_address, hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                audit_id,
                timestamp,
                user_id,
                action,
                entity_type,
                entity_id,
                details_json,
                ip_address,
                hash_value,
            ),
        )
        conn.commit()
        logger.debug(f"Audit record created: {action} {entity_type} {entity_id}")
        return audit_id
    except Exception as e:
        logger.error(f"Error creating audit record: {e}")
        return None
    finally:
        conn.close()


def get_audit_records(
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    """Get audit trail records with optional filtering."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "SELECT id, timestamp, user_id, action, entity_type, entity_id, details, ip_address, hash FROM audit_trail WHERE 1=1"
    params = []

    if entity_type:
        query += " AND entity_type = ?"
        params.append(entity_type)

    if entity_id:
        query += " AND entity_id = ?"
        params.append(entity_id)

    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)

    if action:
        query += " AND action = ?"
        params.append(action)

    if start_time:
        query += " AND timestamp >= ?"
        params.append(start_time)

    if end_time:
        query += " AND timestamp <= ?"
        params.append(end_time)

    query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    records = cursor.fetchall()
    conn.close()

    return [
        {
            "id": record[0],
            "timestamp": record[1],
            "timestamp_formatted": datetime.fromtimestamp(record[1]).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "user_id": record[2],
            "action": record[3],
            "entity_type": record[4],
            "entity_id": record[5],
            "details": json.loads(record[6]) if record[6] else None,
            "ip_address": record[7],
            "hash": record[8],
        }
        for record in records
    ]


def verify_audit_record_integrity(audit_id: str) -> bool:
    """Verify the integrity of an audit record by checking its hash."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, timestamp, user_id, action, entity_type, entity_id, details, ip_address, hash FROM audit_trail WHERE id = ?",
        (audit_id,),
    )

    record = cursor.fetchone()
    conn.close()

    if not record:
        return False

    # Recreate the hash input
    hash_input = f"{record[0]}|{record[1]}|{record[2]}|{record[3]}|{record[4]}|{record[5]}|{record[6]}|{record[7]}"
    computed_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    # Compare with the stored hash
    return computed_hash == record[8]


def create_vulnerability(
    job_id: str,
    name: str,
    description: str,
    severity: str,
    cwe: Optional[str] = None,
    location: Optional[str] = None,
    line_number: Optional[int] = None,
    recommendation: Optional[str] = None,
    status: str = "open",
    user_id: Optional[str] = None,
) -> str:
    """Create a new vulnerability in the database."""
    vuln_id = str(uuid.uuid4())
    created_at = int(time.time())

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO vulnerabilities
            (id, job_id, name, description, severity, cwe, location, line_number, recommendation, status, created_at, updated_at, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                vuln_id,
                job_id,
                name,
                description,
                severity,
                cwe,
                location,
                line_number,
                recommendation,
                status,
                created_at,
                created_at,
                user_id,
                user_id,
            ),
        )
        conn.commit()

        # Create audit record
        create_audit_record(
            action=AUDIT_CREATE,
            entity_type="vulnerability",
            entity_id=vuln_id,
            user_id=user_id,
            details={
                "job_id": job_id,
                "name": name,
                "severity": severity,
                "status": status,
            },
        )

        return vuln_id
    except Exception as e:
        logger.error(f"Error creating vulnerability: {e}")
        return None
    finally:
        conn.close()


def get_vulnerability(vuln_id: str) -> Optional[Dict[str, Any]]:
    """Get a vulnerability by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, job_id, name, description, severity, cwe, location, line_number, recommendation, status,
        created_at, updated_at, created_by, updated_by FROM vulnerabilities WHERE id = ?""",
        (vuln_id,),
    )

    vuln = cursor.fetchone()
    conn.close()

    if vuln:
        return {
            "id": vuln[0],
            "job_id": vuln[1],
            "name": vuln[2],
            "description": vuln[3],
            "severity": vuln[4],
            "cwe": vuln[5],
            "location": vuln[6],
            "line_number": vuln[7],
            "recommendation": vuln[8],
            "status": vuln[9],
            "created_at": vuln[10],
            "updated_at": vuln[11],
            "created_by": vuln[12],
            "updated_by": vuln[13],
        }

    return None


def get_job_vulnerabilities(job_id: str) -> List[Dict[str, Any]]:
    """Get all vulnerabilities for a specific job."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, job_id, name, description, severity, cwe, location, line_number, recommendation, status,
        created_at, updated_at, created_by, updated_by FROM vulnerabilities WHERE job_id = ? ORDER BY severity, name""",
        (job_id,),
    )

    vulns = cursor.fetchall()
    conn.close()

    return [
        {
            "id": vuln[0],
            "job_id": vuln[1],
            "name": vuln[2],
            "description": vuln[3],
            "severity": vuln[4],
            "cwe": vuln[5],
            "location": vuln[6],
            "line_number": vuln[7],
            "recommendation": vuln[8],
            "status": vuln[9],
            "created_at": vuln[10],
            "updated_at": vuln[11],
            "created_by": vuln[12],
            "updated_by": vuln[13],
        }
        for vuln in vulns
    ]


def update_vulnerability(
    vuln_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    severity: Optional[str] = None,
    cwe: Optional[str] = None,
    location: Optional[str] = None,
    line_number: Optional[int] = None,
    recommendation: Optional[str] = None,
    status: Optional[str] = None,
    user_id: Optional[str] = None,
) -> bool:
    """Update a vulnerability in the database."""
    # Get current vulnerability data for audit trail
    current_vuln = get_vulnerability(vuln_id)
    if not current_vuln:
        return False

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Build the update query dynamically based on provided parameters
    update_fields = ["updated_at = ?", "updated_by = ?"]
    params = [int(time.time()), user_id]

    if name is not None:
        update_fields.append("name = ?")
        params.append(name)

    if description is not None:
        update_fields.append("description = ?")
        params.append(description)

    if severity is not None:
        update_fields.append("severity = ?")
        params.append(severity)

    if cwe is not None:
        update_fields.append("cwe = ?")
        params.append(cwe)

    if location is not None:
        update_fields.append("location = ?")
        params.append(location)

    if line_number is not None:
        update_fields.append("line_number = ?")
        params.append(line_number)

    if recommendation is not None:
        update_fields.append("recommendation = ?")
        params.append(recommendation)

    if status is not None:
        update_fields.append("status = ?")
        params.append(status)

    # Add vuln_id to params
    params.append(vuln_id)

    try:
        query = f"UPDATE vulnerabilities SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, params)

        success = cursor.rowcount > 0
        conn.commit()

        if success:
            # Create audit record with changes
            changes = {}
            if name is not None and name != current_vuln["name"]:
                changes["name"] = {"old": current_vuln["name"], "new": name}
            if description is not None and description != current_vuln["description"]:
                changes["description"] = {
                    "old": current_vuln["description"],
                    "new": description,
                }
            if severity is not None and severity != current_vuln["severity"]:
                changes["severity"] = {"old": current_vuln["severity"], "new": severity}
            if status is not None and status != current_vuln["status"]:
                changes["status"] = {"old": current_vuln["status"], "new": status}

            create_audit_record(
                action=AUDIT_UPDATE,
                entity_type="vulnerability",
                entity_id=vuln_id,
                user_id=user_id,
                details={"job_id": current_vuln["job_id"], "changes": changes},
            )

        return success
    except Exception as e:
        logger.error(f"Error updating vulnerability: {e}")
        return False
    finally:
        conn.close()


def create_threat_model(
    job_id: str,
    title: str,
    executive_summary: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None,
) -> str:
    """Create a new threat model in the database."""
    model_id = str(uuid.uuid4())
    created_at = int(time.time())
    metadata_json = json.dumps(metadata) if metadata else None

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO threat_models
            (id, job_id, title, executive_summary, metadata, created_at, updated_at, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                model_id,
                job_id,
                title,
                executive_summary,
                metadata_json,
                created_at,
                created_at,
                user_id,
                user_id,
            ),
        )
        conn.commit()

        # Create audit record
        create_audit_record(
            action=AUDIT_CREATE,
            entity_type="threat_model",
            entity_id=model_id,
            user_id=user_id,
            details={"job_id": job_id, "title": title},
        )

        return model_id
    except Exception as e:
        logger.error(f"Error creating threat model: {e}")
        return None
    finally:
        conn.close()


def get_threat_model(model_id: str) -> Optional[Dict[str, Any]]:
    """Get a threat model by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, job_id, title, executive_summary, metadata, created_at, updated_at, created_by, updated_by
        FROM threat_models WHERE id = ?""",
        (model_id,),
    )

    model = cursor.fetchone()
    conn.close()

    if model:
        return {
            "id": model[0],
            "job_id": model[1],
            "title": model[2],
            "executive_summary": model[3],
            "metadata": json.loads(model[4]) if model[4] else None,
            "created_at": model[5],
            "updated_at": model[6],
            "created_by": model[7],
            "updated_by": model[8],
        }

    return None


def get_job_threat_model(job_id: str) -> Optional[Dict[str, Any]]:
    """Get the threat model for a specific job."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, job_id, title, executive_summary, metadata, created_at, updated_at, created_by, updated_by
        FROM threat_models WHERE job_id = ?""",
        (job_id,),
    )

    model = cursor.fetchone()
    conn.close()

    if model:
        # Get vulnerabilities for this job
        vulnerabilities = get_job_vulnerabilities(job_id)

        return {
            "id": model[0],
            "job_id": model[1],
            "title": model[2],
            "executive_summary": model[3],
            "metadata": json.loads(model[4]) if model[4] else None,
            "created_at": model[5],
            "updated_at": model[6],
            "created_by": model[7],
            "updated_by": model[8],
            "vulnerabilities": vulnerabilities,
        }

    return None


def save_agent_result(
    job_id: str,
    agent_id: str,
    result_data: Dict[str, Any],
    user_id: Optional[str] = None,
) -> str:
    """Save agent result data to the database."""
    result_id = str(uuid.uuid4())
    created_at = int(time.time())
    result_json = json.dumps(result_data)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO agent_results
            (id, job_id, agent_id, result_data, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (result_id, job_id, agent_id, result_json, created_at, created_at),
        )
        conn.commit()

        # Create audit record
        create_audit_record(
            action=AUDIT_CREATE,
            entity_type="agent_result",
            entity_id=result_id,
            user_id=user_id,
            details={"job_id": job_id, "agent_id": agent_id},
        )

        return result_id
    except Exception as e:
        logger.error(f"Error saving agent result: {e}")
        return None
    finally:
        conn.close()


def get_agent_result(job_id: str, agent_id: str) -> Optional[Dict[str, Any]]:
    """Get agent result data from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, result_data, created_at, updated_at
        FROM agent_results WHERE job_id = ? AND agent_id = ?
        ORDER BY created_at DESC LIMIT 1""",
        (job_id, agent_id),
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "id": result[0],
            "job_id": job_id,
            "agent_id": agent_id,
            "result_data": json.loads(result[1]),
            "created_at": result[2],
            "updated_at": result[3],
        }

    return None


def get_all_agent_results(job_id: str) -> Dict[str, Any]:
    """Get all agent results for a specific job."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, agent_id, result_data, created_at, updated_at
        FROM agent_results WHERE job_id = ?
        ORDER BY agent_id, created_at DESC""",
        (job_id,),
    )

    results = cursor.fetchall()
    conn.close()

    # Group by agent_id, taking the most recent result for each agent
    agent_results = {}
    seen_agents = set()

    for result in results:
        agent_id = result[1]
        if agent_id not in seen_agents:
            agent_results[agent_id] = {
                "id": result[0],
                "job_id": job_id,
                "agent_id": agent_id,
                "result_data": json.loads(result[2]),
                "created_at": result[3],
                "updated_at": result[4],
            }
            seen_agents.add(agent_id)

    return agent_results


# Wrap original functions to add audit trail
original_create_job = create_job


def create_job(user_id: Optional[str], config: Dict[str, Any]) -> str:
    """Create a new job with audit trail."""
    job_id = original_create_job(user_id, config)
    if job_id:
        create_audit_record(
            action=AUDIT_CREATE,
            entity_type="job",
            entity_id=job_id,
            user_id=user_id,
            details={"config": config},
        )
    return job_id


original_update_job_status = update_job_status


def update_job_status(
    job_id: str,
    status: str,
    progress_percentage: int = None,
    current_stage: str = None,
    end_time: int = None,
    result_path: str = None,
    error: str = None,
    user_id: Optional[str] = None,
) -> bool:
    """Update job status with audit trail."""
    success = original_update_job_status(
        job_id,
        status,
        progress_percentage,
        current_stage,
        end_time,
        result_path,
        error,
        user_id,
    )
    if success:
        details = {"status": status}
        if progress_percentage is not None:
            details["progress_percentage"] = progress_percentage
        if current_stage is not None:
            details["current_stage"] = current_stage
        if end_time is not None:
            details["end_time"] = end_time
        if result_path is not None:
            details["result_path"] = result_path
        if error is not None:
            details["error"] = error

        create_audit_record(
            action=AUDIT_UPDATE,
            entity_type="job",
            entity_id=job_id,
            user_id=user_id,
            details=details,
        )
    return success


original_set_system_config = set_system_config


def set_system_config(key: str, value: Any, updated_by: str = None) -> bool:
    """Set system configuration with audit trail."""
    success = original_set_system_config(key, value, updated_by)
    if success:
        create_audit_record(
            action=AUDIT_UPDATE,
            entity_type="system_config",
            entity_id=key,
            user_id=updated_by,
            details={"value": value},
        )
    return success


# Initialize the database when the module is imported
init_db()
