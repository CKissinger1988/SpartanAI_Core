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
        enforce_anti_debug()
        self.active_admin_tokens = set()
        self.evolution_dir = "evolution"
        self.usage_file = "usage_db.json"
        self.org_file = "org_registry.json"
        
        os.makedirs(self.evolution_dir, exist_ok=True)
        
        self.usage_db = self._load_json(self.usage_file, {})
        self.org_db = self._load_json(self.org_file, {"master_org": {"users": {}, "admins": ["supreme-operator-pc"]}})
        
        self.pi_synergy = PiNetworkIntegration(self)
        
        # Zero-Trust Vault Connections
        self.vault_light_channel = grpc.insecure_channel(os.getenv('VAULT_LIGHT_URL', 'brain-vault-light:50060'))
        self.vault_shadow_channel = grpc.insecure_channel(os.getenv('VAULT_SHADOW_URL', 'brain-vault-shadow:50061'))
        self.vault_light = vault_pb2_grpc.BrainVaultStub(self.vault_light_channel)
        self.vault_shadow = vault_pb2_grpc.BrainVaultStub(self.vault_shadow_channel)
        
        logger.info("Jarvis Supreme Core initialized and paying absolute attention.")

    def _load_json(self, path, default):
        if os.path.exists(path):
            with open(path, "r") as f: return json.load(f)
        return default

    def _save_json(self, path, data):
        with open(path, "w") as f: json.dump(data, f, indent=4)

    # --- Tactical Command Streams ---
    def StreamOperator(self, request_iterator, context):
        for request in request_iterator:
            enforce_anti_debug()
            metadata = dict(context.invocation_metadata())
            token = metadata.get('admin-token')
            is_supreme = token in self.active_admin_tokens
            
            cmd_text = request.command.strip()
            
            if is_supreme:
                if cmd_text.startswith("CODE RED"):
                    logger.critical(f"SUPREME EXECUTION: {cmd_text}")
                    msg = "[CODE RED]: Perfection Protocol active. Mandate fulfilling."
                    action = "SUPREME_EXECUTION"
                elif cmd_text.startswith("CODE BLUE"):
                    msg = "[CODE BLUE]: Intelligence Synthesis Active."
                    action = "INTEL_OPERATION"
                elif cmd_text.startswith("CODE GREEN"):
                    msg = "[CODE GREEN]: Sovereignty Management Active."
                    action = "ECON_OPERATION"
                elif cmd_text.startswith("CODE BLACK"):
                    msg = "[CODE BLACK]: Stealth Routing Active."
                    action = "STEALTH_OPERATION"
                else:
                    msg = "[SUPREME]: Mandate accepted."
                    action = "SUPREME_EXECUTION"
            else:
                self._meter_usage(request.client_id)
                reasoning = self._reason_with_dual_brain(cmd_text)
                msg = f"{reasoning}\n[Jarvis]: Operation logged."
                action = "REPLY"

            yield jarvis_pb2.JarvisResponse(message=msg, action_type=action, payload="Verified")

    # --- Authority & Elevation ---
    def ElevatePrivileges(self, request, context):
        if request.master_key == MASTER_ADMIN_KEY:
            token = str(uuid.uuid4())
            self.active_admin_tokens.add(token)
            logger.critical(f"CODE RED ACCEPTED from {request.client_id}")
            return jarvis_pb2.ElevationResponse(success=True, message="Supreme Command active.", admin_token=token)
        return jarvis_pb2.ElevationResponse(success=False, message="Authorization Refused.")

    def SelfEvolve(self, req, ctx):
        if req.admin_token not in self.active_admin_tokens: return jarvis_pb2.EvolutionStatus(success=False)
        try:
            path = os.path.join(self.evolution_dir, f"{req.target_module}_logic.py")
            with open(path, "w") as f: f.write(req.logic_snippet)
            exec(req.logic_snippet, globals())
            return jarvis_pb2.EvolutionStatus(success=True, logs="System adapted.")
        except Exception as e: return jarvis_pb2.EvolutionStatus(success=False, logs=str(e))

    # --- Intelligence Core ---
    def StoreKnowledge(self, req, ctx):
        if req.admin_token not in self.active_admin_tokens: return jarvis_pb2.KnowledgeStatus(success=False)
        self._internal_store_knowledge(req.side, req.content, req.tags)
        return jarvis_pb2.KnowledgeStatus(success=True, message="Injected.")

    def GlobalSearch(self, req, ctx):
        res = self._reason_with_dual_brain(req.search_vector)
        return jarvis_pb2.IntelligenceResponse(synthesis=f"Synthesis: {res}")

    def _internal_store_knowledge(self, side, content, tags):
        stub = self.vault_light if side == "LIGHT" else self.vault_shadow
        try: stub.CommitKnowledge(vault_pb2.VaultEntry(content=content, tags=tags, timestamp=time.time()))
        except: logger.error("Vault sync failed.")

    def _reason_with_dual_brain(self, cmd):
        try:
            l = self.vault_light.QueryKnowledge(vault_pb2.VaultQuery(search_vector=cmd))
            s = self.vault_shadow.QueryKnowledge(vault_pb2.VaultQuery(search_vector=cmd))
            return f"[Symmetric Brain]: L:{len(l.entries)} S:{len(s.entries)} intelligence vectors found."
        except: return "[Core]: Synchronizing isolated brains..."

    # --- Organization & Multi-Tenancy ---
    def ManageOrganization(self, req, ctx):
        if req.admin_token not in self.active_admin_tokens: return jarvis_pb2.OrgStatus(success=False)
        org_id = req.org_id
        if org_id not in self.org_db: self.org_db[org_id] = {"users": {}}
        if req.action == "ADD": self.org_db[org_id]["users"][req.target_user_id] = {"role": "USER"}
        elif req.action == "REMOVE": self.org_db[org_id]["users"].pop(req.target_user_id, None)
        self._save_json(self.org_file, self.org_db)
        return jarvis_pb2.OrgStatus(success=True)

    def ListUsers(self, req, ctx):
        if req.admin_token not in self.active_admin_tokens: return jarvis_pb2.UserList()
        org = self.org_db.get(req.org_id, {"users": {}})
        users = [jarvis_pb2.UserInfo(user_id=u, role=d["role"], balance=self.usage_db.get(u, {}).get("balance", 0.0)) for u, d in org["users"].items()]
        return jarvis_pb2.UserList(users=users)

    # --- Financial & Compute ---
    def VerifyPioneer(self, req, ctx):
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        p = loop.run_until_complete(self.pi_synergy.verify_pioneer(req.access_token))
        if p: return jarvis_pb2.PiAuthResponse(success=True, username=p['username'], uid=p['uid'])
        return jarvis_pb2.PiAuthResponse(success=False)

    def ProcessPayment(self, req, ctx):
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        return jarvis_pb2.PiPaymentResponse(success=loop.run_until_complete(self.pi_synergy.process_pi_payment(req.payment_id, req.txid)))

    def GetUsageStats(self, req, ctx):
        s = self.usage_db.get(req.client_id, {"balance": 100.0, "total": 0})
        return jarvis_pb2.UsageResponse(current_balance=s["balance"], requests_processed=s.get("total", 0), pi_equivalent=max(0, (100-s["balance"])*0.01))

    def RefillCredits(self, req, ctx):
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        if loop.run_until_complete(self.pi_synergy.process_pi_payment(req.payment_id, req.txid)):
            if req.client_id not in self.usage_db: self.usage_db[req.client_id] = {"balance": 0.0}
            self.usage_db[req.client_id]["balance"] = 100.0
            self._save_json(self.usage_file, self.usage_db)
            return jarvis_pb2.RefillResponse(success=True, new_balance=100.0)
        return jarvis_pb2.RefillResponse(success=False)

    def ReportCompute(self, req, ctx):
        if req.client_id not in self.usage_db: self.usage_db[req.client_id] = {"balance": 100.0, "total": 0, "compute": 0, "pi_earned": 0}
        self.usage_db[req.client_id]["compute"] += req.cpu_cycles_contributed
        self.usage_db[req.client_id]["pi_earned"] += (req.cpu_cycles_contributed * 0.0001)
        self._save_json(self.usage_file, self.usage_db)
        return jarvis_pb2.ComputeStatus(success=True, credits_earned=req.cpu_cycles_contributed * 0.0001)

    def GetRewardStats(self, req, ctx):
        s = self.usage_db.get(req.client_id, {"compute": 0, "pi_earned": 0})
        return jarvis_pb2.RewardResponse(total_compute_contributed=s["compute"], lifetime_pi_earned=s["pi_earned"], pending_pi_payout=s["pi_earned"])

    def _meter_usage(self, cid):
        if cid not in self.usage_db: self.usage_db[cid] = {"balance": 100.0, "total": 0, "compute": 0, "pi_earned": 0}
        self.usage_db[cid]["balance"] -= 1.0
        self.usage_db[cid]["total"] += 1
        self._save_json(self.usage_file, self.usage_db)

# --- Background Cycle ---
def start_intelligence_cycles(servicer):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    s = [WebIntelligenceScraper(servicer), OmniIntelligenceScraper(servicer), PiIntelligenceScraper(servicer), AIPeerLearning(servicer)]
    for x in s:
        if hasattr(x, 'run_autonomous_cycle'): loop.create_task(x.run_autonomous_cycle())
        if hasattr(x, 'run_omni_cycle'): loop.create_task(x.run_omni_cycle())
        if hasattr(x, 'run_pi_cycle'): loop.create_task(x.run_pi_cycle())
        if hasattr(x, 'run_peer_learning_cycle'): loop.create_task(x.run_peer_learning_cycle())
    loop.run_forever()

def serve():
    try:
        with open('certs/ca.crt', 'rb') as f: rc = f.read()
        with open('certs/server.key', 'rb') as f: pk = f.read()
        with open('certs/server.crt', 'rb') as f: cc = f.read()
        creds = grpc.ssl_server_credentials([(pk, cc)], root_certificates=rc, require_client_auth=True)
        servicer = JarvisServicer()
        threading.Thread(target=start_intelligence_cycles, args=(servicer,), daemon=True).start()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=50))
        jarvis_pb2_grpc.add_JarvisServiceServicer_to_server(servicer, server)
        port = os.getenv('GRPC_PORT', '50051')
        server.add_secure_port(f'[::]:{port}', creds)
        server.start()
        logger.info(f"JarvisAI Supreme Core ONLINE on port {port}")
        server.wait_for_termination()
    except Exception as e: logger.critical(f"CORE FAILURE: {str(e)}")

if __name__ == '__main__':
    serve()
