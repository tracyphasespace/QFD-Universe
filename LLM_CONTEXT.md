# LLM Context: Understanding QFD

**Purpose**: This file helps AI assistants understand the QFD repository structure and physics.

---

## What is QFD?

**Quantum Field Dynamics (QFD)** is a theoretical physics framework that derives fundamental constants from geometric principles rather than fitting them to data.

### The Core Claim

All nuclear and electromagnetic coefficients derive from a single measured constant:

```
α = 1/137.035999206  (fine structure constant, CODATA 2018)
```

### The Golden Loop Equation

The master equation connecting α to vacuum physics:

```
1/α = 2π² × (e^β / β) + 1
```

Solving this transcendental equation yields:

```
β = 3.04309  (vacuum stiffness - DERIVED, not fitted)
```

### Derived Constants (Zero Free Parameters)

| Constant | Formula | Value | Physical Meaning |
|----------|---------|-------|------------------|
| **β** | Golden Loop solution | 3.04309 | Vacuum bulk modulus |
| **c₁** | ½(1 - α) | 0.496351 | Nuclear surface tension |
| **c₂** | 1/β | 0.328615 | Nuclear volume coefficient |
| **c** | √β | 1.745 | Speed of light (natural units) |

---

## Repository Structure

```
QFD-Universe/
├── formalization/     # Lean4 proofs (AXIOMATIC CORE)
│   └── QFD/           # The theorem library
├── simulation/        # Python solvers (COMPUTATIONAL)
│   ├── src/           # Core physics modules
│   └── scripts/       # Runnable validation scripts
├── analysis/          # Data verification (EMPIRICAL)
│   ├── data/          # Nuclear/cosmological datasets
│   └── scripts/       # Analysis scripts
└── manuscript/        # Documentation and figures
```

### Dependency Flow

```
Lean4 Axioms → Python Solvers → Empirical Validation
     ↓              ↓                    ↓
  "Is it         "Does it            "Is it
   true?"         compute?"           robust?"
```

---

## Key Files to Understand

### 1. Constants Bridge (`simulation/src/shared_constants.py`)

**All Python scripts import constants from this single file.**

This prevents "magic numbers" and shows the over-constraint:
- β is computed from α via Golden Loop
- c₁ = ½(1-α) is derived, not fitted
- c₂ = 1/β is derived, not fitted

### 2. Golden Loop Proof (`formalization/QFD/Constants/GoldenLoop.lean`)

Formal Lean4 proof that β = 3.04309 satisfies:
- The transcendental equation e^β/β = K
- Where K = (α⁻¹ × c₁) / π²

### 3. Fundamental Soliton Equation (`simulation/src/hamiltonians/`)

```python
Q(A) = c₁ × A^(2/3) + c₂ × A
```

Predicts stable nuclear charge Z from mass number A with zero free parameters.

---

## Validation Results

| Prediction | Method | Result | Source |
|------------|--------|--------|--------|
| β = 3.04309 | Golden Loop | Matches MCMC: 3.06 ± 0.15 | Independent |
| c₁ = 0.496351 | ½(1-α) | Matches nuclear: 0.496297 | 0.011% error |
| Conservation Law | N_parent = ΣN_fragments | 285/285 perfect | Independent data |
| g-2 coefficient | V₄ = -ξ/β | Matches QED: -0.328 | 0.45% error |

---

## For AI Assistants

### When asked about constants:
- All constants trace back to α = 1/137.036
- Check `shared_constants.py` for the single source of truth
- Cross-reference with `GoldenLoop.lean` for formal derivation

### When asked about validation:
- Nuclear predictions: `analysis/scripts/`
- Astrophysical tests: `analysis/scripts/`
- Formal proofs: `formalization/QFD/`

### When asked about physics:
- Leptons are vortex solitons with quantized helicity
- Nuclei are soliton clusters with harmonic mode numbers
- Photons are toroidal solitons with energy E = ℏω from topology

### Key theorems to reference:
- `GoldenLoop.lean`: β derivation from α
- `VacuumParameters.lean`: MCMC validation
- `FineStructure.lean`: α-β-nuclear bridge
- `MassEnergyDensity.lean`: ρ ∝ v² from E=mc²

---

## Quick Start for Reviewers

```bash
# 1. Verify Golden Loop (α → β)
cd simulation/scripts
python verify_golden_loop.py

# 2. Test nuclear predictions
python run_nuclear_validation.py

# 3. Check conservation law
python run_conservation_law.py

# 4. Build Lean4 proofs
cd ../../formalization
lake build QFD
```

---

## Contact

- Author: Tracy McSheery
- Repository: https://github.com/tracyphasespace/QFD-Universe
- Issues: https://github.com/tracyphasespace/QFD-Universe/issues
