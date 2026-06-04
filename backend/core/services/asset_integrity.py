import hashlib
import os
import logging

class AssetIntegrity:
    """
    Asset Integrity.
    MANDATE: Ensure high-fidelity persistence of all Sovereign assets.
    """
    def __init__(self):
        self.verified_hashes = {}

    def audit_storage_nodes(self, node_list):
        """Audits a list of storage nodes for data consistency and integrity."""
        logging.info("[ASSET-INTEGRITY]: Starting storage node audit...")
        results = {}
        for node in node_list:
            if os.path.exists(node):
                file_hash = self._calculate_sha256(node)
                results[node] = {
                    "exists": True,
                    "hash": file_hash,
                    "verified": self._verify_against_registry(node, file_hash)
                }
            else:
                results[node] = {"exists": False, "verified": False}
        return results

    def _calculate_sha256(self, file_path):
        """Calculates the SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _verify_against_registry(self, node, current_hash):
        """Verifies the current hash against the sovereign integrity registry."""
        # Simple local registry simulation
        if node not in self.verified_hashes:
            self.verified_hashes[node] = current_hash
            return True
        return self.verified_hashes[node] == current_hash

    def register_asset(self, path):
        """Adds a new asset to the integrity registry."""
        if os.path.exists(path):
            self.verified_hashes[path] = self._calculate_sha256(path)
            logging.info(f"[ASSET-INTEGRITY]: Registered asset: {path}")
