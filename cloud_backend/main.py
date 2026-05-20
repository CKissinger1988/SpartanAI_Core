import grpc
from concurrent import futures
import jarvis_pb2
import jarvis_pb2_grpc
import time
import os
import uuid

# Master Admin Key - Should be stored in a secure secret manager
MASTER_ADMIN_KEY = os.getenv("MASTER_ADMIN_KEY", "nexus_master_override_2026")

class JarvisServicer(jarvis_pb2_grpc.JarvisServiceServicer):
    def __init__(self):
        self.active_admin_tokens = set()

    def StreamOperator(self, request_iterator, context):
        for request in request_iterator:
            # Check if client has admin context (e.g. from metadata)
            metadata = dict(context.invocation_metadata())
            is_admin = metadata.get('admin-token') in self.active_admin_tokens
            
            role_label = "[MASTER ADMIN]" if is_admin else "[USER]"
            print(f"[{time.time()}] {role_label} Secure request from {request.client_id}: {request.command}")
            
            msg = "Securely processed by Cloud Jarvis"
            if is_admin:
                msg = "Master Admin access granted. Full control panel available."
            
            yield jarvis_pb2.JarvisResponse(
                message=msg,
                action_type="REPLY",
                payload="mTLS Verified"
            )

    def ElevatePrivileges(self, request, context):
        if request.master_key == MASTER_ADMIN_KEY:
            token = str(uuid.uuid4())
            self.active_admin_tokens.add(token)
            print(f"[{time.time()}] Privilege elevation SUCCESS for client: {request.client_id}")
            return jarvis_pb2.ElevationResponse(
                success=True,
                message="Master Admin access granted.",
                admin_token=token
            )
        else:
            print(f"[{time.time()}] Privilege elevation FAILED for client: {request.client_id}")
            return jarvis_pb2.ElevationResponse(
                success=False,
                message="Access denied. Invalid master key.",
                admin_token=""
            )

def serve():
    # Load CNSA-compliant certificates
    with open('certs/ca.crt', 'rb') as f:
        root_certs = f.read()
    with open('certs/server.key', 'rb') as f:
        private_key = f.read()
    with open('certs/server.crt', 'rb') as f:
        certificate_chain = f.read()

    server_credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)],
        root_certificates=root_certs,
        require_client_auth=True
    )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jarvis_pb2_grpc.add_JarvisServiceServicer_to_server(JarvisServicer(), server)
    
    port = os.getenv('GRPC_PORT', '50051')
    server.add_secure_port(f'[::]:{port}', server_credentials)
    server.start()
    print(f"JarvisAI gRPC Backend SECURELY running on port {port}...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
