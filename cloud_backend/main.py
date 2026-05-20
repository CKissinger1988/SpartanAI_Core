import grpc
from concurrent import futures
import jarvis_pb2
import jarvis_pb2_grpc
import time
import os
import uuid
import json
import asyncio
import threading
from intelligence_scraper import WebIntelligenceScraper
from omni_intelligence import OmniIntelligenceScraper
from peer_learning import AIPeerLearning
from pi_synergy import PiNetworkIntegration, PiIntelligenceScraper

# Master Admin Key
MASTER_ADMIN_KEY = os.getenv("MASTER_ADMIN_KEY", "nexus_master_override_2026")

class JarvisServicer(jarvis_pb2_grpc.JarvisServiceServicer):
    def __init__(self):
        self.active_admin_tokens = set()
        self.evolution_dir = "evolution"
        self.knowledge_dir = "knowledge"
        self.usage_file = "usage_db.json"
        os.makedirs(self.evolution_dir, exist_ok=True)
        os.makedirs(self.knowledge_dir, exist_ok=True)
        
        self.light_brain = self._load_knowledge("LIGHT")
        self.shadow_brain = self._load_knowledge("SHADOW")
        self.usage_db = self._load_usage()
        
        self.pi_synergy = PiNetworkIntegration(self)
        self.pi_rate = 0.01 # 1 Credit = 0.01 Pi

    def _load_usage(self):
        if os.path.exists(self.usage_file):
            with open(self.usage_file, "r") as f: return json.load(f)
        return {}

    def _save_usage(self):
        with open(self.usage_file, "w") as f: json.dump(self.usage_db, f, indent=4)

    def _meter_usage(self, client_id, cost=1.0):
        if client_id not in self.usage_db:
            self.usage_db[client_id] = {"balance": 100.0, "total_requests": 0}
        self.usage_db[client_id]["balance"] -= cost
        self.usage_db[client_id]["total_requests"] += 1
        self._save_usage()

    def StreamOperator(self, request_iterator, context):
        for request in request_iterator:
            self._meter_usage(request.client_id)
            metadata = dict(context.invocation_metadata())
            is_admin = metadata.get('admin-token') in self.active_admin_tokens
            reasoning = self._reason_with_dual_brain(request.command)
            yield jarvis_pb2.JarvisResponse(
                message=f"{reasoning}\n[Jarvis]: Metered session active.",
                action_type="REPLY",
                payload="Pi-Billing Active"
            )

    def GetUsageStats(self, request, context):
        stats = self.usage_db.get(request.client_id, {"balance": 100.0, "total_requests": 0})
        # Cost to refill to 100
        refill_needed = 100.0 - stats["balance"]
        pi_cost = max(0, refill_needed * self.pi_rate)
        return jarvis_pb2.UsageResponse(
            current_balance=stats["balance"],
            requests_processed=stats["total_requests"],
            pi_equivalent=pi_cost
        )

    def RefillCredits(self, request, context):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # Verify payment with Pi Blockchain
        success = loop.run_until_complete(self.pi_synergy.process_pi_payment(request.payment_id, request.txid))
        if success:
            self.usage_db[request.client_id]["balance"] = 100.0
            self._save_usage()
            return jarvis_pb2.RefillResponse(success=True, new_balance=100.0)
        return jarvis_pb2.RefillResponse(success=False, new_balance=0)

    def ElevatePrivileges(self, request, context):
        if request.master_key == MASTER_ADMIN_KEY:
            token = str(uuid.uuid4())
            self.active_admin_tokens.add(token)
            return jarvis_pb2.ElevationResponse(success=True, message="Admin granted.", admin_token=token)
        return jarvis_pb2.ElevationResponse(success=False, message="Denied.", admin_token="")

    def StoreKnowledge(self, request, context):
        if request.admin_token not in self.active_admin_tokens:
            return jarvis_pb2.KnowledgeStatus(success=False, message="Unauthorized.")
        self._internal_store_knowledge(request.side, request.content, request.tags)
        return jarvis_pb2.KnowledgeStatus(success=True, message=f"Stored in {request.side}.")

    def VerifyPioneer(self, request, context):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        pioneer = loop.run_until_complete(self.pi_synergy.verify_pioneer(request.access_token))
        if pioneer: return jarvis_pb2.PiAuthResponse(success=True, username=pioneer['username'], uid=pioneer['uid'])
        return jarvis_pb2.PiAuthResponse(success=False)

    def ProcessPayment(self, request, context):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(self.pi_synergy.process_pi_payment(request.payment_id, request.txid))
        return jarvis_pb2.PiPaymentResponse(success=success, message="Payment finalized" if success else "Failed")

    def _internal_store_knowledge(self, side, content, tags):
        target_brain = self.light_brain if side == "LIGHT" else self.shadow_brain
        target_brain.append({"content": content, "tags": tags, "timestamp": time.time()})
        self._save_knowledge(side, target_brain)

    def _reason_with_dual_brain(self, command):
        light_matches = [k for k in self.light_brain if any(t in command for t in k['tags'].split(','))]
        shadow_matches = [k for k in self.shadow_brain if any(t in command for t in k['tags'].split(','))]
        output = "[Metered-Reasoning]: "
        if light_matches: output += f"Positive protocols found ({len(light_matches)}). "
        if shadow_matches: output += f"Adversarial vectors identified ({len(shadow_matches)}). "
        return output

    def _load_knowledge(self, side):
        path = os.path.join(self.knowledge_dir, f"{side.lower()}_knowledge.json")
        if os.path.exists(path):
            with open(path, "r") as f: return json.load(f)
        return []

    def _save_knowledge(self, side, data):
        path = os.path.join(self.knowledge_dir, f"{side.lower()}_knowledge.json")
        with open(path, "w") as f: json.dump(data, f, indent=4)

def run_scrapers(servicer):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    threat_scraper = WebIntelligenceScraper(servicer)
    omni_scraper = OmniIntelligenceScraper(servicer)
    peer_learning = AIPeerLearning(servicer)
    pi_scraper = PiIntelligenceScraper(servicer)
    loop.create_task(threat_scraper.run_autonomous_cycle())
    loop.create_task(omni_scraper.run_omni_cycle())
    loop.create_task(peer_learning.run_peer_learning_cycle())
    loop.create_task(pi_scraper.run_pi_cycle())
    loop.run_forever()

def serve():
    with open('certs/ca.crt', 'rb') as f: root_certs = f.read()
    with open('certs/server.key', 'rb') as f: private_key = f.read()
    with open('certs/server.crt', 'rb') as f: certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials([(private_key, certificate_chain)], root_certificates=root_certs, require_client_auth=True)
    servicer = JarvisServicer()
    scraper_thread = threading.Thread(target=run_scrapers, args=(servicer,), daemon=True)
    scraper_thread.start()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jarvis_pb2_grpc.add_JarvisServiceServicer_to_server(servicer, server)
    server.add_secure_port('[::]:50051', server_credentials)
    server.start()
    print("JarvisAI Omni-Core with Metered Pi Billing Online...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
