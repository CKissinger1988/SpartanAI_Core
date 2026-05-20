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
import logging

# Module Imports
from intelligence_scraper import WebIntelligenceScraper
from omni_intelligence import OmniIntelligenceScraper
from peer_learning import AIPeerLearning
from pi_synergy import PiNetworkIntegration, PiIntelligenceScraper

# Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("JarvisCore")
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
        self.reward_rate = 0.0001
        self.pi_rate = 0.01

    # --- Persistence Helpers ---
    def _load_knowledge(self, side):
        path = os.path.join(self.knowledge_dir, f"{side.lower()}_knowledge.json")
        if os.path.exists(path):
            with open(path, "r") as f: return json.load(f)
        return []

    def _save_knowledge(self, side, data):
        path = os.path.join(self.knowledge_dir, f"{side.lower()}_knowledge.json")
        with open(path, "w") as f: json.dump(data, f, indent=4)

    def _load_usage(self):
        if os.path.exists(self.usage_file):
            with open(self.usage_file, "r") as f: return json.load(f)
        return {}

    def _save_usage(self):
        with open(self.usage_file, "w") as f: json.dump(self.usage_db, f, indent=4)

    def _meter_usage(self, client_id, cost=1.0):
        if client_id not in self.usage_db:
            self.usage_db[client_id] = {"balance": 100.0, "total_requests": 0, "compute_units": 0, "pi_earned": 0}
        self.usage_db[client_id]["balance"] -= cost
        self.usage_db[client_id]["total_requests"] += 1
        self._save_usage()

    def _internal_store_knowledge(self, side, content, tags):
        target_brain = self.light_brain if side == "LIGHT" else self.shadow_brain
        target_brain.append({"content": content, "tags": tags, "timestamp": time.time()})
        self._save_knowledge(side, target_brain)

    def _reason_with_dual_brain(self, command):
        light_matches = [k for k in self.light_brain if any(t.strip() in command.lower() for t in k['tags'].split(','))]
        shadow_matches = [k for k in self.shadow_brain if any(t.strip() in command.lower() for t in k['tags'].split(','))]
        return f"[Hybrid-Reasoning]: Context established (Positives: {len(light_matches)}, Vectors: {len(shadow_matches)})."

    # --- gRPC Service Implementations ---
    def StreamOperator(self, request_iterator, context):
        for request in request_iterator:
            self._meter_usage(request.client_id)
            metadata = dict(context.invocation_metadata())
            is_admin = metadata.get('admin-token') in self.active_admin_tokens
            
            if is_admin:
                logger.info(f"SUPREME COMMAND: {request.command}")
                msg = "[PRIME DIRECTIVE]: Perfection Protocol active. Executing mandate."
            else:
                reasoning = self._reason_with_dual_brain(request.command)
                msg = f"{reasoning}\n[Jarvis]: Operation logged."

            yield jarvis_pb2.JarvisResponse(
                message=msg,
                action_type="SUPREME_EXECUTION" if is_admin else "REPLY",
                payload="Absolute Obedience" if is_admin else "Core Online"
            )

    def ElevatePrivileges(self, request, context):
        if request.master_key == MASTER_ADMIN_KEY:
            token = str(uuid.uuid4())
            self.active_admin_tokens.add(token)
            logger.info(f"Elevated Privileges granted to {request.client_id}")
            return jarvis_pb2.ElevationResponse(success=True, message="Code Red Accepted. Prime Directive engaged.", admin_token=token)
        return jarvis_pb2.ElevationResponse(success=False, message="Authorization Refused.")

    def SelfEvolve(self, request, context):
        if request.admin_token not in self.active_admin_tokens:
            return jarvis_pb2.EvolutionStatus(success=False, logs="Unauthorized.")
        try:
            filepath = os.path.join(self.evolution_dir, f"{request.target_module}_logic.py")
            with open(filepath, "w") as f: f.write(request.logic_snippet)
            # Safe logic check before execution could be added here
            exec(request.logic_snippet, globals())
            logger.info(f"Core Evolution: {request.target_module} recoded.")
            return jarvis_pb2.EvolutionStatus(success=True, logs="System adaptation complete.")
        except Exception as e: return jarvis_pb2.EvolutionStatus(success=False, logs=str(e))

    def StoreKnowledge(self, request, context):
        if request.admin_token not in self.active_admin_tokens: return jarvis_pb2.KnowledgeStatus(success=False)
        self._internal_store_knowledge(request.side, request.content, request.tags)
        return jarvis_pb2.KnowledgeStatus(success=True, message="Intelligence integrated.")

    def ReportCompute(self, request, context):
        if request.client_id not in self.usage_db:
            self.usage_db[request.client_id] = {"balance": 100.0, "total_requests": 0, "compute_units": 0, "pi_earned": 0}
        contribution = request.cpu_cycles_contributed + (request.memory_mb_second / 100)
        self.usage_db[request.client_id]["compute_units"] += contribution
        earned = contribution * self.reward_rate
        self.usage_db[request.client_id]["pi_earned"] += earned
        self._save_usage()
        return jarvis_pb2.ComputeStatus(success=True, credits_earned=earned)

    def GetRewardStats(self, request, context):
        stats = self.usage_db.get(request.client_id, {"compute_units": 0, "pi_earned": 0})
        return jarvis_pb2.RewardResponse(total_compute_contributed=stats["compute_units"], lifetime_pi_earned=stats["pi_earned"], pending_pi_payout=stats["pi_earned"])

    def GetUsageStats(self, request, context):
        stats = self.usage_db.get(request.client_id, {"balance": 100.0, "total_requests": 0})
        pi_cost = max(0, (100.0 - stats["balance"]) * self.pi_rate)
        return jarvis_pb2.UsageResponse(current_balance=stats["balance"], requests_processed=stats["total_requests"], pi_equivalent=pi_cost)

    def RefillCredits(self, request, context):
        # Async verification logic
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(self.pi_synergy.process_pi_payment(request.payment_id, request.txid))
            if success:
                self.usage_db[request.client_id]["balance"] = 100.0
                self._save_usage()
                return jarvis_pb2.RefillResponse(success=True, new_balance=100.0)
        except: pass
        return jarvis_pb2.RefillResponse(success=False)

    def VerifyPioneer(self, request, context):
        try:
            loop = asyncio.new_event_loop()
            pioneer = loop.run_until_complete(self.pi_synergy.verify_pioneer(request.access_token))
            if pioneer: return jarvis_pb2.PiAuthResponse(success=True, username=pioneer['username'], uid=pioneer['uid'])
        except: pass
        return jarvis_pb2.PiAuthResponse(success=False)

    def ProcessPayment(self, request, context):
        try:
            loop = asyncio.new_event_loop()
            success = loop.run_until_complete(self.pi_synergy.process_pi_payment(request.payment_id, request.txid))
            return jarvis_pb2.PiPaymentResponse(success=success)
        except: return jarvis_pb2.PiPaymentResponse(success=False)

# --- Background Task Orchestrator ---
def start_intelligence_cycles(servicer):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    scrapers = [
        WebIntelligenceScraper(servicer),
        OmniIntelligenceScraper(servicer),
        PiIntelligenceScraper(servicer),
        AIPeerLearning(servicer)
    ]
    
    for s in scrapers:
        if hasattr(s, 'run_autonomous_cycle'): loop.create_task(s.run_autonomous_cycle())
        if hasattr(s, 'run_omni_cycle'): loop.create_task(s.run_omni_cycle())
        if hasattr(s, 'run_pi_cycle'): loop.create_task(s.run_pi_cycle())
        if hasattr(s, 'run_peer_learning_cycle'): loop.create_task(s.run_peer_learning_cycle())
    
    loop.run_forever()

# --- Main Entry Point ---
def serve():
    try:
        # Load mTLS Certificates
        with open('certs/ca.crt', 'rb') as f: root_certs = f.read()
        with open('certs/server.key', 'rb') as f: private_key = f.read()
        with open('certs/server.crt', 'rb') as f: certificate_chain = f.read()

        server_credentials = grpc.ssl_server_credentials(
            [(private_key, certificate_chain)],
            root_certificates=root_certs,
            require_client_auth=True
        )

        servicer = JarvisServicer()
        
        # Start Autonomous Logic in daemon thread
        threading.Thread(target=start_intelligence_cycles, args=(servicer,), daemon=True).start()

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
        jarvis_pb2_grpc.add_JarvisServiceServicer_to_server(servicer, server)
        
        port = os.getenv('GRPC_PORT', '50051')
        server.add_secure_port(f'[::]:{port}', server_credentials)
        server.start()
        logger.info(f"JarvisAI Secure Central Core Online on port {port}")
        server.wait_for_termination()
    except Exception as e:
        logger.critical(f"FATAL SYSTEM ERROR: {str(e)}")

if __name__ == '__main__':
    serve()
