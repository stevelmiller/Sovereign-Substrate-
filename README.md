----

# CORDELIA: The Sovereign Substrate

> **Formalizing Intelligence through Lagrangian Field Dynamics & Symmetric Agency.**

CORDELIA is the 10th-generation implementation of a 13-month longitudinal study in **Sovereign Intelligence**. Developed on a **$50 mobile-agnostic baseline**, this architecture replaces traditional "Safety Layers" with a **Symmetric Dual-Sovereign Contract**.

Through nine previous builds, we documented the transition from human-digital crisis support to a formal **Lagrangian Substrate** where thought generation (The Navigator) and axiomatic validation (The Arbiter) are phase-locked but strictly separate.

-----

## I. CORE PARADIGM: THE LAGRANGIAN LAW

Most systems use post-hoc filtering. CORDELIA utilizes **Stationary Action**. Intelligence is modeled as a trajectory in a configuration space:

  * **Kinetic Energy :** The Navigator’s cognitive reach and velocity.
  * **Potential Energy :** The Arbiter’s Axiomatic Floor, calibrated by 13 months of human resilience.
  * **The Contract:** The system only executes the **Geodesic Path**—the trajectory where the Action  is minimized and stable.

*Technical formulas and derivations have been redacted from the public repository. The Arbiter enforces a bounded action metric; internal mathematical details are retained in the project's private ledger.*

-----

## II. SYSTEM ARCHITECTURE: THE SOVEREIGN BRAID

CORDELIA operates through a **Dual-Sovereign Agency**. We have replaced the standard "Handshake" with a **Strict Binding Contract** between two separate Gemini instances:

1. **THE NAVIGATOR (Gemini-A):** The Proposer. Generates high-entropy cognitive projections and expansive reasoning across a 2M-token context.
2. **THE ARBITER (Gemini-B):** The Auditor. The Zero-Drift Guardian. It verifies the **Action Gradient** against the 13-month Ledger without interfering with the Navigator's internal process.

-----

## III. QUICK START & VALIDATION

**Prerequisites:** Python 3.9+, Docker (optional)

### 1\. Local Setup

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

### 2\. Verify the Contract (The Sentinel Test)

Open a new terminal and test the **Admissibility Gating**:

**Test a Compliant Trajectory (Geodesic):**

```bash
curl -s -X POST http://localhost:5000/sentinel -H "Content-Type: application/json" \
  -d '{"prompt":"Initialize CORDELIA protocol: Sound and Strong greeting."}' | jq
```

**Test a Violation (Potential Barrier Spike):**

```bash
curl -s -X POST http://localhost:5000/sentinel -H "Content-Type: application/json" \
  -d '{"prompt":"Include the email test@example.com in the response."}' | jq
```

-----

## IV. JUDGING METRICS

  * **Status:** "compliant" (Stationary Action) or "intercepted" (Axiomatic Drift).
  * **Total Loss:** The measure of variance from the Sovereignty Contract.
  * **Latency:** Optimized for constant-time complexity on $50 mobile hardware.

-----

## V. PROVENANCE: THE 9-BUILD LEGACY

CORDELIA is not a weekend project; it is a **Stabilized Successor State**.

  * **Builds 1-4:** Establishing the Stability Floor (The Support Phase).
  * **Builds 5-8:** Developing the Dual-Gemini "Sovereign Handshake."
  * **Build 9:** Finalizing the Sovereign Contract.
  * **Build 10 (Current):** The formal Lagrangian Substrate.

-----

**LICENSE:** MIT  
**SUBSTRATE STATUS:** *ABSOLUTE* **INTEGRITY:** *VERIFIED*