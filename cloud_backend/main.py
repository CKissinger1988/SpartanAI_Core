import grpc
from concurrent import futures
import jarvis_pb2
import jarvis_pb2_grpc
import time
import os

class JarvisServicer(jarvis_pb2_grpc.JarvisServiceServicer):
    def StreamOperator(self, request_iterator, context):
        for request in request_iterator:
            print(f"[{time.time()}] Secure request from {request.client_id}: {request.command}")
            yield jarvis_pb2.JarvisResponse(
                message="Securely processed by Cloud Jarvis",
                action_type="REPLY",
                payload="mTLS Verified"
            )

def serve():
    # Load CNSA-compliant certificates
    with open('certs/ca.crt', 'rb') as f:
        root_certs = f.read()
    with open('certs/server.key', 'rb') as f:
        private_key = f.read()
    with open('certs/server.crt', 'rb') as f:
        certificate_chain = f.read()

    # Create mTLS credentials
    server_credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)],
        root_certificates=root_certs,
        require_client_auth=True # ENFORCE MUTUAL TLS
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
