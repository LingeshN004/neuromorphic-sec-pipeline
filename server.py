import socket
import json
from engine import FlySecurityEngine, sign_packet

# Initialize the bio-security engine
engine = FlySecurityEngine()

# Configure network socket (UDP localhost)
HOST = "127.0.0.1"  # Local machine only
PORT = 5005         # Port to listen for Minecraft/bot data

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print("=" * 65)
print(f"[*] Connectome Telemetry Bridge running on {HOST}:{PORT}")
print("[*] Waiting for live sensor packets...")
print("=" * 65)

try:
    while True:
        # 1. Listen for incoming telemetry packets
        raw_data, addr = sock.recvfrom(4096)
        
        try:
            packet = json.loads(raw_data.decode("utf-8"))
        except Exception:
            # Drop malformed non-JSON data
            continue

        # 2. Run data through the Zero-Trust + Connectome brain
        decision = engine.step(packet)

        # 3. Log decision to the console
        status = decision["status"]
        yaw = decision["yaw"]
        thrust = decision["thrust"]
        log_msg = decision["reason"]
        print(f"[{status:8}] Client {addr[1]} | Yaw: {yaw:+6.2f}° | Thrust: {thrust:.2f} | Info: {log_msg}")

        # 4. Reply with motor commands
        response = {
            "yaw": yaw,
            "thrust": thrust,
            "status": status
        }
        sock.sendto(json.dumps(response).encode("utf-8"), addr)

except KeyboardInterrupt:
    print("\n[*] Server shutdown cleanly.")
    sock.close()