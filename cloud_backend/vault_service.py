import grpc
from concurrent import futures
import vault_pb2
import vault_pb2_grpc
import os
import json
import logging
from cryptography.fernet import Fernet

# Brain Vault Service: Provides encrypted isolation for knowledge
class BrainVaultServicer(vault_pb2_grpc.BrainVaultServicer):
    def __init__(self, vault_type):
        self.vault_type = vault_type
        self.storage_path = f"/vault/data/{vault_type.lower()}_brain.enc"
        # Master Key - In production, this comes from KMS/HSM
        self.key = os.getenv("VAULT_MASTER_KEY", Fernet.generate_key().decode())
        self.cipher = Fernet(self.key.encode())
        self.memory_db = self._unlock_vault()
        logging.info(f"Vault {vault_type} initialized and encrypted at rest.")

    def _unlock_vault(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "rb") as f:
                encrypted_data = f.read()
                return json.loads(self.cipher.decrypt(encrypted_data).decode())
        return []

    def _lock_vault(self):
        encrypted_data = self.cipher.encrypt(json.dumps(self.memory_db).encode())
        with open(self.storage_path, "wb") as f:
            f.write(encrypted_data)

    def QueryKnowledge(self, request, context):
        # Basic vector/tag match simulation
        matches = [e for e in self.memory_db if request.search_vector.lower() in e['content'].lower()]
        response = vault_pb2.VaultResponse()
        for m in matches:
            response.entries.add(content=m['content'], tags=m['tags'], timestamp=m['timestamp'])
        return response

    def CommitKnowledge(self, request, context):
        entry = {
            "content": request.content,
            "tags": request.tags,
            "timestamp": request.timestamp
        }
        self.memory_db.append(entry)
        self._lock_vault()
        return vault_pb2.VaultStatus(success=True, vault_id=self.vault_type)

def serve():
    vault_type = os.getenv("VAULT_TYPE", "LIGHT")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    vault_pb2_grpc.add_BrainVaultServicer_to_server(BrainVaultServicer(vault_type), server)
    
    # Internal gRPC on isolated network
    port = os.getenv("VAULT_PORT", "50060")
    server.add_insecure_port(f'[::]:{port}') # mTLS added in deployment layer
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
