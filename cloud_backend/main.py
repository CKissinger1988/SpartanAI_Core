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

# Master Admin Key
MASTER_ADMIN_KEY = os.getenv("MASTER_ADMIN_KEY", "nexus_master_override_2026")

class JarvisServicer(jarvis_pb2_grpc.JarvisServiceServicer):
    def __init__(self):
        self.active_admin_tokens = set()
        self.evolution_dir = "evolution"
        self.knowledge_dir = "knowledge"
        os.makedirs(self.evolution_dir, exist_ok=True)
        os.makedirs(self.knowledge_dir, exist_ok=True)
        self.light_brain = self._load_knowledge("LIGHT")
        self.shadow_brain = self._load_knowledge("SHADOW")

    def StreamOperator(self, request_iterator, context):
        for request in request_iterator:
            metadata = dict(context.invocation_metadata())
            is_admin = metadata.get('admin-token') in self.active_admin_tokens
            reasoning = self._reason_with_dual_brain(request.command)
            yield jarvis_pb2.JarvisResponse(
                message=f"{reasoning}\n[Jarvis]: Central Intelligence active.",
                action_type="REPLY",
                payload="Omni-Intelligence Core Online"
            )

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

    def _internal_store_knowledge(self, side, content, tags):
        target_brain = self.light_brain if side == "LIGHT" else self.shadow_brain
        target_brain.append({"content": content, "tags": tags, "timestamp": time.time()})
        self._save_knowledge(side, target_brain)

    def _reason_with_dual_brain(self, command):
        # Deep Synthesis reasoning logic
        light_matches = [k for k in self.light_brain if any(t in command for t in k['tags'].split(','))]
        shadow_matches = [k for k in self.shadow_brain if any(t in command for t in k['tags'].split(','))]
        output = "[Omni-Reasoning]: "
        if light_matches: output += f"Global logic paths found ({len(light_matches)}). "
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
    threat_scraper = WebIntelligenceScraper(servicer)
    omni_scraper = OmniIntelligenceScraper(servicer)
    peer_learning = AIPeerLearning(servicer)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Parallelize all intelligence streams
    loop.create_task(threat_scraper.run_autonomous_cycle())
    loop.create_task(omni_scraper.run_omni_cycle())
    loop.create_task(peer_learning.run_peer_learning_cycle())
    
    loop.run_forever()

def serve():
    with open('certs/ca.crt', 'rb') as f: root_certs = f.read()
    with open('certs/server.key', 'rb') as f: private_key = f.read()
    with open('certs/server.crt', 'rb') as f: certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials([(private_key, certificate_chain)], root_certificates=root_certs, require_client_auth=True)
    
    servicer = JarvisServicer()
    
    # Start Universal Intelligence Ingestion in background
    scraper_thread = threading.Thread(target=run_scrapers, args=(servicer,), daemon=True)
    scraper_thread.start()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jarvis_pb2_grpc.add_JarvisServiceServicer_to_server(servicer, server)
    server.add_secure_port('[::]:50051', server_credentials)
    server.start()
    print("JarvisAI Omni-Intelligence Central Core Active...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
