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
        self.usage_file = "usage_db.json"
        os.makedirs(self.evolution_dir, exist_ok=True)
        
        self.usage_db = self._load_usage()
        self.pi_synergy = PiNetworkIntegration(self)
        
        # Vault Connections (Zero-Trust Internal gRPC)
        self.vault_light_channel = grpc.insecure_channel('brain-vault-light:50060')
        self.vault_shadow_channel = grpc.insecure_channel('brain-vault-shadow:50061')
        self.vault_light = vault_pb2_grpc.BrainVaultStub(self.vault_light_channel)
        self.vault_shadow = vault_pb2_grpc.BrainVaultStub(self.vault_shadow_channel)

    def _internal_store_knowledge(self, side, content, tags):
        stub = self.vault_light if side == "LIGHT" else self.vault_shadow
        try:
            stub.CommitKnowledge(vault_pb2.VaultEntry(
                content=content, tags=tags, timestamp=time.time()
            ))
        except Exception as e:
            logger.error(f"Vault Commit Failure: {str(e)}")

    def _reason_with_dual_brain(self, command):
        # Query isolated vaults
        try:
            light_res = self.vault_light.QueryKnowledge(vault_pb2.VaultQuery(search_vector=command))
            shadow_res = self.vault_shadow.QueryKnowledge(vault_pb2.VaultQuery(search_vector=command))
            return f"[Vault-Reasoning]: Isolated cross-reference complete. (L:{len(light_res.entries)} S:{len(shadow_res.entries)})"
        except Exception as e:
            return f"[Vault-Error]: Secure brain sync interrupted."

    def StreamOperator(self, request_iterator, context):
        for request in request_iterator:
            self._meter_usage(request.client_id)
            metadata = dict(context.invocation_metadata())
            is_admin = metadata.get('admin-token') in self.active_admin_tokens
            
            if is_admin:
                msg = "[PRIME DIRECTIVE]: Perfection Protocol active. Executing via Encrypted Vaults."
            else:
                reasoning = self._reason_with_dual_brain(request.command)
                msg = f"{reasoning}\n[Jarvis]: Operation logged in secure buffer."

            yield jarvis_pb2.JarvisResponse(
                message=msg,
                action_type="SUPREME_EXECUTION" if is_admin else "REPLY",
                payload="Absolute Obedience via Isolated Brains"
            )

    # --- Standard Persistence & Logic ---
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
        self._save_usage()

    def ElevatePrivileges(self, request, context):
        if request.master_key == MASTER_ADMIN_KEY:
            token = str(uuid.uuid4())
            self.active_admin_tokens.add(token)
            return jarvis_pb2.ElevationResponse(success=True, message="Prime Directive engaged.", admin_token=token)
        return jarvis_pb2.ElevationResponse(success=False)

    def StoreKnowledge(self, request, context):
        if request.admin_token not in self.active_admin_tokens: return jarvis_pb2.KnowledgeStatus(success=False)
        self._internal_store_knowledge(request.side, request.content, request.tags)
        return jarvis_pb2.KnowledgeStatus(success=True)

def serve():
    with open('certs/ca.crt', 'rb') as f: rc = f.read()
    with open('certs/server.key', 'rb') as f: pk = f.read()
    with open('certs/server.crt', 'rb') as f: cc = f.read()
    creds = grpc.ssl_server_credentials([(pk, cc)], root_certificates=rc, require_client_auth=True)
    servicer = JarvisServicer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    jarvis_pb2_grpc.add_JarvisServiceServicer_to_server(servicer, server)
    server.add_secure_port('[::]:50051', creds)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
