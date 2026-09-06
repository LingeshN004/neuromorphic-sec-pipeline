import hmac
import hashlib
import json
import numpy as np

SHARED_SECRET_KEY = b"neurocraft_super_secret_capstone_key_2026"

def generate_signed_packet(payload: dict) -> dict:
    """Simulates an authorized Minecraft agent sending HMAC-signed telemetry."""
    raw_data = json.dumps(payload, sort_keys=True).encode("utf-8")
    signature = hmac.new(SHARED_SECRET_KEY, raw_data, hashlib.sha256).hexdigest()
    return {"data": payload, "signature": signature}

class ZeroTrustInputValidator:
    def __init__(self, max_delta: float = 8.0, min_range: float = 0.0, max_range: float = 32.0):
        self.max_delta = max_delta
        self.min_range = min_range
        self.max_range = max_range
        self.prev_telemetry = None

    def verify_hmac(self, packet: dict) -> bool:
        """Enforces message integrity and origin authenticity."""
        if "data" not in packet or "signature" not in packet:
            return False
        raw_data = json.dumps(packet["data"], sort_keys=True).encode("utf-8")
        expected_sig = hmac.new(SHARED_SECRET_KEY, raw_data, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_sig, packet["signature"])

    def sanitize_and_filter(self, packet: dict):
        """
        Detects FDI (False Data Injection), physics violations, 
        and anomalous sensory jumps.
        """
        # 1. Cryptographic Gateway Verification
        if not self.verify_hmac(packet):
            return None, "[ALERT] HMAC Integrity Check Failed! Packet Dropped (Tampered/Spoofed)"

        sensors = packet["data"]
        sanitized = {}

        # 2. Schema and Numerical Range Sanitization
        for key in ["left", "front", "right"]:
            val = sensors.get(key, None)
            if val is None or np.isnan(val) or np.isinf(val):
                return None, f"[ALERT] Sensor Fault / Anomaly: {key} contains invalid float"
            if val < self.min_range or val > self.max_range:
                return None, f"[ALERT] Out-of-Bounds Injection: {key}={val} violates physical limits"
            sanitized[key] = float(val)

        # 3. Temporal Anomaly & Sensor Spoofing Check (Rate-of-Change Delta)
        if self.prev_telemetry is not None:
            for key in ["left", "front", "right"]:
                delta = abs(sanitized[key] - self.prev_telemetry[key])
                if delta > self.max_delta:
                    return None, f"[ALERT] Physics Violation Delta: {key} shifted by {delta:.1f}m in a single tick"

        self.prev_telemetry = sanitized.copy()
        return sanitized, "[OK] Verified & Sanitized"

# ==================== ATTACK SIMULATION ====================
validator = ZeroTrustInputValidator()

test_packets = [
    ("Legitimate Tick 1", generate_signed_packet({"left": 10.0, "front": 10.0, "right": 10.0})),
    ("Legitimate Tick 2", generate_signed_packet({"left": 9.2,  "front": 8.5,  "right": 9.8})),
    ("Attack 1: FDI / Spoofed Distance", generate_signed_packet({"left": -4.5, "front": 8.0,  "right": 10.0})),
    ("Attack 2: Replay / Tampered Packet", {"data": {"left": 2.0, "front": 2.0, "right": 2.0}, "signature": "bad_actor_fake_sig"}),
    ("Attack 3: Teleportation / Rate Jump", generate_signed_packet({"left": 9.2, "front": 0.1,  "right": 9.8})),
]

print("=" * 60)
print("ZERO-TRUST CPS SECURITY GATEWAY TEST SUITE")
print("=" * 60)

for test_name, pkt in test_packets:
    clean_data, log = validator.sanitize_and_filter(pkt)
    status = "[ACCEPTED]" if clean_data else "[BLOCKED] "
    print(f"{status} {test_name:32} -> {log}")

