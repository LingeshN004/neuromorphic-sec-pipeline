import hmac
import hashlib
import json
import numpy as np

# Cryptographic Keys & Baseline Model Checksum
SHARED_SECRET_KEY = b"neurocraft_super_secret_capstone_key_2026"

# Normalized biological synaptic weights derived from FAFB v783
SYNAPSE_WEIGHT_LEFT  = 1260664 / (1260664 + 1306835)  # 0.4910
SYNAPSE_WEIGHT_RIGHT = 1306835 / (1260664 + 1306835)  # 0.5090

def sign_packet(payload: dict) -> dict:
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    sig = hmac.new(SHARED_SECRET_KEY, raw, hashlib.sha256).hexdigest()
    return {"data": payload, "signature": sig}

class FlySecurityEngine:
    def __init__(self, max_delta=10.0, range_bounds=(0.0, 32.0)):
        self.max_delta = max_delta
        self.min_range, self.max_range = range_bounds
        self.prev = None
        self.stats = {"accepted": 0, "blocked": 0}

    def verify_and_sanitize(self, packet: dict):
        if not isinstance(packet, dict) or "data" not in packet or "signature" not in packet:
            return None, "Corrupted packet structure"

        # 1. Cryptographic Gateway Verification (HMAC-SHA256)
        raw = json.dumps(packet["data"], sort_keys=True).encode("utf-8")
        expected = hmac.new(SHARED_SECRET_KEY, raw, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, packet["signature"]):
            return None, "HMAC integrity check failed (Tampered/Spoofed)"

        sensors = packet["data"]
        sanitized = {}

        # 2. Physics & Value Boundary Checks
        for ch in ["left", "front", "right"]:
            val = sensors.get(ch)
            if val is None or np.isnan(val) or np.isinf(val):
                return None, f"Invalid float value in '{ch}'"
            if val < self.min_range or val > self.max_range:
                return None, f"Out-of-bounds sensor injection: {ch}={val}"
            sanitized[ch] = float(val)

        # 3. Dynamic Temporal Delta Check (Rate-of-change)
        if self.prev is not None:
            for ch in ["left", "front", "right"]:
                delta = abs(sanitized[ch] - self.prev[ch])
                if delta > self.max_delta:
                    return None, f"Sensor rate jump delta={delta:.1f}m (Physics anomaly)"

        self.prev = sanitized.copy()
        return sanitized, "OK"

    def compute_neuromorphic_flight(self, sensors: dict):
        """
        Uses empirical synaptic weights to calculate 
        bilateral wingbeat steering differential.
        """
        tl = np.clip(1.0 / (sensors["left"] + 1e-3), 0.0, 1.0)
        tf = np.clip(1.0 / (sensors["front"] + 1e-3), 0.0, 1.0)
        tr = np.clip(1.0 / (sensors["right"] + 1e-3), 0.0, 1.0)

        # Weighting transfer functions using connectome density
        drive_left = (0.5 * tl) * SYNAPSE_WEIGHT_LEFT
        drive_right = (0.5 * tr) * SYNAPSE_WEIGHT_RIGHT

        # Yaw steering response (degrees per simulation tick)
        yaw_rate = float((drive_left - drive_right) * 90.0)
        thrust = float(np.clip(1.0 - (0.85 * tf), 0.08, 1.0))

        return yaw_rate, thrust

    def step(self, packet: dict):
        clean, status = self.verify_and_sanitize(packet)
        if clean is None:
            self.stats["blocked"] += 1
            # Failsafe Hover State
            return {"status": "BLOCKED", "reason": status, "yaw": 0.0, "thrust": 0.05}
        
        self.stats["accepted"] += 1
        yaw, thrust = self.compute_neuromorphic_flight(clean)
        return {"status": "ACCEPTED", "reason": status, "yaw": yaw, "thrust": thrust}

# ==================== AUTOMATED TEST HARNESS ====================
if __name__ == "__main__":
    engine = FlySecurityEngine()

    test_stream = [
        ("T1: Open Corridor", sign_packet({"left": 12.0, "front": 12.0, "right": 12.0})),
        ("T2: Impending Left Wall", sign_packet({"left": 2.1, "front": 9.0, "right": 11.0})),
        ("T3: Acute Left Threat", sign_packet({"left": 0.5, "front": 7.0, "right": 10.5})),
        ("T4: FDI Spoof Injection", sign_packet({"left": -8.0, "front": 7.0, "right": 10.5})),
        ("T5: Man-in-the-Middle Replay", {"data": {"left": 2.0, "front": 2.0, "right": 2.0}, "signature": "spoofed_signature_token"}),
        ("T6: Instant Sensor Teleport", sign_packet({"left": 0.5, "front": 28.0, "right": 10.5})),
        ("T7: Right Barrier Evasion", sign_packet({"left": 9.0, "front": 6.0, "right": 0.8})),
    ]

    print("=" * 82)
    print("DROSOPHILA CONNECTOME ZERO-TRUST ENGINE — EXECUTION LOG")
    print("=" * 82)

    for label, pkt in test_stream:
        res = engine.step(pkt)
        tag = res["status"]
        print(f"[{tag:8}] {label:28} | Yaw: {res['yaw']:+6.2f}°/t | Thrust: {res['thrust']:.2f} | Log: {res['reason']}")

    print("=" * 82)
    print(f"[SUMMARY] Total Accepted: {engine.stats['accepted']} | Total Threats Defeated: {engine.stats['blocked']}")
    print("=" * 82)
