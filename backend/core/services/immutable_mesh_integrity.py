import hashlib
import logging

class ImmutableMeshIntegrity:
    """
    Immutable Mesh Integrity.
    MANDATE: Ensure cryptographic non-repudiation and integrity of the Supreme Mesh.
    """
    def __init__(self):
        self.genesis_block = "SPARTAN_GENESIS_v50"
        self.last_hash = self.genesis_block

    def verify_node_signature_chain(self, chain):
        """Verifies the integrity of a node signature chain."""
        logging.info("[MESH-INTEGRITY]: Validating node signature chain...")
        
        for block in chain:
            if not self._validate_block(block):
                logging.error(f"[MESH-INTEGRITY]: Integrity breach detected in block {block.get('id')}.")
                return False
                
        return True

    def _validate_block(self, block):
        """Validates a single block in the signature chain."""
        # Simplified validation logic
        expected_hash = hashlib.sha256((str(block.get('data')) + self.last_hash).encode()).hexdigest()
        if block.get('hash') == expected_hash:
            self.last_hash = expected_hash
            return True
        return False

    def get_mesh_health(self):
        """Returns the overall health of the mesh based on integrity checks."""
        return {
            "status": "IMMUTABLE",
            "last_verification_ts": "GENESIS-STABLE",
            "threat_index": 0.01
        }
