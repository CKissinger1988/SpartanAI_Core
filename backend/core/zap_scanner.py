import time
import os
import subprocess
from zapv2 import ZAPv2

class ZapScanner:
    """
    Automated DAST Shard using OWASP ZAP.
    Mandate: Identify web vulnerabilities autonomously in the integration pipeline.
    """
    def __init__(self, target_url="http://localhost:3001"):
        self.target = target_url
        self.zap = ZAPv2(apikey=os.environ.get("ZAP_API_KEY", "changeme"))

    def start_scan(self):
        """Engages the ZAP scan."""
        print(f"[ZAP-SCAN]: Initiating DAST on {self.target}...")
        try:
            # Spider the target
            scan_id = self.zap.spider.scan(self.target)
            while int(self.zap.spider.status(scan_id)) < 100:
                time.sleep(2)
            
            # Active scan
            ascan_id = self.zap.ascan.scan(self.target)
            while int(self.zap.ascan.status(ascan_id)) < 100:
                time.sleep(5)
            
            alerts = self.zap.core.alerts(baseurl=self.target)
            return f"Scan complete. Found {len(alerts)} alerts."
        except Exception as e:
            return f"[ZAP-SCAN-ERROR]: {e}"

if __name__ == "__main__":
    scanner = ZapScanner()
    print(scanner.start_scan())
