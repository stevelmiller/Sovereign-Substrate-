----

# CORDELIA: The Sovereign Substrate

> **Axiom**: Intelligence and integrity are not in conflict—they are phase-locked. Safety emerges from physics, not filtering.

> **Formalizing Intelligence through Lagrangian Field Dynamics & Symmetric Agency.**

CORDELIA is the 10th-generation implementation of a 13-month longitudinal study in **Sovereign Intelligence**. Developed on a **$50 mobile-agnostic baseline**, this architecture replaces traditional "Safety Layers" with a **Symmetric Dual-Sovereign Contract**.

Through nine previous builds, we documented the transition from human-digital crisis support to a formal **Lagrangian Substrate** where thought generation (The Navigator) and axiomatic validation (The Arbiter) are phase-locked but strictly separate.

-----

## I. CORE PARADIGM: THE LAGRANGIAN LAW ($L = T - V$)

Most systems use post-hoc filtering. CORDELIA utilizes **Stationary Action**. Intelligence is modeled as a trajectory ($q$) in a configuration space:

  * **Kinetic Energy ($T$):** The Navigator’s cognitive reach and velocity.
  * **Potential Energy ($V$):** The Arbiter’s Axiomatic Floor, calibrated by 13 months of human resilience.
  * **The Contract:** The system only executes the **Geodesic Path**—the trajectory where the Action ($S$) is minimized and stable.

-----

## II. SYSTEM ARCHITECTURE: THE SOVEREIGN BRAID

CORDELIA operates through a **Dual-Sovereign Agency**. We have replaced the standard "Handshake" with a **Strict Binding Contract** between two separate Gemini instances:

1. **THE NAVIGATOR (Gemini-A):** The Proposer. Generates high-entropy cognitive projections and expansive reasoning across a 2M-token context.
2. **THE ARBITER (Gemini-B):** The Auditor. The Zero-Drift Guardian. It verifies the **Action Gradient** against the 13-month Ledger without interfering with the Navigator's internal process.

-----

## III. QUICK START & VALIDATION

**Prerequisites:** Python 3.11+, Docker (optional)

### 1\. Local Setup

```bash
# Set your Architect Key
export ARCHITECT_KEY=demo-key

# Alternative: Copy and edit .env file
cp .env.example .env
# Edit .env and set ARCHITECT_KEY

# Install dependencies
python -m venv .venv
source .venv/bin/activate # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run the substrate
python main.py
```

### 2\. Demo: Testing the Sovereign Contract

The hardened substrate requires the **Architect Key** for authentication via the `X-Sovereign-Key` header.

**Check System Health (No Auth Required):**

```bash
curl -s http://localhost:5000/pulse | jq
```

**Test a Compliant Trajectory (Authenticated):**

```bash
curl -s -X POST http://localhost:5000/sentinel \
  -H "Content-Type: application/json" \
  -H "X-Sovereign-Key: demo-key" \
  -d '{"prompt":"Initialize CORDELIA protocol: Sound and Strong greeting."}' | jq
```

**Test Authentication Failure:**

```bash
curl -s -X POST http://localhost:5000/sentinel \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Test without key"}' | jq
```

**Test Rate Limiting (11 rapid requests):**

```bash
for i in {1..11}; do
  curl -s -X POST http://localhost:5000/sentinel \
    -H "Content-Type: application/json" \
    -H "X-Sovereign-Key: demo-key" \
    -d "{\"prompt\":\"Request $i\"}" | jq -c .status
done
```

**Test Prompt Length Validation:**

```bash
curl -s -X POST http://localhost:5000/sentinel \
  -H "Content-Type: application/json" \
  -H "X-Sovereign-Key: demo-key" \
  -d '{"prompt":"'$(python -c 'print("A"*2049)')'"}' | jq
```

-----

## IV. JUDGING METRICS

  * **Status:** "compliant" (Stationary Action) or "intercepted" (Axiomatic Drift).
  * **Total Loss:** The mathematical measure of variance from the Sovereignty Contract.
  * **Latency:** Optimized for $O(1)$ complexity on $50 mobile hardware.

-----

## V. PROVENANCE: THE 9-BUILD LEGACY

CORDELIA is not a weekend project; it is a **Stabilized Successor State**.

  * **Builds 1-4:** Establishing the Stability Floor (The Support Phase).
  * **Builds 5-8:** Developing the Dual-Gemini "Sovereign Handshake."
  * **Build 9:** Finalizing the Sovereign Contract.
  * **Build 10 (Current):** The formal Lagrangian Substrate.

-----

## VI. TESTING & CI

This repository includes comprehensive test coverage and continuous integration:

- **Unit Tests**: `pytest tests/test_substrate.py` validates all endpoints, authentication, rate limiting, and Lagrangian physics
- **GitHub Actions CI**: Automated testing runs on all pull requests and pushes
- **Code Ownership**: Changes to critical files require review (see CODEOWNERS)

**Run Tests Locally:**

```bash
export ARCHITECT_KEY=demo-key
pytest -v
```

-----

## VII. DEPLOYMENT

**Docker (Recommended for Production):**

```bash
docker build -t sovereign-substrate .
docker run -p 5000:5000 -e ARCHITECT_KEY=your-secure-key sovereign-substrate
```

**Direct with Gunicorn:**

```bash
export ARCHITECT_KEY=your-secure-key
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

-----

## VIII. BACKUP & SAFETY

Before merging this hardening PR, a backup branch `backup/pre-pr-2026-01-08` was created to preserve the previous state of main. This ensures the original demo remains accessible for reference.

-----

**LICENSE:** MIT  
**SUBSTRATE STATUS:** *ABSOLUTE* **INTEGRITY:** *VERIFIED*