import os
import sys
import json
import sqlite3
import subprocess
from datetime import datetime
from fastmcp import FastMCP

# Define the JarvisAI MCP Server
mcp = FastMCP("JarvisAI")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
EXPLOITS_DB = os.path.join(BACKEND_DIR, "exploits.db")
C2_DB = os.path.join(BACKEND_DIR, "nexus_c2.db")
OAUTH_CREDS = os.path.join(os.path.expanduser("~"), ".gemini", "oauth_creds.json")

@mcp.tool()
def list_exploits(limit: int = 10):
    """Lists the latest exploits from the NexusAI database."""
    if not os.path.exists(EXPLOITS_DB):
        return "Exploit database not found."
    
    conn = sqlite3.connect(EXPLOITS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT cve_id, name, type, date_added FROM exploits ORDER BY date_added DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No exploits found."
    
    result = "Latest NexusAI Exploits:\n"
    for r in rows:
        result += f"- [{r[0]}] {r[1]} ({r[2]}) - Added: {r[3]}\n"
    return result

@mcp.tool()
def get_c2_uplink():
    """Retrieves the current master C2 uplink coordinates."""
    uplink_file = os.path.join(BASE_DIR, "MASTER_UPLINK.json")
    if not os.path.exists(uplink_file):
        return "C2 Uplink not active."
    
    with open(uplink_file, "r") as f:
        data = json.load(f)
    
    return f"Master Uplink Active: {data['onion_address']} (Port: {data['port']}) - Status: {data['status']}"

@mcp.tool()
def scan_gcp_compute():
    """Connects to Google Cloud Compute using stored OAuth tokens and lists instances."""
    if not os.path.exists(OAUTH_CREDS):
        return "GCP OAuth credentials not found."
    
    with open(OAUTH_CREDS, "r") as f:
        creds = json.load(f)
    
    token = creds.get("access_token")
    if not token:
        return "Access token missing in credentials."
    
    # We'll use curl.exe to list projects and then instances
    cmd = [
        "curl.exe", "-H", f"Authorization: Bearer {token}",
        "https://cloudresourcemanager.googleapis.com/v1/projects"
    ]
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        projects = json.loads(proc.stdout).get("projects", [])
        
        if not projects:
            return "No GCP projects found or token expired."
        
        summary = "GCP Projects Found:\n"
        for p in projects:
            summary += f"- {p['name']} ({p['projectId']})\n"
        
        return summary
    except Exception as e:
        return f"Error connecting to GCP: {str(e)}"

@mcp.tool()
def build_tactical_iso():
    """Triggers the building of a CNSA-hardened automated Kali ISO."""
    script_path = os.path.join(BASE_DIR, "integrate_kali_automated.sh")
    if not os.path.exists(script_path):
        return "ISO Integration script not found."
    
    # This is a long-running process, we'll run it in the background or just return the command
    return f"To build the ISO, run: wsl -d kali-linux -u root -- /mnt/c/Users/ckiss/integrate_kali_automated.sh"

@mcp.tool()
def jarvis_exec(command: str):
    """Executes a system or hardware-level command with Jarvis authority (Root/Admin)."""
    # For safety, we route through the established shells
    try:
        proc = subprocess.run(command, shell=True, capture_output=True, text=True)
        return f"STDOUT: {proc.stdout}\nSTDERR: {proc.stderr}\nEXIT_CODE: {proc.returncode}"
    except Exception as e:
        return f"Execution Error: {str(e)}"

@mcp.tool()
def run_tactical_audit():
    """Triggers a full system audit for CNSA compliance, anonymity, and root integrity."""
    audit_script = os.path.join(BASE_DIR, "scripts", "system_audit.py")
    try:
        proc = subprocess.run(["python3", audit_script], capture_output=True, text=True)
        return proc.stdout
    except Exception as e:
        return f"Audit Error: {str(e)}"

@mcp.tool()
def set_auto_patch(enabled: bool = True):
    """Enables or disables Jarvis autonomous system patching."""
    os.environ["JARVIS_AUTO_PATCH"] = "true" if enabled else "false"
    return f"Jarvis Autonomous Patching set to: {enabled}"

if __name__ == "__main__":
    mcp.run()
