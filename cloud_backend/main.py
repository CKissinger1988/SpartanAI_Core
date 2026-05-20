import grpc
from concurrent import futures
import jarvis_pb2
import jarvis_pb2_grpc
import time
import os
import uuid
import json

# Master Admin Key
MASTER_ADMIN_KEY = os.getenv("MASTER_ADMIN_KEY", "nexus_master_override_2026")

class JarvisServicer(jarvis_pb2_grpc.JarvisServiceServicer):
    def __init__(self):
        self.active_admin_tokens = set()
        self.evolution_dir = "evolution"
        self.knowledge_dir = "knowledge"
        os.makedirs(self.evolution_dir, exist_ok=True)
        os.makedirs(self.knowledge_dir, exist_ok=True)
        
        # Initialize Dual Brain Databases
        self.light_brain = self._load_knowledge("LIGHT")
        self.shadow_brain = self._load_knowledge("SHADOW")

    def StreamOperator(self, request_iterator, context):
        for request in request_iterator:
            metadata = dict(context.invocation_metadata())
            is_admin = metadata.get('admin-token') in self.active_admin_tokens
            
            role_label = "[MASTER ADMIN]" if is_admin else "[USER]"
            print(f"[{time.time()}] {role_label} Secure request from {request.client_id}: {request.command}")
            
            # Deep Reasoning: Contrast Light vs Shadow
            reasoning = self._reason_with_dual_brain(request.command)
            msg = f"{reasoning}\n[Jarvis]: Command securely processed."
            
            yield jarvis_pb2.JarvisResponse(
                message=msg,
                action_type="REPLY",
                payload="Symmetric Core Online"
            )

    def ElevatePrivileges(self, request, context):
        if request.master_key == MASTER_ADMIN_KEY:
            token = str(uuid.uuid4())
            self.active_admin_tokens.add(token)
            return jarvis_pb2.ElevationResponse(success=True, message="Master Admin granted.", admin_token=token)
        return jarvis_pb2.ElevationResponse(success=False, message="Access denied.", admin_token="")

    def SelfEvolve(self, request, context):
        if request.admin_token not in self.active_admin_tokens:
            return jarvis_pb2.EvolutionStatus(success=False, logs="Unauthorized.")
        try:
            filepath = os.path.join(self.evolution_dir, f"{request.target_module}_logic.py")
            with open(filepath, "w") as f: f.write(request.logic_snippet)
            exec(request.logic_snippet, globals())
            return jarvis_pb2.EvolutionStatus(success=True, logs="Core evolution reloaded.")
        except Exception as e:
            return jarvis_pb2.EvolutionStatus(success=False, logs=str(e))

    def StoreKnowledge(self, request, context):
        if request.admin_token not in self.active_admin_tokens:
            return jarvis_pb2.KnowledgeStatus(success=False, message="Unauthorized.")
        
        target_brain = self.light_brain if request.side == "LIGHT" else self.shadow_brain
        target_brain.append({"content": request.content, "tags": request.tags, "timestamp": time.time()})
        
        self._save_knowledge(request.side, target_brain)
        print(f"[{time.time()}] [KNOWLEDGE] Integrated new intelligence into {request.side} core.")
        return jarvis_pb2.KnowledgeStatus(success=True, message=f"Knowledge integrated into {request.side} brain.")

    def _reason_with_dual_brain(self, command):
        # SIMULATED DEEP REASONING
        # In a real implementation, this would use embeddings/vector search to find matches
        light_matches = [k for k in self.light_brain if any(t in command for t in k['tags'].split(','))]
        shadow_matches = [k for k in self.shadow_brain if any(t in command for t in k['tags'].split(','))]
        
        output = "[Reasoning Core]: "
        if light_matches: output += f"Positive protocols found ({len(light_matches)}). "
        if shadow_matches: output += f"Adversarial vectors identified ({len(shadow_matches)}). "
        if not light_matches and not shadow_matches: output += "Neutral context established. "
        
        return output

    def _load_knowledge(self, side):
        path = os.path.join(self.knowledge_dir, f"{side.lower()}_knowledge.json")
        if os.path.exists(path):
            with open(path, "r") as f: return json.load(f)
        return []

    def _save_knowledge(self, side, data):
        path = os.path.join(self.knowledge_dir, f"{side.lower()}_knowledge.json")
        with open(path, "w") as f: json.dump(data, f, indent=4)

def serve():
    with open('certs/ca.crt', 'rb') as f: root_certs = f.read()
    with open('certs/server.key', 'rb') as f: private_key = f.read()
    with open('certs/server.crt', 'rb') as f: certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials([(private_key, certificate_chain)], root_certificates=root_certs, require_client_auth=True)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jarvis_pb2_grpc.add_JarvisServiceServicer_to_server(JarvisServicer(), server)
    server.add_secure_port('[::]:50051', server_credentials)
    server.start()
    print("JarvisAI Dual-Brain Symmetric Backend running...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
