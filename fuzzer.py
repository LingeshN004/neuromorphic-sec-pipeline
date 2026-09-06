import socket
import json
import time
from engine import sign_packet

HOST = "127.0.0.1"
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2.0)

# Deliberate cyber-physical attack payloads
attacks = [
    ("Attack 1: Negative FDI Injection", {"left": -5.0, "front": 10.0, "right": 10.0}, False),
    ("Attack 2: Out-of-bounds Extreme Sensor", {"left": 10.0, "front": 99.0, "right": 10.0}, False),
    ("Attack 3: MITM Signature Forgery", {"left": 2.0, "front": 2.0, "right": 2.0}, "forged_bad_sig"),
    ("Attack 4: Nan/Corrupt Float Injection", {"left": float("nan"), "front": 10.0, "right": 10.0}, False),
]

print("=" * 65)
print("[!] LAUNCHING ADVERSARIAL FUZZER AGAINST ENGINE PORT 5005")
print("=" * 65)

for name, payload, tamper_sig in attacks:
    if tamper_sig:
        packet = {"data": payload, "signature": tamper_sig}
    else:
        # Legitimate HMAC but malicious data
        packet = sign_packet(payload)
        
    sock.sendto(json.dumps(packet).encode("utf-8"), (HOST, PORT))
    
    try:
        reply_bytes, _ = sock.recvfrom(4096)
        reply = json.loads(reply_bytes.decode("utf-8"))
        print(f"[*] {name:38} | Result: {reply['status']:7} | Safe Hover: Thrust={reply['thrust']}")
    except socket.timeout:
        print(f"[!] {name:38} | Dropped silently")
        
    time.sleep(0.3)

sock.close()
print("=" * 65)
print("[*] Fuzzing complete.")