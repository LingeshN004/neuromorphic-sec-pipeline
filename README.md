# Neuromorphic Zero-Trust Agent Pipeline

[![Security Architecture](https://img.shields.io/badge/Security-Zero--Trust%20%7C%20HMAC--SHA256-blue.svg)](#-security-architecture-zero-trust-model)
[![Neuroscience](https://img.shields.io/badge/Connectome-FlyWire%20FAFB%20v783-purple.svg)](#-neuromorphic-engine)
[![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Node.js%20%7C%20Mineflayer-green.svg)](#-system-architecture)
[![Testing](https://img.shields.io/badge/Tests-Pytest%20%7C%20Fuzzing-orange.svg)](#-testing--adversarial-validation)

> **What happens when you transplant the biological brain wiring of a real fruit fly into an autonomous Minecraft agent—and then wrap its entire nervous system inside a military-grade Zero-Trust cryptographic fortress?**

---

## What Is This? 

Imagine taking the literal neural wiring of an insect over **5.3 million real biological synapses** mapped by neuroscientists at Princeton University and turning it into an artificial brain that pilots a Minecraft bot in real time.

Now imagine treating that bot like an untrusted military drone operating in hostile territory:

* **The Body (Mineflayer / Node.js):** Wanders the world using a custom 3-ray LiDAR vision system to measure obstacles, senses incoming threats, and executes hardwired survival reflexes (proactive mob knockbacks, ledge vaults, and tactical retreats).
* **The Nervous System (HMAC-SHA256 UDP Bridge):** Instead of trusting the bot's raw sensory data, every millisecond of vision is cryptographically signed and fired across an isolated UDP socket.
* **The Firewall (Zero-Trust Security Gateway):** A hardened Python gatekeeper inspects every incoming packet. If an attacker injects fake distances, tampers with the payload, or fakes impossible speeds, the gateway drops the packet instantly and commands the bot to enter emergency fail-safe mode.
* **The Brain (Neuromorphic Connectome Engine):** Only cryptographically authenticated, physically verified sensations are allowed into the 5.3-million-synapse neural matrix, where real biological circuits steer the agent across complex terrain.

It’s part neuroscience experiment, part autonomous robotics platform, and part hard-core network security testbed.

---

## System Architecture

```text
       [ Minecraft World: Hostile Mobs & Rough Terrain ]
                             │
                             ▼
                 ┌───────────────────────┐
                 │   Mineflayer Agent    │
                 │      (`bot.js`)       │
                 │  3-Ray LiDAR Vision   │
                 │  Proactive Mob Combat │
                 │  Step / Wall Detector │
                 └───────────┬───────────┘
                             │
                             │ Signed Telemetry Packets (Port 5005)
                             │ HMAC-SHA256 Canonical JSON
                             ▼
    ═══════════════════════════════════════════════════════════════
               ZERO-TRUST CRYPTOGRAPHIC SECURITY PERIMETER
    ═══════════════════════════════════════════════════════════════
                             │
                 ┌───────────▼───────────┐
                 │ Cryptographic Gateway │
                 │     (`server.py`)     │
                 │ HMAC Signature Verify │
                 │ FDI Anomaly Detector  │
                 │ Rate-of-Change Filter │
                 └───────────┬───────────┘
                             │ Sanitized & Verified Inputs
                             ▼
                 ┌───────────────────────┐
                 │  Neuromorphic Engine  │
                 │     (`engine.py`)     │
                 │  Princeton FlyWire    │
                 │  5.3M+ Synapse Matrix │
                 └───────────────────────┘
```

---

## Security Architecture (Zero-Trust Model)

Built to reflect **CompTIA Security+** defensive architecture principles: assume the client environment is fully compromised, enforce strict boundary verification, and never trust raw sensory data.

| Attack Vector | Threat Scenario | Defense Mechanism | Mitigation Engine |
| :--- | :--- | :--- | :--- |
| **Man-in-the-Middle (MITM)** | Malicious packet sniffing & telemetry alteration | Canonical JSON hashing signed with shared-secret **HMAC-SHA256** | `server.py` |
| **False Data Injection (FDI)** | Spoofed telemetry injecting extreme/negative distances | Hard boundary clipping gate ($0.0\text{m} \le d \le 16.0\text{m}$) | `engine.py` |
| **Physics / Teleport Exploits** | Instantaneous spatial jumps or speed hack anomalies | Temporal rate-of-change smoothing ($\Delta d \le 2.0\text{m/tick}$) | `bot.js` & `server.py` |
| **Malformed Packet DoS** | Corrupted payloads designed to crash the neuromorphic loop | Isolated try-catch deserializer falling back to a safe hover state | `server.py` |

---

## Neuromorphic Connectome Engine

The navigation controller runs on synaptic data directly extracted from the **FlyWire Whole-Brain Connectome (FAFB v783)**:

* **Sensory Encoding:** Left, center, and right raycasts map directly to visual optical expansion units (lobula plate tangential cells).
* **Bilateral Inhibition:** Synaptic weight ratios drive differential lateral turns—naturally repelling the bot away from approaching terrain or hostile mobs.
* **Giant Fiber Survival Reflex:** Emulates the emergency escape circuits found in dipteran insects, forcing an immediate retaliatory knockback swing against mobs followed by an autonomous clearance pivot when cornered.

---

## Repository Structure

```text
neuromorphic-sec-pipeline/
├── bot.js                  # Autonomous Mineflayer agent (Sensors, Combat, Reflexes)
├── engine.py               # Neuromorphic matrix processor & motor logic
├── server.py               # Asynchronous UDP verification listener & security gateway
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

# Configure Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### 2. Launching the Hardened Stack
In your first terminal (start the Zero-Trust cryptographic gateway):
```bash
python3 server.py
```

In your second terminal (spawn the agent into Minecraft):
```bash
node bot.js
```

### 3. Adversarial Testing & Verification
Verify cryptographic enforcement and test Zero-Trust rejection rates against malicious packets:
```bash
# Run integrity & logic unit tests
pytest -v

# Run adversarial packet injection simulator
python3 fuzzer.py
```
