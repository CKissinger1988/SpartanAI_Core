import qrcode
import json
import os
import secrets
import sys

# Pathing
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
TOKEN_FILE = os.path.join(BACKEND_DIR, ".persistent_tokens.json")

def generate_pairing_payload():
    """Generates a secure JSON payload for QR pairing."""
    # 1. Fetch current Uplink data
    uplink_path = os.path.join(BASE_DIR, "MASTER_UPLINK.json")
    if not os.path.exists(uplink_path):
        return None, "MASTER_UPLINK.json not found. Ensure Tor is initialized."
    
    with open(uplink_path, 'r') as f:
        uplink = json.load(f)
        
    # 2. Fetch 2FA secret
    secret_path = os.path.join(BACKEND_DIR, ".2fa_secret")
    if not os.path.exists(secret_path):
        return None, "2FA Secret not found. Run auth_2fa.py first."
    
    with open(secret_path, 'r') as f:
        totp_secret = f.read().strip()
        
    # 3. Generate a long-term 'Passkey' (Access Token)
    passkey = secrets.token_urlsafe(32)
    
    # Store passkey locally for verification
    tokens = {}
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            tokens = json.load(f)
    
    tokens[uplink['instance_id']] = passkey
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f, indent=4)

    payload = {
        "id": uplink['instance_id'],
        "onion": uplink['onion_address'],
        "port": uplink['port'],
        "totp": totp_secret,
        "passkey": passkey,
        "v": "3.3.2"
    }
    
    return payload, None

def create_qr_code():
    print("[*] Generating Secure Pairing QR Code...")
    payload, error = generate_pairing_payload()
    
    if error:
        print(f"[!] Error: {error}")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(payload))
    qr.make(fit=True)

    img = qr.make_image(fill_color="green", back_color="black")
    output_path = os.path.join(BASE_DIR, "NEXUS_PAIRING_QR.png")
    img.save(output_path)
    
    print(f"[+] Pairing QR Code saved to: {output_path}")
    print("[*] Scan this in the NexusAI Mobile Hub for persistent uplink.")

if __name__ == "__main__":
    create_qr_code()
