import pandas as pd
import numpy as np

print("[*] Parsing descending motor neurons...")
annot_df = pd.read_csv("fly_annotations.csv", compression="gzip", low_memory=False)
descending = annot_df[annot_df["super_class"] == "descending"]

left_dns = set(descending[descending["side"] == "left"]["root_id"])
right_dns = set(descending[descending["side"] == "right"]["root_id"])

print(f"[+] Found {len(left_dns)} Left DNs and {len(right_dns)} Right DNs")

print("[*] Streaming filtered synapse connections (this processes ~68MB)...")
# Process in chunks to keep memory usage low
chunksize = 250000
left_incoming_synapses = 0
right_incoming_synapses = 0
total_edges = 0

for chunk in pd.read_csv("fly_connections.csv.gz", compression="gzip", chunksize=chunksize, low_memory=False):
    total_edges += len(chunk)
    
    # Filter for connections targeting our descending motor neurons
    left_hits = chunk[chunk["post_root_id"].isin(left_dns)]
    right_hits = chunk[chunk["post_root_id"].isin(right_dns)]
    
    left_incoming_synapses += left_hits["syn_count"].sum()
    right_incoming_synapses += right_hits["syn_count"].sum()

print("\n" + "=" * 55)
print("BIOLOGICAL SYNAPSE AGGREGATION RESULTS")
print("=" * 55)
print(f"[+] Total Synaptic Edges Scanned:    {total_edges:,}")
print(f"[+] Total Synapses -> Left Motor DNs:  {left_incoming_synapses:,}")
print(f"[+] Total Synapses -> Right Motor DNs: {right_incoming_synapses:,}")

# Compute bilateral symmetry ratio
ratio = left_incoming_synapses / max(right_incoming_synapses, 1)
print(f"[+] Hemispheric Balance Ratio:         {ratio:.4f}")
print("=" * 55)
