# generate_certs.ps1 - Generates mTLS Certificates for JarvisAI
mkdir -p certs
cd certs

# 1. Create CA
openssl genrsa -out ca.key 4096
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt -subj "/CN=JarvisRootCA"

# 2. Create Server Cert
openssl genrsa -out server.key 4096
openssl req -new -key server.key -out server.csr -subj "/CN=jarvis-backend"
openssl x509 -req -days 3650 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt

# 3. Create Client Cert
openssl genrsa -out client.key 4096
openssl req -new -key client.key -out client.csr -subj "/CN=jarvis-operator"
openssl x509 -req -days 3650 -in client.csr -CA ca.crt -CAkey ca.key -set_serial 02 -out client.crt
