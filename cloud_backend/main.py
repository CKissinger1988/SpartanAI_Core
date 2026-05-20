import grpc
from concurrent import futures
import jarvis_pb2
import jarvis_pb2_grpc
import time
import os
import uuid
import importlib.util
import sys

# Master Admin Key
MASTER_ADMIN_KEY = os.getenv("MASTER_ADMIN_KEY", "nexus_master_override_2026")

class JarvisServicer(jarvis_pb2_grpc.JarvisServiceServicer):
    def __init__(self):
        self.active_admin_tokens = set()
        self.evolution_dir = "evolution"
        os.makedirs(self.evolution_dir, exist_ok=True)

    def StreamOperator(self, request_iterator, context):
        for request in request_iterator:
            metadata = dict(context.invocation_metadata())
            is_admin = metadata.get('admin-token') in self.active_admin_tokens
            
            role_label = "[MASTER ADMIN]" if is_admin else "[USER]"
            print(f"[{time.time()}] {role_label} Secure request from {request.client_id}: {request.command}")
            
            # Execute command (including potential dynamic logic)
            msg = self._execute_adaptive_logic(request.command, is_admin)
            
            yield jarvis_pb2.JarvisResponse(
                message=msg,
                action_type="REPLY",
                payload="Adaptive Core Active"
            )

    def ElevatePrivileges(self, request, context):
        if request.master_key == MASTER_ADMIN_KEY:
            token = str(uuid.uuid4())
            self.active_admin_tokens.add(token)
            return jarvis_pb2.ElevationResponse(success=True, message="Master Admin granted.", admin_token=token)
        return jarvis_pb2.ElevationResponse(success=False, message="Access denied.", admin_token="")

    def SelfEvolve(self, request, context):
        if request.admin_token not in self.active_admin_tokens:
            return jarvis_pb2.EvolutionStatus(success=False, logs="Unauthorized: Master Admin authority required.")

        try:
            # Persist and integrate new logic
            filename = f"{request.target_module}_logic.py"
            filepath = os.path.join(self.evolution_dir, filename)
            
            with open(filepath, "w") as f:
                f.write(request.logic_snippet)
            
            # Hot-reload check (verification execution)
            exec(request.logic_snippet, globals())
            
            print(f"[{time.time()}] [EVOLUTION] Core module '{request.target_module}' recoded successfully.")
            return jarvis_pb2.EvolutionStatus(success=True, logs=f"Module '{request.target_module}' updated and reloaded.")
        except Exception as e:
            return jarvis_pb2.EvolutionStatus(success=False, logs=str(e))

    def _execute_adaptive_logic(self, command, is_admin):
        # Placeholder for dynamic logic selection
        return "Securely processed by Adaptive Cloud Jarvis"

def serve():
    with open('certs/ca.crt', 'rb') as f: root_certs = f.read()
    with open('certs/server.key', 'rb') as f: private_key = f.read()
    with open('certs/server.crt', 'rb') as f: certificate_chain = f.read()

    server_credentials = grpc.ssl_server_credentials([(private_key, certificate_chain)], root_certificates=root_certs, require_client_auth=True)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jarvis_pb2_grpc.add_JarvisServiceServicer_to_server(JarvisServicer(), server)
    
    port = os.getenv('GRPC_PORT', '50051')
    server.add_secure_port(f'[::]:{port}', server_credentials)
    server.start()
    print(f"JarvisAI gRPC Adaptive Backend running on port {port}...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
