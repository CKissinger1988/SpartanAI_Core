# Apex-Grade Security Specification for Encrypted Storage

## Core Mandates
- **Cascaded Cryptography**: All stored payloads MUST be encrypted using a cascaded approach: AES-256-GCM followed by ChaCha20-Poly1305.
- **ApexVault Integration**: Key management MUST be routed through the ApexVault HSM.
- **Zero-Trust Enforcement**: No access is granted without explicit, ephemeral, and verified identity (Voice/VAC).

## Collections
- `encrypted_records`: Stores cascaded encrypted data payloads linked to a user.

## Invariants
- `encrypted_records` documents MUST have a `userId` field matching the `request.auth.uid`.
- Users can only read/write their own records after cryptographic verification via ApexVault.

## Hardening Payloads (Security Tests)
- Payload 1: { userId: "other-user", encryptedData: "...", iv: "...", tag: "..." } -> SHOUD BE DENIED
- Payload 2: { userId: "my-user", encryptedData: "...", iv: "...", tag: "..." } -> SHOULD BE ALLOWED

