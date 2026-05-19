import http.server
import socketserver
import json
import sqlite3
import os
import datetime
from urllib.parse import urlparse, parse_qs

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
    def do_POST(self):
        if self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                instance_id = data.get('instance_id')
                onion = data.get('onion_address')
                status = data.get('status', 'online')
                meta = json.dumps(data.get('metadata', {}))
                
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
                ''', (instance_id, onion, status, datetime.datetime.now().isoformat(), meta))
                conn.commit()
                conn.close()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            except Exception as e:
                self.send_error(400, str(e))

    def do_GET(self):
        if self.path == '/list':
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('SELECT instance_id, onion_address, status, last_seen, metadata FROM instances')
                rows = cursor.fetchall()
                conn.close()
                
                instances = []
                for r in rows:
                    instances.append({
                        "id": r[0],
                        "onion": r[1],
                        "status": r[2],
                        "last_seen": r[3],
                        "metadata": json.loads(r[4])
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
        print(f"NEXUS C2 REGISTRY ACTIVE ON PORT {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
