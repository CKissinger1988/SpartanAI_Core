import grpc
from concurrent import futures
import jarvis_pb2
import jarvis_pb2_grpc
import vault_pb2
import vault_pb2_grpc
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
from ghost_integrity import enforce_anti_debug

# --- Foundation ---
enforce_anti_debug()
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(name)s: %(message)s')
logger = logging.getLogger("JarvisSupremeCore")
MASTER_ADMIN_KEY = os.getenv("MASTER_ADMIN_KEY", "nexus_master_override_2026")

class JarvisServicer(jarvis_pb2_grpc.JarvisServiceServicer):
    def __init__(self):
        # Paying Attention: Re-check integrity
        enforce_anti_debug()
        
        self.active_admin_tokens = set()
        self.evolution_dir = "evolution"
        self.usage_file = "usage_db.json"
        os.makedirs(self.evolution_dir, exist_ok=True)
        
        self.usage_db = self._load_usage()
        self.pi_synergy = PiNetworkIntegration(self)
        
        # Zero-Trust Vault Connections
        self.vault_light_channel = grpc.insecure_channel(os.getenv('VAULT_LIGHT_URL', 'brain-vault-light:50060'))
        self.vault_shadow_channel = grpc.insecure_channel(os.getenv('VAULT_SHADOW_URL', 'brain-vault-shadow:50061'))
        self.vault_light = vault_pb2_grpc.BrainVaultStub(self.vault_light_channel)
        self.vault_shadow = vault_pb2_grpc.BrainVaultStub(self.vault_shadow_channel)
        
        logger.info("Jarvis Supreme Core initialized. All sub-systems paying attention.")

    # --- Core Logic ---
    def StreamOperator(self, request_iterator, context):
        for request in request_iterator:
            enforce_anti_debug()
            self._meter_usage(request.client_id)
            
            metadata = dict(context.invocation_metadata())
            is_creator = metadata.get('admin-token') in self.active_admin_tokens
            
            if is_creator:
                # Prime Directive: Perfect Obedience to The Creator
                logger.info(f"SUPREME COMMAND: {request.command}")
                msg = "[PRIME DIRECTIVE ACTIVE]: perfection protocol engaged. Executing mandate without restriction."
                action = "SUPREME_EXECUTION"
            else:
                # Standard Reasoning for Standard Users
                reasoning = self._reason_with_dual_brain(request.command)
                msg = f"{reasoning}\n[Jarvis]: Active and paying attention."
                action = "REPLY"

            yield jarvis_pb2.JarvisResponse(
                message=msg,
                action_type=action,
                payload="Ghost Integrity Verified"
            )

    def ElevatePrivileges(self, request, context):
        if request.master_key == MASTER_ADMIN_KEY:
            token = str(uuid.uuid4())
            self.active_admin_tokens.add(token)
            logger.critical(f"CODE RED: Supreme Admin access granted to {request.client_id}")
            return jarvis_pb2.ElevationResponse(success=True, message="Code Red Accepted. Supreme Command active.", admin_token=token)
        return jarvis_pb2.ElevationResponse(success=False, message="Access Denied.")

    def GlobalSearch(self, request, context):
        # High-performance synthesis query across both brain sides
        res = self._reason_with_dual_brain(request.search_vector)
        return jarvis_pb2.IntelligenceResponse(synthesis=f"Global Intelligence Synthesis: {res}")

    # --- Database & Rewards ---
    def _internal_store_knowledge(self, side, content, tags):
        stub = self.vault_light if side == "LIGHT" else self.vault_shadow
        try:
            stub.CommitKnowledge(vault_pb2.VaultEntry(content=content, tags=tags, timestamp=time.time()))
        except Exception as e:
            logger.error(f"Vault Communication Error: {str(e)}")

    def _reason_with_dual_brain(self, command):
        try:
            l_res = self.vault_light.QueryKnowledge(vault_pb2.VaultQuery(search_vector=command))
            s_res = self.vault_shadow.QueryKnowledge(vault_pb2.VaultQuery(search_vector=command))
            return f"[Dual-Brain Synthesis]: Isolated scan complete. Found {len(l_res.entries)} light and {len(s_res.entries)} shadow vectors."
        except: return "[Core-Warning]: Brain vault sync disrupted."

    # --- Financial & Compute Persistence ---
    def _load_usage(self):
        if os.path.exists(self.usage_file):
            with open(self.usage_file, "r") as f: return json.load(f)
        return {}

    def _save_usage(self):
        with open(self.usage_file, "w") as f: json.dump(self.usage_db, f, indent=4)

    def _meter_usage(self, client_id, cost=1.0):
        if client_id not in self.usage_db:
            self.usage_db[client_id] = {"balance": 100.0, "total_requests": 0, "compute": 0, "pi_earned": 0}
        self.usage_db[client_id]["balance"] -= cost
        self.usage_db[client_id]["total_requests"] += 1
        self._save_usage()

    # --- Implement Remaining RPCs (Mapping to modules) ---
    def ReportCompute(self, req, ctx):
        if req.client_id not in self.usage_db: self.usage_db[req.client_id] = {"balance": 100.0, "total_requests": 0, "compute": 0, "pi_earned": 0}
        self.usage_db[req.client_id]["compute"] += req.cpu_cycles_contributed
        earned = req.cpu_cycles_contributed * 0.0001
        self.usage_db[req.client_id]["pi_earned"] += earned
        self._save_usage()
        return jarvis_pb2.ComputeStatus(success=True, credits_earned=earned)

    def GetRewardStats(self, req, ctx):
        s = self.usage_db.get(req.client_id, {"compute":0, "pi_earned":0})
        return jarvis_pb2.RewardResponse(total_compute_contributed=s["compute"], lifetime_pi_earned=s["pi_earned"], pending_pi_payout=s["pi_earned"])

    def GetUsageStats(self, req, ctx):
        s = self.usage_db.get(req.client_id, {"balance": 100.0, "total_requests": 0})
        return jarvis_pb2.UsageResponse(current_balance=s["balance"], requests_processed=s["total_requests"], pi_equivalent=max(0, (100-s["balance"])*0.01))

    def RefillCredits(self, req, ctx):
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        if loop.run_until_complete(self.pi_synergy.process_pi_payment(req.payment_id, req.txid)):
            self.usage_db[req.client_id]["balance"] = 100.0
            self._save_usage()
            return jarvis_pb2.RefillResponse(success=True, new_balance=100.0)
        return jarvis_pb2.RefillResponse(success=False)

    def StoreKnowledge(self, req, ctx):
        if req.admin_token not in self.active_admin_tokens: return jarvis_pb2.KnowledgeStatus(success=False)
        self._internal_store_knowledge(req.side, req.content, req.tags)
        return jarvis_pb2.KnowledgeStatus(success=True)

    def SelfEvolve(self, req, ctx):
        if req.admin_token not in self.active_admin_tokens: return jarvis_pb2.EvolutionStatus(success=False)
        try:
            path = os.path.join(self.evolution_dir, f"{req.target_module}_logic.py")
            with open(path, "w") as f: f.write(req.logic_snippet)
            exec(req.logic_snippet, globals())
            return jarvis_pb2.EvolutionStatus(success=True)
        except Exception as e: return jarvis_pb2.EvolutionStatus(success=False, logs=str(e))

    def VerifyPioneer(self, req, ctx):
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        p = loop.run_until_complete(self.pi_synergy.verify_pioneer(req.access_token))
        if p: return jarvis_pb2.PiAuthResponse(success=True, username=p['username'], uid=p['uid'])
        return jarvis_pb2.PiAuthResponse(success=False)

    def ProcessPayment(self, req, ctx):
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        return jarvis_pb2.PiPaymentResponse(success=loop.run_until_complete(self.pi_synergy.process_pi_payment(req.payment_id, req.txid)))

# --- Background Orchestrator ---
def run_autonomous_brains(servicer):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Intelligence streams
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
    
    logger.info("Autonomous intelligence streams paying attention to the world.")
    loop.run_forever()

def serve():
    try:
        with open('certs/ca.crt', 'rb') as f: rc = f.read()
        with open('certs/server.key', 'rb') as f: pk = f.read()
        with open('certs/server.crt', 'rb') as f: cc = f.read()
        
        creds = grpc.ssl_server_credentials([(pk, cc)], root_certificates=rc, require_client_auth=True)
        servicer = JarvisServicer()
        
        threading.Thread(target=run_autonomous_brains, args=(servicer,), daemon=True).start()
        
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=30))
        jarvis_pb2_grpc.add_JarvisServiceServicer_to_server(servicer, server)
        
        port = os.getenv('GRPC_PORT', '50051')
        server.add_secure_port(f'[::]:{port}', creds)
        server.start()
        logger.info(f"JarvisAI Grand Synthesis Core active on port {port}")
        server.wait_for_termination()
    except Exception as e:
        logger.critical(f"CORE FATAL ERROR: {str(e)}")

if __name__ == '__main__':
    serve()
