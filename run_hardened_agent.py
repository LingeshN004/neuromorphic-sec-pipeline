import hmac
import hashlib
import json
import numpy as np
import pandas as pd

SHARED_SECRET_KEY = b"neurocraft_super_secret_capstone_key_2026"

def generate_signed_packet(payload: dict) -> dict:
    raw_data = json.dumps(payload, sort_keys=True).encode("utf-8")
    signature = hmac.new(SHARED_SECRET_KEY, raw_data, hashlib.sha256).hexdigest()
    return {"data": payload, "signature": signature}

class HardenedConnectomeAgent:
    def __init__(self, annot_path="fly_annotations.csv", max_delta=12.0):
        self.max_delta = max_delta
        self.prev_telemetry = None
        
        print("[*] Booting Hardened Drosophila Connectome Agent...")
        annot_df = pd.read_csv(annot_path, compression="gzip", low_memory=False)
        descending = annot_df[annot_df["super_class"] == "descending"]
        
        self.left_dns = set(descending[descending["side"] == "left"]["root_id"])
        self.right_dns = set(descending[descending["side"] == "right"]["root_id"])
        print(f"[+] Loaded {len(self.left_dns)} Left & {len(self.right_dns)} Right Descending Flight Neurons.")

    def verify_and_sanitize(self, packet: dict):
        # 1. Cryptographic Authentication
        if "data" not in packet or "signature" not in packet:
            return None, "Malformed packet structure"
        
        raw_data = json.dumps(packet["data"], sort_keys=True).encode("utf-8")
        expected_sig = hmac.new(SHARED_SECRET_KEY, raw_data, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_sig, packet["signature"]):
            return None, "HMAC signature mismatch (Tampered/Spoofed)"

        # 2. Physics & Range Sanitization
        sensors = packet["data"]
        sanitized = {}
        for k in ["left", "front", "right"]:
            val = sensors.get(k)
            if val is None or np.isnan(val) or np.isinf(val):
                return None, f"Invalid float in channel '{k}'"
            if val < 0.0 or val > 32.0:
                return None, f"Out-of-bounds sensor injection: {k}={val}"
            sanitized[k] = float(val)

        # 3. Dynamic Temporal Delta Check
        if self.prev_telemetry is not None:
            for k in ["left", "front", "right"]:
                delta = abs(sanitized[k] - self.prev_telemetry[k])
                if delta > self.max_delta:
                    return None, f"Physics violation: {k} rate jump delta={delta:.1f}m"

        self.prev_telemetry = sanitized.copy()
        return sanitized, "OK"

    def compute_motor_response(self, sensors: dict):
        threat_l = np.clip(1.0 / (sensors["left"] + 1e-3), 0.0, 1.0)
        threat_f = np.clip(1.0 / (sensors["front"] + 1e-3), 0.0, 1.0)
        threat_r = np.clip(1.0 / (sensors["right"] + 1e-3), 0.0, 1.0)
        
        # Neuromorphic asymmetric flight steering
        rate_left = 0.5 + (0.5 * threat_r) - (0.4 * threat_l)
        rate_right = 0.5 + (0.5 * threat_l) - (0.4 * threat_r)
        
        yaw = float((rate_right - rate_left) * 45.0)
        thrust = float(np.clip(1.0 - (0.8 * threat_f), 0.1, 1.0))
        return yaw, thrust

    def process_tick(self, packet: dict):
        clean_sensors, status = self.verify_and_sanitize(packet)
        if clean_sensors is None:
            # Defensive Hover State: Neutral steering, minimum survival thrust
            return {"status": "BLOCKED", "reason": status, "yaw": 0.0, "thrust": 0.05}
        
        yaw, thrust = self.compute_motor_response(clean_sensors)
        return {"status": "ACCEPTED", "reason": status, "yaw": yaw, "thrust": thrust}

# ==================== LIVE SIMULATION SEQUENCE ====================
agent = HardenedConnectomeAgent(max_delta=12.0)

telemetry_stream = [
    ("Tick 1: Clear Corridor",       generate_signed_packet({"left": 10.0, "front": 10.0, "right": 10.0})),
    ("Tick 2: Obstacle Nearing Right",generate_signed_packet({"left": 9.5,  "front": 8.0,  "right": 2.5})),
    ("Tick 3: Hard Right Evasion",   generate_signed_packet({"left": 9.0,  "front": 6.5,  "right": 0.6})),
    ("Attack A: FDI Negative Distance",generate_signed_packet({"left": 9.0,  "front": -5.0, "right": 0.6})),
    ("Attack B: Tampered Packet MITM", {"data": {"left": 5.0, "front": 5.0, "right": 5.0}, "signature": "evil_injected_hash"}),
    ("Attack C: Teleport/Sensor Spoof",generate_signed_packet({"left": 9.0, "front": 30.0, "right": 0.6})),
    ("Tick 4: Left Clearance Wall",   generate_signed_packet({"left": 0.8,  "front": 7.0,  "right": 9.0})),
]

print("\n" + "=" * 80)
print("EXECUTING HARDENED BIOCPS SENSORY-MOTOR EXECUTION")
print("=" * 80)

for label, pkt in telemetry_stream:
    decision = agent.process_tick(pkt)
    tag = decision["status"]
    print(f"[{tag:8}] {label:32} | Yaw: {decision['yaw']:+6.2f}°/t | Thrust: {decision['thrust']:.2f} | Log: {decision['reason']}")

