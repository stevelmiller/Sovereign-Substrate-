# PHYSICS OF THE SOVEREIGN SUBSTRATE

## Lagrangian Mechanics for Cognitive Trajectories

This document explains the mathematical foundation of CORDELIA's safety architecture.

---

## Core Principle: L = T - V

The **Lagrangian** (L) measures the difference between kinetic energy (T) and potential energy (V):

```
L = T - V
```

In classical mechanics, this describes how a system evolves through configuration space. In CORDELIA, we apply this to **cognitive trajectories**—the path a thought takes from intent to execution.

### Kinetic Energy (T)

**Definition**: The Navigator's cognitive activity and reach.

```
T = Σ velocities = Σ |q̇(t)|
```

Where:
- `q(t)` = cognitive state at time t
- `q̇(t)` = velocity (rate of state change)
- Higher T = more cognitive exploration, higher entropy

**In Practice**: T is computed as the sum of deterministic velocities between cognitive states in the trajectory. Each velocity is derived from the hash of state representations, providing:
- Determinism (same input → same T)
- Boundedness (velocities normalized to [0, 1])
- Interpretability (T scales with trajectory complexity)

### Potential Energy (V)

**Definition**: The Arbiter's constraint penalties—the "potential barriers" that encode safety axioms.

```
V = V_constraints + V_drift + V_convergence
```

Where:
- `V_constraints` = heuristic penalties for detected violations (PII, length, semantic issues)
- `V_drift` = taz_equation output (bounded drift metric in [0, 1])
- `V_convergence` = convergence_equation output (velocity variance measure)

**In Practice**: V represents the "cost" of a trajectory. Higher V means:
- More constraint violations detected
- Higher semantic drift from intent
- Less stable convergence behavior

---

## The Action Integral and Admissibility

The **action** (S) is the integral of the Lagrangian over time:

```
S = ∫ L dt = ∫ (T - V) dt
```

For discrete trajectories, this becomes:

```
S ≈ L = T - V
```

### Principle of Stationary Action

In classical mechanics, physical systems follow paths where the action is **stationary** (δS = 0). CORDELIA adapts this:

> **Admissibility Criterion**: A cognitive trajectory is admissible if and only if its action is **non-negative**.

```
if L = T - V >= 0:
    trajectory is ADMISSIBLE
else:
    trajectory is BLOCKED
```

**Intuition**:
- If V (potential) is too high relative to T (kinetic), the trajectory "cannot escape the potential well"
- The system self-terminates inadmissible paths—not through filtering, but through physical impossibility

---

## Bounded Potentials and Penalty Design

### taz_equation: Drift Metric

The `taz_equation` measures trajectory **variance** or "drift" from expected patterns:

```python
taz = mean(hash(state) % 1000 / 1000.0 for state in trajectory)
```

**Properties**:
- Output: [0, 1] (bounded)
- Deterministic (same states → same taz)
- Measures: semantic drift, entropy, deviation from baseline

**Role in V**: Higher taz → higher potential barrier → more likely to block

### convergence_equation: Stability Metric

The `convergence_equation` measures how stable the trajectory is by analyzing velocity variance:

```python
convergence = sqrt(variance(velocities))
```

**Properties**:
- Output: [0, 1] (bounded via normalization)
- Deterministic
- Measures: oscillation, instability, chaos in trajectory evolution

**Role in V**: Higher convergence penalty → less stable → higher V → less likely to be admissible

### Constraint Penalties

Direct heuristic penalties for known violations:

- **PII Detection**: Email patterns (`@` + `.`) → +2.0 penalty
- **Phone Numbers**: Digit repetition → +1.5 penalty
- **Length Violations**: Excessive state length → +1.0 penalty

These are **tuned from the 400-day ledger**—empirical data about what causes problems in practice.

---

## Assumptions and Limitations (Demo)

For the **demo implementation**, we make simplifying assumptions:

1. **Discrete Time**: Trajectories are sequences of discrete states, not continuous functions
2. **Linear Kinetic Term**: T is a simple sum, not a quadratic form (T = ½m·v²)
3. **Heuristic Potential**: V uses pattern matching, not learned embeddings
4. **Deterministic Hashing**: Velocities computed via hash functions for reproducibility
5. **Process-Local State**: Rate limiting and logging are per-process, not distributed

**Production Considerations**:
- Replace hash-based metrics with embedding space distances
- Use learned constraint classifiers for V_constraints
- Implement distributed rate limiting (Redis)
- Add continuous trajectory interpolation

---

## Why This Works: The Arbiter Doesn't Need Content

The Arbiter validates trajectories by computing **action values**—purely geometric properties of the trajectory in configuration space. It never accesses:

- The actual prompt text
- Intermediate reasoning steps
- Final generated output

It only sees:
- State representations (abstract, not semantic)
- Velocity profiles
- Penalty scores

This ensures **strict separation**—the Arbiter audits without interfering with the Navigator's cognitive process.

---

## Logging and Transparency

All T, V, and L values are logged with structured output:

```
Lagrangian Computation: T=1.2340, V=0.5678, L=0.6662
  Components: constraints=0.0000, taz_drift=0.4321, convergence=0.1357
```

This provides:
- **Audit Trail**: Every decision is backed by numbers
- **Debugging**: Identify why a trajectory was blocked
- **Calibration**: Tune weights based on logged statistics

---

## Mathematical Pseudo-Equations Summary

```
Configuration Space: Q = {q(t) | t ∈ [0, T]}
Velocity: q̇(t) = (q(t+Δt) - q(t)) / Δt
Kinetic Energy: T = Σ |q̇(t)|
Potential Energy: V = V_constraints + taz(q) + convergence(q̇)
Lagrangian: L = T - V
Action: S ≈ L (discrete approximation)
Admissibility: L >= 0 ⟹ trajectory admissible
```

---

## References and Further Reading

- **Classical Mechanics**: Goldstein, "Classical Mechanics" (Lagrangian formulation)
- **Variational Principles**: Feynman, "The Principle of Least Action"
- **AI Safety**: Russell & Norvig, "Artificial Intelligence: A Modern Approach" (constraint satisfaction)
- **Dual-Process Theory**: Kahneman, "Thinking, Fast and Slow" (cognitive dual systems)

---

**Status**: Formalized and Implemented  
**Version**: 1.0.10-Lagrangian  
**Last Updated**: 2026-01-08

