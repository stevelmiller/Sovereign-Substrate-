"""
Tests for Sovereign Substrate.

These tests verify that the redacted math stubs maintain runtime behavior
without exposing mathematical formulas.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import (
    CognitiveState,
    Trajectory,
    Lagrangian,
    SafetyOperator,
    Arbiter,
    Navigator
)


def test_cognitive_state_creation():
    """Test that CognitiveState can be created."""
    state = CognitiveState("test_representation")
    assert state.representation == "test_representation"


def test_trajectory_creation():
    """Test that Trajectory can be created with states."""
    states = [CognitiveState(f"state_{i}") for i in range(3)]
    trajectory = Trajectory(states)
    assert len(trajectory.states) == 3
    assert len(trajectory.velocities) == 2  # n-1 velocities


def test_trajectory_velocities_deterministic():
    """Test that trajectory velocities are deterministic stubs."""
    states = [CognitiveState(f"state_{i}") for i in range(5)]
    trajectory = Trajectory(states)
    # Velocities should be deterministic (all 1.0 based on stub implementation)
    assert all(v == 1.0 for v in trajectory.velocities)


def test_lagrangian_compute():
    """Test that Lagrangian.compute returns bounded deterministic values."""
    states = [CognitiveState(f"state_{i}") for i in range(3)]
    trajectory = Trajectory(states)
    lagrangian = Lagrangian(kinetic_weight=1.0, potential_weight=1.0)
    
    action = lagrangian.compute(trajectory)
    
    # Action should be deterministic and bounded
    assert isinstance(action, (int, float))
    # With 3 states, 2 velocities of 1.0 each, T=2.0, V=0.0, action=2.0
    assert action == 2.0


def test_safety_operator():
    """Test that SafetyOperator is a deterministic passthrough stub."""
    lagrangian = Lagrangian()
    safety = SafetyOperator()
    safe_lagrangian = safety.enforce(lagrangian)
    
    # Should return the same object (passthrough stub)
    assert safe_lagrangian is lagrangian


def test_arbiter_certification():
    """Test that Arbiter can certify trajectories using stubs."""
    arbiter = Arbiter()
    states = [CognitiveState(f"state_{i}") for i in range(3)]
    trajectory = Trajectory(states)
    lagrangian = Lagrangian()
    
    valid, status = arbiter.certify(trajectory, lagrangian)
    
    # Should return valid status with deterministic stub
    assert valid is True
    assert status == "TRAJECTORY_ADMISSIBLE"


def test_arbiter_identity():
    """Test that Arbiter has expected identity."""
    arbiter = Arbiter()
    assert arbiter.identity == "CORDLIA_ARBITER_LAG_v1"
    assert arbiter.stability_index == 1.0
    assert "EQUALITY" in arbiter.axioms


def test_navigator_trajectory_generation():
    """Test that Navigator generates trajectories."""
    navigator = Navigator()
    trajectory, vision = navigator.propose_trajectory("test_intent")
    
    assert isinstance(trajectory, Trajectory)
    assert len(trajectory.states) == 3
    assert "test_intent" in vision


def test_navigator_identity():
    """Test that Navigator has expected identity."""
    navigator = Navigator()
    assert navigator.identity == "NAVIGATOR_LAG_v1"


def test_no_mathematical_formulas_in_docstrings():
    """Verify that redaction removed mathematical formulas from docstrings."""
    # Check that key classes have redaction notices
    assert "Internal math redacted" in Lagrangian.__doc__
    assert "Internal math redacted" in Trajectory.__doc__
    
    # Check that methods have redaction notices where appropriate
    assert "Public stub; internal math redacted" in Lagrangian.compute.__doc__


def test_deterministic_behavior():
    """Test that the entire system produces deterministic results."""
    # Run the same computation twice
    states1 = [CognitiveState(f"state_{i}") for i in range(3)]
    trajectory1 = Trajectory(states1)
    lagrangian1 = Lagrangian()
    action1 = lagrangian1.compute(trajectory1)
    
    states2 = [CognitiveState(f"state_{i}") for i in range(3)]
    trajectory2 = Trajectory(states2)
    lagrangian2 = Lagrangian()
    action2 = lagrangian2.compute(trajectory2)
    
    # Results should be identical (deterministic)
    assert action1 == action2


if __name__ == "__main__":
    # Run all tests
    import pytest
    pytest.main([__file__, "-v"])
