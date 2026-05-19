import http.server
import socketserver
import json
import sqlite3
import os
import datetime
import sys
from urllib.parse import urlparse, parse_qs

# CNSA utility path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'JarvisAI_Stable'))
try:
    import config_manager
except ImportError:
    config_manager = None

DB_PATH = os.path.join(os.path.dirname(__file__), 'nexus_c2.db')
PORT = 9091

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instance_id TEXT UNIQUE,
            onion_address TEXT,
            status TEXT,
            last_seen TEXT,
            metadata TEXT
        )
    ''')
    conn.commit()
    conn.close()

class C2Handler(http.server.BaseHTTPRequestHandler):
    def _get_key(self):
        if config_manager:
            return config_manager.generate_master_key()
        return None

    def do_POST(self):
        if self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                instance_id = data.get('instance_id')
                onion = data.get('onion_address')
                status = data.get('status', 'online')
                meta_raw = json.dumps(data.get('metadata', {}))
                
                # CNSA Layer: Encrypt sensitive onion and metadata at rest
                key = self._get_key()
                if key:
                    onion = config_manager.aes_256_gcm_encrypt(onion.encode(), key).decode()
                    meta_raw = config_manager.aes_256_gcm_encrypt(meta_raw.encode(), key).decode()

                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO instances (instance_id, onion_address, status, last_seen, metadata)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(instance_id) DO UPDATE SET
                        onion_address=excluded.onion_address,
                        status=excluded.status,
                        last_seen=excluded.last_seen,
                        metadata=excluded.metadata
                ''', (instance_id, onion, status, datetime.datetime.now().isoformat(), meta_raw))
                conn.commit()
                conn.close()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "enc": "AES-256-GCM"}).encode())
            except Exception as e:
                self.send_error(400, str(e))

    def do_GET(self):
        if self.path == '/list':
            try:
                key = self._get_key()
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('SELECT instance_id, onion_address, status, last_seen, metadata FROM instances')
                rows = cursor.fetchall()
                conn.close()
                
                instances = []
                for r in rows:
                    onion = r[1]
                    meta = r[4]
                    if key:
                        try:
                            onion = config_manager.aes_256_gcm_decrypt(onion.encode(), key).decode()
                            meta = config_manager.aes_256_gcm_decrypt(meta.encode(), key).decode()
                        except: pass # fallback to raw if decryption fails

                    instances.append({
                        "id": r[0],
                        "onion": onion,
                        "status": r[2],
                        "last_seen": r[3],
                        "metadata": json.loads(meta) if isinstance(meta, str) and meta.startswith('{') else {}
                    })
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(instances).encode())
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404)

def run_server():
    init_db()
    with socketserver.TCPServer(("", PORT), C2Handler) as httpd:
        print(f"NEXUS C2 REGISTRY ACTIVE [CNSA MODE] ON PORT {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
