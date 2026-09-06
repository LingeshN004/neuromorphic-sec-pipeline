# Bio-Neuromorphic Zero-Trust Flight Controller

A bio-mimetic autonomous flight controller integrating Princeton's FlyWire connectome data (FAFB v783) with a rule-based Zero-Trust security layer.

## Overview
- **Connectome Weights**: Extracted from 5.3M+ biological synapses connecting sensory inputs to bilateral descending motor neurons (0.4910 Left vs. 0.5090 Right balance ratio).
- **Zero-Trust Security**: Validates all incoming telemetry using HMAC-SHA256 integrity checks, boundary filtering (0.0m - 32.0m), and temporal rate-of-change delta limits.
- **Fail-Safe Mechanism**: Automatically transitions into a safe hover state (`yaw = 0.0`, `thrust = 0.05`) upon detecting False Data Injection (FDI), MITM tampering, or sensor teleportation anomalies.

## Architecture
- `engine.py`: Core neuromorphic motor control logic & Zero-Trust verification gateway.
- `server.py`: Asynchronous UDP telemetry server listening on `127.0.0.1:5005`.
- `client_sim.py`: Simulated flight client streaming telemetry packets.
- `fuzzer.py`: Adversarial test script verifying 100% attack mitigation.
- `test_engine.py`: Comprehensive `pytest` automated test suite.

## Running Tests
```bash
source venv/bin/activate
pytest -v