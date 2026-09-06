# Neuromorphic Zero-Trust Agent Pipeline

[![Security Architecture](https://img.shields.io/badge/Security-Zero--Trust%20%7C%20HMAC--SHA256-blue.svg)](#-security-architecture-zero-trust-model)
[![Neuroscience](https://img.shields.io/badge/Connectome-FlyWire%20FAFB%20v783-purple.svg)](#-neuromorphic-engine)
[![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Node.js%20%7C%20Mineflayer-green.svg)](#-system-architecture)
[![Testing](https://img.shields.io/badge/Tests-Pytest%20%7C%20Fuzzing-orange.svg)](#-testing--adversarial-validation)

An autonomous sensory-motor agent driven by real Drosophila melanogaster (fruit fly) connectome synapse graphs, isolated behind an HMAC-authenticated, rate-limited Zero-Trust UDP telemetry gateway.

---

## System Architecture

The project decouples the untrusted sensory agent from the internal neuromorphic motor engine via a cryptographically enforced physical boundary:

```text
  [ Minecraft World / Mobs / Terrain ]
                 │
                 ▼
     ┌───────────────────────┐
     │   Mineflayer Agent    │ ◄── [ 3-Ray LiDAR + Melee Reflexes ]
     │      (`bot.js`)       │
     └───────────┬───────────┘
                 │
                 │ Signed UDP Telemetry (Port 5005)
                 │ HMAC-SHA256 Canonical JSON
                 ▼
    ═══════════════════════════  ◄── [ ZERO-TRUST CRYPTOGRAPHIC BOUNDARY ]
                 │
     ┌───────────▼───────────┐
     │ Cryptographic Gateway │ ◄── [ Signature Verifier + Anomaly Gate ]
     │     (`server.py`)     │
     └───────────┬───────────┘
                 │ Validated Telemetry
                 ▼
     ┌───────────────────────┐
     │  Neuromorphic Engine  │ ◄── [ 5.3M+ Synapse Weight Matrix ]
     │     (`engine.py`)     │
     └───────────────────────┘
```

---

## Security Architecture (Zero-Trust Model)

Designed around perimeter-defense and telemetry validation principles:

| Attack Vector | Threat Profile | Defense Mechanism | Mitigation Location |
| :--- | :--- | :--- | :--- |
| **Tampering / MITM** | Telemetry interception & packet modification | Canonical JSON serialization signed with HMAC-SHA256 | `server.py` |
| **False Data Injection (FDI)** | Spoofed out-of-bounds raycast values | Hard bounded range gate (0.0m <= d <= 16.0m) | `engine.py` |
| **Replay / Physics Spoofing** | Teleportation & impossible velocity anomalies | Temporal rate-of-change smoothing (Delta d <= 2.0m/tick) | `bot.js` & `server.py` |
| **DoS / Protocol Desync** | Corrupted packets & malformed data schemas | Isolated try-catch deserializer with safe hover fallback | `server.py` |

---

## Neuromorphic Engine

The navigation pipeline runs against synaptic connections derived from the **FlyWire Whole-Brain Connectome (FAFB v783)**:

* **Sensory Encoding**: Left, center, and right raycasts map directly to visual optical expansion units (lobula plate tangential cells).
* **Bilateral Inhibition**: Synaptic weight ratios drive differential lateral turns—repelling the bot away from approaching terrain or hostile mobs.
* **Proactive Combat Reflexes**: Emulates giant fiber escape circuits, forcing immediate retaliatory knockback against hostile mobs and executing an autonomous clearance pivot when cornered.

---

## Repository Structure

```text
neuromorphic-sec-pipeline/
├── bot.js                  # Autonomous Mineflayer agent (Sensors, Combat, Reflexes)
├── engine.py               # Neuromorphic matrix processor & motor logic
├── server.py               # Asynchronous UDP verification listener
├── fuzzer.py               # Adversarial telemetry injection & fuzzing suite
├── build_synapse_matrix.py # FlyWire biological synapse parsing tool
├── fly_annotations.csv     # Neuron classification metadata
├── fly_connections.csv.gz  # Raw Drosophila synaptic connection graph
├── tests/                  # Pytest verification suites
└── requirements.txt        # Python dependency manifest
```

---

## Quickstart

### 1. Environment Setup
```bash
# Clone the repository
git clone [https://github.com/LingeshN004/neuromorphic-sec-pipeline.git](https://github.com/LingeshN004/neuromorphic-sec-pipeline.git)
cd neuromorphic-sec-pipeline

# Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Node.js dependencies
npm install
```

### 2. Launching the Hardened Stack
In your first terminal (start the verified UDP gateway):
```bash
python3 server.py
```

In your second terminal (spawn the agent into Minecraft):
```bash
node bot.js
```

### 3. Adversarial Testing & Verification
Execute the test suite and launch the telemetry fuzzer to test Zero-Trust rejection rates:
```bash
# Run integrity & logic unit tests
pytest -v

# Run adversarial packet injection simulator
python3 fuzzer.py
```
