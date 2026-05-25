import os, sys, secrets, logging
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PayloadEncryptor")
def encrypt_directory(source_dir, dest_dir, key):
    aesgcm = AESGCM(key)
    for root, dirs, files in os.walk(source_dir):
        rel_path = os.path.relpath(root, source_dir)
        target_root = os.path.join(dest_dir, rel_path)
        os.makedirs(target_root, exist_ok=True)
        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_root, file + ".enc")
            try:
                with open(source_file, "rb") as f: data = f.read()
                nonce = secrets.token_bytes(12)
                ciphertext = aesgcm.encrypt(nonce, data, None)
                with open(target_file, "wb") as f: f.write(nonce + ciphertext)
            except Exception as e:
                logger.error("Failed to encrypt: " + str(e))
def main():
    logger.info("[ENCRYPTOR] Initiating Apex-Grade Payload Encryption...")
    key = AESGCM.generate_key(bit_length=256)
    key_path = os.path.join(os.path.dirname(__file__), "..", "ISO_DECRYPTION_KEY.bin")
    with open(key_path, "wb") as f: f.write(key)
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    source_backend = os.path.join(base_dir, "backend")
    dest_encrypted = os.path.join(base_dir, "encrypted_payload")
    if not os.path.exists(dest_encrypted): os.makedirs(dest_encrypted)
    encrypt_directory(source_backend, os.path.join(dest_encrypted, "backend"), key)
    logger.info("[ENCRYPTOR] Encryption Complete.")
if __name__ == "__main__": main()