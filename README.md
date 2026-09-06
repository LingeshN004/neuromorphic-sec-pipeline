# 🧠 Neuromorphic Zero-Trust Agent Pipeline

[![Security Architecture](https://img.shields.io/badge/Security-Zero--Trust%20%7C%20HMAC--SHA256-blue.svg)](#security-architecture)
[![Neuroscience](https://img.shields.io/badge/Connectome-FlyWire%20FAFB%20v783-purple.svg)](#neuromorphic-engine)
[![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Node.js%20%7C%20Mineflayer-green.svg)](#system-architecture)
[![Testing](https://img.shields.io/badge/Tests-Pytest%20%7C%20Fuzzing-orange.svg)](#testing--adversarial-validation)

An autonomous sensory-motor agent driven by real *Drosophila melanogaster* (fruit fly) connectome synapse graphs, isolated behind an HMAC-authenticated, rate-limited Zero-Trust UDP telemetry gateway.

---

## 🏛 System Architecture

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
