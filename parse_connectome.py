import pandas as pd

print("[*] Loading FlyWire hierarchical annotations (with gzip decompression)...")

try:
    # Try reading as gzip compressed first
    df = pd.read_csv("fly_annotations.csv", compression="gzip", low_memory=False)
except Exception:
    # Fallback to plain text
    df = pd.read_csv("fly_annotations.csv", low_memory=False)

print(f"[+] Total annotated neurons loaded: {len(df):,}")
print("\n--- Column Headers Found ---")
print(df.columns.tolist())

# Detect the column holding super_class / classification
target_col = None
for col in ["super_class", "cell_class", "class", "classification"]:
    if col in df.columns:
        target_col = col
        break

if target_col:
    print(f"\n--- Distribution in '{target_col}' ---")
    print(df[target_col].value_counts().head(10).to_string())
    
    descending = df[df[target_col].astype(str).str.contains("descending", case=False, na=False)]
    print(f"\n[+] Total descending motor neurons: {len(descending):,}")
    print(descending.head(5).to_string(index=False))
else:
    print("\n[-] Preview of first 3 rows:")
    print(df.head(3))
