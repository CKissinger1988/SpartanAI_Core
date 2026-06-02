import json
import socket
import sys
import os
import time
import logging
from zeroconf import ServiceBrowser, Zeroconf, ServiceListener

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IoTManager")

class IoTListener(ServiceListener):
    def __init__(self):
        self.devices = []

    def update_service(self, zc, type_, name):
        pass

    def remove_service(self, zc, type_, name):
        pass

    def add_service(self, zc, type_, name):
        info = zc.get_service_info(type_, name)
        if info:
            addresses = [socket.inet_ntoa(addr) for addr in info.addresses]
            device = {
                "name": name,
                "type": type_,
                "addresses": addresses,
                "port": info.port,
                "properties": {k.decode('utf-8') if isinstance(k, bytes) else k: v.decode('utf-8') if isinstance(v, bytes) else v for k, v in info.properties.items()},
                "server": info.server
            }
            self.devices.append(device)

def scan_iot():
    logger.info("Starting IoT Network Discovery (mDNS)...")
    zeroconf = Zeroconf()
    listener = IoTListener()
    # Common IoT service types
    services = ["_http._tcp.local.", "_hap._tcp.local.", "_esphomelib._tcp.local.", "_wled._tcp.local.", "_mqtt._tcp.local."]
    
    browsers = []
    for service in services:
        browsers.append(ServiceBrowser(zeroconf, service, listener))
    
    # Wait for discovery
    time.sleep(3)
    zeroconf.close()
    
    return listener.devices

def control_device(ip, port, path, method="POST", data=None):
    import urllib.request
    url = f"http://{ip}:{port}{path}"
    logger.info(f"Sending {method} to {url}")
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, method=method)
        req.add_header('Content-Type', 'application/json')
        # Apex-Grade mandate: ensure secure identification
        req.add_header('X-SpartanAI-ID', 'SupremeCore-Operational')
        
        with urllib.request.urlopen(req, timeout=2) as response:
            return {"status": "success", "response": response.read().decode()}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "scan":
            print(json.dumps(scan_iot()))
        elif cmd == "control" and len(sys.argv) > 4:
            ip = sys.argv[2]
            port = sys.argv[3]
            path = sys.argv[4]
            method = sys.argv[5] if len(sys.argv) > 5 else "POST"
            # Optional data handling could be added here
            print(json.dumps(control_device(ip, port, path, method)))
    else:
        # Default to scan if no args
        print(json.dumps(scan_iot()))
