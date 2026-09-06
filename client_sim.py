import socket
import json
import time
from engine import sign_packet

HOST = "127.0.0.1"
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2.0)

# Sequence of simulated game ticks
simulated_frames = [
    {"left": 10.0, "front": 15.0, "right": 10.0},  # Clear corridor
    {"left": 1.5,  "front": 12.0, "right": 8.0},   # Left obstacle closing in
    {"left": 0.8,  "front": 5.0,  "right": 9.0},   # Acute left threat + front block
    {"left": 12.0, "front": 14.0, "right": 1.2},   # Right obstacle
]

print("[*] Starting simulated client telemetry stream...")

for i, raw_sensors in enumerate(simulated_frames, 1):
    packet = sign_packet(raw_sensors)
    payload = json.dumps(packet).encode("utf-8")
    
    sock.sendto(payload, (HOST, PORT))
    
    try:
        reply_bytes, _ = sock.recvfrom(4096)
        reply = json.loads(reply_bytes.decode("utf-8"))
        print(f"Tick {i} Sent: {raw_sensors} | Received: Status={reply['status']}, Yaw={reply['yaw']:+.2f}°, Thrust={reply['thrust']:.2f}")
    except socket.timeout:
        print(f"Tick {i} Error: Timed out waiting for server response")
        
    time.sleep(0.5)

sock.close()
print("[*] Stream complete.")