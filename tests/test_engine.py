import pytest
import numpy as np
from engine import FlySecurityEngine, sign_packet, SYNAPSE_WEIGHT_LEFT, SYNAPSE_WEIGHT_RIGHT

@pytest.fixture
def engine():
    """Initializes a fresh security engine for each test."""
    return FlySecurityEngine()

def test_connectome_bilateral_ratio():
    """Verify biological weights sum to 1.0 within normal symmetry margins."""
    total = SYNAPSE_WEIGHT_LEFT + SYNAPSE_WEIGHT_RIGHT
    assert np.isclose(total, 1.0)
    assert 0.48 < SYNAPSE_WEIGHT_LEFT < 0.52
    assert 0.48 < SYNAPSE_WEIGHT_RIGHT < 0.52

def test_nominal_forward_flight(engine):
    """Test open space results in forward flight with minimal yaw drift."""
    pkt = sign_packet({"left": 15.0, "front": 20.0, "right": 15.0})
    res = engine.step(pkt)
    assert res["status"] == "ACCEPTED"
    assert abs(res["yaw"]) < 1.0
    assert res["thrust"] > 0.8

def test_left_wall_avoidance(engine):
    """Test agent banks right when obstacle closes in on the left."""
    pkt = sign_packet({"left": 1.0, "front": 10.0, "right": 12.0})
    res = engine.step(pkt)
    assert res["status"] == "ACCEPTED"
    assert res["yaw"] > 5.0  # Positive yaw turns right

def test_right_wall_avoidance(engine):
    """Test agent banks left when obstacle closes in on the right."""
    pkt = sign_packet({"left": 12.0, "front": 10.0, "right": 1.0})
    res = engine.step(pkt)
    assert res["status"] == "ACCEPTED"
    assert res["yaw"] < -5.0  # Negative yaw turns left

def test_attack_fdi_negative_rejected(engine):
    """Reject false data injection with negative values."""
    pkt = sign_packet({"left": -2.0, "front": 10.0, "right": 10.0})
    res = engine.step(pkt)
    assert res["status"] == "BLOCKED"
    assert res["thrust"] == 0.05
    assert res["yaw"] == 0.0

def test_attack_hmac_tamper_rejected(engine):
    """Reject packets with altered signatures."""
    pkt = {"data": {"left": 5.0, "front": 5.0, "right": 5.0}, "signature": "bad_sig"}
    res = engine.step(pkt)
    assert res["status"] == "BLOCKED"
    assert res["thrust"] == 0.05

def test_attack_teleport_delta_rejected(engine):
    """Reject sudden distance teleportation exceeding physical bounds."""
    pkt1 = sign_packet({"left": 5.0, "front": 5.0, "right": 5.0})
    engine.step(pkt1)
    
    # 5.0m to 25.0m delta is 20m, exceeding 10.0m limit
    pkt2 = sign_packet({"left": 25.0, "front": 5.0, "right": 5.0})
    res = engine.step(pkt2)
    assert res["status"] == "BLOCKED"
    assert res["thrust"] == 0.05