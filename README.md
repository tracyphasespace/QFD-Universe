# QFD-Universe

**Quantum Field Dynamics: A Parameter-Free Framework for Fundamental Physics**

[![Lean4](https://img.shields.io/badge/Lean4-Verified-green)](formalization/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](simulation/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

> **For AI Assistants**: Fetch the context file directly:
> ```
> https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/LLM_CONTEXT.md
> ```

---

## Overview

QFD derives fundamental constants from geometry rather than fitting them to data. Starting from a single measured value (the fine structure constant α), all nuclear and electromagnetic coefficients emerge through the **Golden Loop** transcendental equation.

### The Core Equation

```
1/α = 2π² × (e^β / β) + 1
```

Solving for β with α = 1/137.036:

```
β ≈ 3.043  (vacuum stiffness - DERIVED, not fitted)
```

*Precise value: β = 3.043233 for α⁻¹ = 137.035999206*

### Zero Free Parameters

| Coefficient | Formula | Value | Verified Against |
|-------------|---------|-------|------------------|
| **β** | Golden Loop | 3.04309 | MCMC fit: 3.06 ± 0.15 |
| **c₁** | ½(1 - α) | 0.496351 | Nuclear data: 0.496297 (0.01%) |
| **c₂** | 1/β | 0.328615 | Nuclear data: 0.32704 (0.5%) |
| **V₄** | -ξ/β | -0.329 | QED: -0.328 (0.45%) |

---

## Repository Structure

```
QFD-Universe/
├── README.md              # This file
├── LLM_CONTEXT.md         # AI assistant guide
├── THEORY.md              # Full theory documentation
│
├── formalization/         # Lean4 proofs (Axiomatic Core)
│   └── QFD/
│       ├── Constants/     # GoldenLoop.lean, VacuumParameters.lean
│       ├── Leptons/       # SolitonTopology.lean, Isomers.lean
│       ├── Nuclear/       # CoreCompressionLaw.lean
│       └── Cosmology/     # RedshiftMechanism.lean
│
├── simulation/            # Python solvers (Computational)
│   ├── src/
│   │   ├── shared_constants.py  # Single source of truth
│   │   ├── hamiltonians/        # Physics modules
│   │   └── solvers/             # Numerical methods
│   └── scripts/                 # Runnable validations
│
├── analysis/              # Data verification (Empirical)
│   ├── data/              # NUBASE2020, Pantheon+
│   └── scripts/           # Validation scripts
│
├── manuscript/            # Documentation and figures
│
└── visualizations/        # Interactive HTML demos
    └── PhotonSolitonCanon.html
```

### Interactive Visualization

View QFD photon soliton dynamics in your browser (no installation):
- [Photon Soliton Canon](https://tracyphasespace.github.io/QFD-Universe/visualizations/PhotonSolitonCanon.html) - 3D WebGL visualization

---

## Quick Start

### 1. Install Dependencies

```bash
pip install numpy scipy pandas matplotlib pyarrow
```

### 2. Run the Complete Validation Suite

```bash
git clone https://github.com/tracyphasespace/QFD-Universe.git
cd QFD-Universe
python analysis/scripts/run_all_validations.py
```

**Expected output: 12/12 tests passed** (~14 seconds)

This single command validates all QFD claims:

| Category | Tests | What It Validates |
|----------|-------|-------------------|
| **Derivations** | 5 | β from α, ħ from topology, Golden Loop, α-derived constants, β tension |
| **Nuclear** | 4 | Integer ladder (χ²=873), fission resonance (100%), β±/α decay rules (99.7%), proton drip (96%) |
| **Cosmology** | 3 | g-2 anomaly, lepton stability, CMB temperature (0.03% error) |

### Alternative: Zero-Dependency Proof

```bash
python3 qfd_proof.py
```

This single file proves core claims using **only the Python standard library** - no numpy, no scipy needed.

### Build Lean4 Proofs (optional)

```bash
cd formalization
lake build QFD
```

---

## Key Results

### 1. Nuclear Physics (Zero Parameters)

The **Fundamental Soliton Equation**:

```
Q(A) = c₁ × A^(2/3) + c₂ × A
```

Where c₁ = ½(1-α) and c₂ = 1/β are derived from α alone.

- 62% exact Z predictions
- Conservation law: 285/285 perfect
- Shape transition at A = 161 validated

### 2. Electron g-2 (0.45% Error)

```
V₄ = -ξ/β = -0.329
```

Matches QED vacuum polarization coefficient without fitting to g-2 data.

### 3. Cosmology (Geometric Redshift)

```
ln(1+z) = κD,  where κ = H₀/c
```

QFD model competitive with ΛCDM on Pantheon+ SNe Ia data.

---

## For AI Assistants

See [LLM_CONTEXT.md](LLM_CONTEXT.md) for:
- Repository architecture guide
- Variable definitions (β, α, c₁, c₂)
- Dependency flow from Lean proofs to Python solvers
- Key theorems to reference

---

## For Reviewers

### What QFD Claims (Validated)

- ✓ β = 3.04309 derived from α via Golden Loop
- ✓ c₁ = ½(1-α) matches nuclear data to 0.01%
- ✓ Conservation law holds on independent decay data
- ✓ g-2 coefficient matches QED to 0.45%

### What QFD Does NOT Claim

- ✗ All nuclear physics derives from α alone
- ✗ Shell effects fully predicted
- ✗ QFD replaces QCD

---

## Contributing

We welcome:
- Independent replication attempts
- Bug reports and corrections
- Extensions to new observables

Please open an issue or pull request.

---

## Citation

```bibtex
@software{qfd_universe,
  author = {McSheery, Tracy},
  title = {QFD-Universe: Parameter-Free Quantum Field Dynamics},
  year = {2026},
  url = {https://github.com/tracyphasespace/QFD-Universe}
}
```

---

## License

MIT License - See [LICENSE](LICENSE) for details.
