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
        self.org_db = self._load_json(self.org_file, {"master_org": {"users": {}, "admins": ["windows-pc-01"]}})
        
        self.pi_synergy = PiNetworkIntegration(self)
        
        self.vault_light_channel = grpc.insecure_channel(os.getenv('VAULT_LIGHT_URL', 'brain-vault-light:50060'))
        self.vault_shadow_channel = grpc.insecure_channel(os.getenv('VAULT_SHADOW_URL', 'brain-vault-shadow:50061'))
        self.vault_light = vault_pb2_grpc.BrainVaultStub(self.vault_light_channel)
        self.vault_shadow = vault_pb2_grpc.BrainVaultStub(self.vault_shadow_channel)

    def _load_json(self, path, default):
        if os.path.exists(path):
            with open(path, "r") as f: return json.load(f)
        return default

    def _save_json(self, path, data):
        with open(path, "w") as f: json.dump(data, f, indent=4)

    # --- Organization Management ---
    def ManageOrganization(self, request, context):
        if request.admin_token not in self.active_admin_tokens:
            return jarvis_pb2.OrgStatus(success=False, message="Unauthorized.")
        
        org_id = request.org_id
        if org_id not in self.org_db:
            self.org_db[org_id] = {"users": {}, "admins": []}
            
        if request.action == "ADD":
            self.org_db[org_id]["users"][request.target_user_id] = {"role": "USER", "joined": time.time()}
        elif request.action == "REMOVE":
            self.org_db[org_id]["users"].pop(request.target_user_id, None)
            if request.target_user_id in self.org_db[org_id]["admins"]:
                self.org_db[org_id]["admins"].remove(request.target_user_id)
        elif request.action == "SET_ADMIN":
            if request.target_user_id in self.org_db[org_id]["users"]:
                self.org_db[org_id]["users"][request.target_user_id]["role"] = "ORG_ADMIN"
                if request.target_user_id not in self.org_db[org_id]["admins"]:
                    self.org_db[org_id]["admins"].append(request.target_user_id)

        self._save_json(self.org_file, self.org_db)
        return jarvis_pb2.OrgStatus(success=True, message=f"Action {request.action} completed for {request.target_user_id}")

    def ListUsers(self, request, context):
        if request.admin_token not in self.active_admin_tokens: return jarvis_pb2.UserList()
        
        org = self.org_db.get(request.org_id, {"users": {}})
        user_infos = []
        for uid, data in org["users"].items():
            balance = self.usage_db.get(uid, {}).get("balance", 0.0)
            user_infos.append(jarvis_pb2.UserInfo(user_id=uid, role=data["role"], balance=balance))
        return jarvis_pb2.UserList(users=user_infos)

    # --- Existing Core Streams ---
    def StreamOperator(self, request_iterator, context):
        for request in request_iterator:
            enforce_anti_debug()
            metadata = dict(context.invocation_metadata())
            is_supreme = metadata.get('admin-token') in self.active_admin_tokens
            
            # Meter usage only for non-supreme sessions
            if not is_supreme: self._meter_usage(request.client_id)
            
            if is_supreme:
                msg = "[SUPREME COMMAND]: perfection protocol active."
                action = "SUPREME_EXECUTION"
            else:
                reasoning = self._reason_with_dual_brain(request.command)
                msg = f"{reasoning}\n[Jarvis]: Active."
                action = "REPLY"

            yield jarvis_pb2.JarvisResponse(message=msg, action_type=action, payload="Verified")

    def ElevatePrivileges(self, request, context):
        if request.master_key == MASTER_ADMIN_KEY:
            token = str(uuid.uuid4())
            self.active_admin_tokens.add(token)
            return jarvis_pb2.ElevationResponse(success=True, message="Supreme Command active.", admin_token=token)
        return jarvis_pb2.ElevationResponse(success=False)

    # ... Maintaining all other logic (Search, Compute, Pi, Scrapers) ...
    def GlobalSearch(self, req, ctx):
        r = self._reason_with_dual_brain(req.search_vector)
        return jarvis_pb2.IntelligenceResponse(synthesis=f"Synthesis: {r}")

    def StoreKnowledge(self, req, ctx):
        if req.admin_token not in self.active_admin_tokens: return jarvis_pb2.KnowledgeStatus(success=False)
        stub = self.vault_light if req.side == "LIGHT" else self.vault_shadow
        try: stub.CommitKnowledge(vault_pb2.VaultEntry(content=req.content, tags=req.tags, timestamp=time.time()))
        except: pass
        return jarvis_pb2.KnowledgeStatus(success=True)

    def ReportCompute(self, req, ctx):
        if req.client_id not in self.usage_db: self.usage_db[req.client_id] = {"balance": 100.0, "total_requests": 0, "compute": 0, "pi_earned": 0}
        self.usage_db[req.client_id]["compute"] += req.cpu_cycles_contributed
        self.usage_db[req.client_id]["pi_earned"] += (req.cpu_cycles_contributed * 0.0001)
        self._save_json(self.usage_file, self.usage_db)
        return jarvis_pb2.ComputeStatus(success=True)

    def GetUsageStats(self, req, ctx):
        s = self.usage_db.get(req.client_id, {"balance": 100.0})
        return jarvis_pb2.UsageResponse(current_balance=s["balance"])

    def _reason_with_dual_brain(self, cmd):
        try:
            l = self.vault_light.QueryKnowledge(vault_pb2.VaultQuery(search_vector=cmd))
            s = self.vault_shadow.QueryKnowledge(vault_pb2.VaultQuery(search_vector=cmd))
            return f"[Synthesis]: L:{len(l.entries)} S:{len(s.entries)}"
        except: return "[Error]: Sync failed."

    def _meter_usage(self, cid):
        if cid not in self.usage_db: self.usage_db[cid] = {"balance": 100.0, "total_requests": 0}
        self.usage_db[cid]["balance"] -= 1.0
        self._save_json(self.usage_file, self.usage_db)

def serve():
    with open('certs/ca.crt', 'rb') as f: rc = f.read()
    with open('certs/server.key', 'rb') as f: pk = f.read()
    with open('certs/server.crt', 'rb') as f: cc = f.read()
    creds = grpc.ssl_server_credentials([(pk, cc)], root_certificates=rc, require_client_auth=True)
    servicer = JarvisServicer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=30))
    jarvis_pb2_grpc.add_JarvisServiceServicer_to_server(servicer, server)
    server.add_secure_port('[::]:50051', creds)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
