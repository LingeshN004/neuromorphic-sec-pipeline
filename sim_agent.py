import gzip
import pandas as pd
import numpy as np

print("[*] Loading connectome annotations...")
annot_df = pd.read_csv("fly_annotations.csv", compression="gzip", low_memory=False)
descending = annot_df[annot_df["super_class"] == "descending"]

left_dn = set(descending[descending["side"] == "left"]["root_id"])
right_dn = set(descending[descending["side"] == "right"]["root_id"])

print(f"[+] Loaded Descending Motor Neurons: {len(left_dn)} Left | {len(right_dn)} Right")

print("[*] Inspecting synaptic connection edges...")
# Read first 5 rows to verify edge structure
edges_sample = pd.read_csv("fly_connections.csv.gz", compression="gzip", nrows=5)
print("[+] Edge Table Columns:", edges_sample.columns.tolist())
print(edges_sample.head(3).to_string(index=False))

def bio_flight_controller(dist_left: float, dist_front: float, dist_right: float):
    """
    Translates sensor threats into asymmetric wing motor commands.
    """
    threat_l = np.clip(1.0 / (dist_left + 1e-3), 0.0, 1.0)
    threat_f = np.clip(1.0 / (dist_front + 1e-3), 0.0, 1.0)
    threat_r = np.clip(1.0 / (dist_right + 1e-3), 0.0, 1.0)
    
    # Bilateral asymmetric motor activation
    rate_left = 0.5 + (0.5 * threat_r) - (0.4 * threat_l)
    rate_right = 0.5 + (0.5 * threat_l) - (0.4 * threat_r)
    
    yaw = float((rate_right - rate_left) * 45.0)
    thrust = float(np.clip(1.0 - (0.8 * threat_f), 0.1, 1.0))
    return yaw, thrust

test_cases = [
    ("Clear Corridor", 12.0, 12.0, 12.0),
    ("Head-on Wall", 12.0, 0.8, 12.0),
    ("Left Proximity Hazard", 0.6, 8.0, 12.0),
    ("Right Proximity Hazard", 12.0, 8.0, 0.5),
]

print("\n--- Testing Neuromorphic Motor Translation ---")
for scenario, l, f, r in test_cases:
    yaw, thrust = bio_flight_controller(l, f, r)
    print(f"[{scenario:24}] L={l:<4.1f} F={f:<4.1f} R={r:<4.1f} -> Yaw: {yaw:+6.2f}°/t | Thrust: {thrust:.2f}")

