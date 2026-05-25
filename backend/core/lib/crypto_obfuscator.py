import base64
def obfuscate_c2_traffic(data):
    # Cycle 5: Multi-layer C2 traffic obfuscation
    return base64.b64encode(data.encode()).decode()
