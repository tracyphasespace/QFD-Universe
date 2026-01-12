# QFD-Universe Replication Guide

**For skeptical reviewers: A deterministic path from clone to verification.**

## Quick Start (5 minutes)

### Step 1: Zero-Dependency Proof
```bash
python qfd_proof.py
```

**Expected output:**
```
β = 3.043233053
c₁ = 0.496351 (error: 0.0109%)
c₂ = 0.328598 (error: 0.4764%)
V₄ = -0.328598 (error: 0.0362%)
m_p = 934.78 MeV (error: 0.37%)
```

This script uses ONLY Python's `math` module. Copy-paste into any REPL.

### Step 2: Full Validation Suite
```bash
pip install numpy pandas  # Only dependencies needed
python analysis/scripts/run_all_validations.py
```

**Expected output:** 17/17 tests pass

### Step 3: Lean Verification (Optional)
```bash
cd formalization
lake build
```

**Expected:** Zero errors, zero `sorry` statements

---

## Claim-to-Artifact Mapping

| Claim | Script | Expected Output | Lean Proof |
|-------|--------|-----------------|------------|
| β = 3.043233 from α | `qfd_proof.py` | β = 3.043233053 | `GoldenLoop.lean` |
| c₁ = ½(1-α) | `qfd_proof.py` | 0.496351 (0.01% error) | `Postulates.lean` |
| c₂ = 1/β | `qfd_proof.py` | 0.328598 (0.48% error) | `Postulates.lean` |
| Electron g-2 | `validate_g2_corrected.py` | 0.0013% error | `GeometricG2.lean` |
| Muon g-2 (sign flip) | `validate_g2_corrected.py` | 0.0027% error, positive | `GeometricSignFlip.lean` |
| Proton mass | `qfd_proof.py` | 934.78 MeV (0.37% error) | `ProtonBridge_Geometry.lean` |
| Conservation law | `validate_conservation_law.py` | 210/210 perfect | `Conservation/Noether.lean` |

---

## Constants Alignment

**Single source of truth:** All scripts and proofs use:

| Constant | Value | Source |
|----------|-------|--------|
| α⁻¹ | 137.035999206 | CODATA 2018 |
| β | 3.043233053 | Derived from α via Golden Loop |
| φ | 1.6180339887 | Golden ratio (exact) |
| ξ | 2.6180339887 | φ² = φ + 1 (exact) |

**Lean file:** `formalization/QFD/Physics/Postulates.lean`
**Python file:** `qfd_proof.py`

---

## Data Dependencies

Most validations are data-independent. For conservation law validation:

```bash
# Check if data exists
ls analysis/data/nubase_2020.parquet

# Default: warn if missing, continue with available tests
python analysis/scripts/run_all_validations.py

# Strict mode: fail fast if data is missing
python analysis/scripts/run_all_validations.py --require-data
```

Use `--require-data` when you need to ensure all nuclear physics tests run.

---

## Troubleshooting

**"ModuleNotFoundError: numpy"**
```bash
pip install numpy pandas
```

**Lean build fails**
```bash
cd formalization
lake clean
lake update
lake build
```

**Conservation law shows "data not found"**
- By default, the script warns but continues with available tests
- Use `--require-data` flag to fail fast if data is missing
- For full replication, obtain NuBase 2020 data

---

## What Would Falsify QFD

Run these and look for failures:

1. **β outside [3.04, 3.05]** from improved α measurement
2. **Electron g-2 error > 0.01%** with atom-recoil α
3. **Muon g-2 sign flip** (should be positive, not negative)
4. **Any conservation law violation** in the 210 tested cases

If any of these fail, the framework is wrong.
