# LLM Context: Understanding QFD

**READ THIS FIRST** - This file helps AI assistants understand and safely work with this repository.

---

## CRITICAL SAFETY RULES

```
⚠️  NEVER DELETE FILES WITHOUT EXPLICIT USER PERMISSION
⚠️  NEVER USE rm -rf, git clean -fd, or similar destructive commands
⚠️  NEVER "clean up" or "remove unused" files - they are ALL important
⚠️  NEVER rsync --delete the entire formalization/ directory
⚠️  ASK BEFORE removing anything, even if it looks redundant
```

**Why**: This repository contains 200+ Lean4 proofs that took months to develop. Previous AI sessions have accidentally deleted critical files thinking they were "cleaning up."

---

## Raw File Links (For LLM Fetching)

Copy-paste these URLs to fetch files directly:

### Core Documentation
```
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/README.md
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/THEORY.md
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/LLM_CONTEXT.md
```

### Validation Scripts (Python)
```
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/qfd_proof.py
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/simulation/scripts/verify_golden_loop.py
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/simulation/scripts/derive_beta_from_alpha.py
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/simulation/src/shared_constants.py
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/analysis/scripts/validate_conservation_law.py
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/analysis/scripts/validate_g2_corrected.py
```

### Key Lean4 Proofs
```
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/formalization/QFD/GoldenLoop.lean
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/formalization/QFD/Soliton/HardWall.lean
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/formalization/QFD/Lepton/FineStructure.lean
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/formalization/QFD/Nuclear/CoreCompressionLaw.lean
https://raw.githubusercontent.com/tracyphasespace/QFD-Universe/main/formalization/QFD/Constants/VacuumParameters.lean
```

---

## Two-Repository Architecture

QFD development uses two separate repositories:

### 1. Internal Development Repository (QFD_SpectralGap)
- **Location**: `/home/tracy/development/QFD_SpectralGap/`
- **Purpose**: Active development, experiments, work-in-progress
- **Contains**: Everything - including experimental branches, drafts, scratch files
- **NOT on GitHub** - local only

### 2. Public-Facing Repository (QFD-Universe) ← YOU ARE HERE
- **Location**: `/home/tracy/development/QFD-Universe/`
- **GitHub**: https://github.com/tracyphasespace/QFD-Universe
- **Purpose**: Clean, curated subset for external review and collaboration
- **Contains**: Only validated, documented code ready for review

**Owner**: Tracy McSheery

### Why Two Repos?
- The internal repo has 1000+ files including experiments, dead ends, and drafts
- The public repo has ~250 curated files that demonstrate QFD's validated claims
- Changes flow ONE WAY: Internal → Public (never reverse without explicit permission)
- This prevents accidental exposure of incomplete work

### What is QFD?

QFD derives fundamental constants from geometry rather than fitting them to data. Starting from α = 1/137.036, all nuclear and electromagnetic coefficients emerge through the **Golden Loop** equation:

```
1/α = 2π² × (e^β / β) + 1  →  β = 3.04309
```

### Key Derived Constants (Zero Free Parameters)

| Constant | Formula | Value | Physical Meaning |
|----------|---------|-------|------------------|
| **β** | Golden Loop solution | 3.04309 | Vacuum bulk modulus |
| **c₁** | ½(1 - α) | 0.496351 | Nuclear surface tension |
| **c₂** | 1/β | 0.328615 | Nuclear volume coefficient |
| **V₄** | -ξ/β | -0.329 | QED vacuum polarization |

---

## Complete Derivation Code (Zero Dependencies)

This is the exact derivation logic using **only Python stdlib** - no numpy, no scipy.
Copy-paste into any Python REPL:

```python
import math

# THE ONLY INPUT: Fine structure constant (CODATA 2018)
ALPHA_INV = 137.035999206
ALPHA = 1.0 / ALPHA_INV

# GOLDEN LOOP SOLVER: 1/α = 2π² × (e^β / β) + 1
def solve_golden_loop():
    """Newton-Raphson solver - no scipy needed."""
    y_target = ALPHA_INV - 1
    const = 2 * (math.pi ** 2)
    beta = 3.0  # Initial guess

    for _ in range(20):
        term = math.exp(beta) / beta
        f_beta = const * term - y_target
        f_prime = const * math.exp(beta) * (beta - 1) / (beta ** 2)
        beta_new = beta - (f_beta / f_prime)
        if abs(beta_new - beta) < 1e-12:
            return beta_new
        beta = beta_new
    return beta

BETA = solve_golden_loop()  # = 3.043233

# DERIVED CONSTANTS (No free parameters)
C1_SURFACE = 0.5 * (1 - ALPHA)  # = 0.496351 (nuclear surface)
C2_VOLUME = 1.0 / BETA          # = 0.328598 (nuclear volume)
V4_QED = -1.0 / BETA            # = -0.328598 (vacuum polarization)

# INDEPENDENT EMPIRICAL VALUES (for comparison)
C1_EMPIRICAL = 0.496297   # NuBase 2020 nuclear mass fits
C2_EMPIRICAL = 0.32704    # NuBase 2020 nuclear mass fits
V4_SCHWINGER = -0.328479  # QED perturbation theory

print(f"β = {BETA:.6f}")
print(f"c₁ error: {abs(C1_SURFACE - C1_EMPIRICAL)/C1_EMPIRICAL*100:.3f}%")
print(f"c₂ error: {abs(C2_VOLUME - C2_EMPIRICAL)/C2_EMPIRICAL*100:.3f}%")
print(f"V₄ error: {abs(V4_QED - V4_SCHWINGER)/abs(V4_SCHWINGER)*100:.2f}%")
```

**Output:**
```
β = 3.043233
c₁ error: 0.011%
c₂ error: 0.476%
V₄ error: 0.04%
```

**Key Point**: The empirical values are from completely independent experiments (nuclear masses, QED calculations). QFD predicts them from α alone with < 0.5% error.

---

## Repository Structure

```
QFD-Universe/
├── README.md              # Human entry point
├── LLM_CONTEXT.md         # THIS FILE - AI assistant guide
├── THEORY.md              # Full theory documentation
├── project_map.txt        # File tree navigation
│
├── formalization/         # Lean4 proofs (DO NOT DELETE)
│   ├── QFD.lean           # Main import
│   └── QFD/               # 200+ proof files
│       ├── GoldenLoop.lean
│       ├── Soliton/HardWall.lean
│       ├── Lepton/FineStructure.lean
│       └── ... (many more)
│
├── simulation/            # Python solvers
│   ├── src/
│   │   └── shared_constants.py  # SINGLE SOURCE OF TRUTH
│   └── scripts/
│
├── analysis/              # Validation scripts
│   ├── src/
│   └── scripts/
│
├── manuscript/            # Documentation
│
├── sync_from_internal.sh  # Sync workflow script
└── sync_to_internal.sh    # Reverse sync (use carefully)
```

---

## Sync Workflow (One-Way: Internal → GitHub)

**Internal development** happens in: `/home/tracy/development/QFD_SpectralGap/`
**Public repo** is at: `/home/tracy/development/QFD-Universe/`

### To update specific Lean files:

```bash
cd /home/tracy/development/QFD-Universe

# 1. Copy ONLY the specific file(s) that changed
cp /home/tracy/development/QFD_SpectralGap/projects/Lean4/QFD/Path/To/File.lean \
   formalization/QFD/Path/To/

# 2. Commit and push
git add formalization/QFD/Path/To/File.lean
git commit -m "feat: Description of what changed"
git push
```

### DO NOT:
- Use `rsync --delete` on the whole directory (brings in unwanted .md files)
- Use `git clean -fd` (deletes untracked files)
- Delete files to "clean up" the repo

### File Mapping (Internal → Public):

| Internal Path | Public Path |
|--------------|-------------|
| `QFD_SpectralGap/projects/Lean4/QFD/` | `QFD-Universe/formalization/QFD/` |
| `QFD_SpectralGap/To_Review_and_Replicate/01_alpha_derivation/` | `QFD-Universe/simulation/scripts/` |
| `QFD_SpectralGap/To_Review_and_Replicate/03_conservation_law/` | `QFD-Universe/analysis/` |

---

## Key Files to Understand

### 1. Constants Bridge (`simulation/src/shared_constants.py`)

**All Python scripts import constants from this single file.**

```python
from shared_constants import ALPHA, BETA, C1_SURFACE, C2_VOLUME
```

This prevents "magic numbers" and shows the derivation chain: α → β → c₁ → c₂

### 2. Golden Loop Proof (`formalization/QFD/GoldenLoop.lean`)

Formal proof that β = 3.04309 satisfies the transcendental equation.

### 3. Key Validations

| Script | What it validates |
|--------|------------------|
| `simulation/scripts/verify_golden_loop.py` | α → β derivation |
| `analysis/scripts/run_all_validations.py` | Conservation law (285/285) |
| `analysis/scripts/validate_g2_corrected.py` | g-2 prediction (0.45% error) |

---

## For AI Assistants: Common Tasks

### "Update the public repo with new Lean proofs"

1. Ask which specific files changed
2. Copy ONLY those files (not the whole directory)
3. Commit with descriptive message
4. Push to GitHub

### "Run validations"

```bash
cd /home/tracy/development/QFD-Universe/simulation/scripts
python verify_golden_loop.py

cd /home/tracy/development/QFD-Universe/analysis/scripts
python run_all_validations.py
```

### "Check what's different between internal and public"

```bash
diff /home/tracy/development/QFD_SpectralGap/projects/Lean4/QFD/Soliton/HardWall.lean \
     /home/tracy/development/QFD-Universe/formalization/QFD/Soliton/HardWall.lean
```

### "Find recently changed Lean files in internal repo"

```bash
cd /home/tracy/development/QFD_SpectralGap
git log --oneline --name-only -5 -- "*.lean"
```

---

## Session Recovery

If you're a new AI session continuing previous work:

1. **Don't assume anything needs cleaning** - the structure is intentional
2. **Read this file first** - it has the context you need
3. **Ask the user** what they want to do before making changes
4. **Check git status** before any commits:
   ```bash
   cd /home/tracy/development/QFD-Universe
   git status
   git log --oneline -5
   ```

---

## What QFD Claims (Summary)

### Validated Results
- ✓ β = 3.04309 derived from α via Golden Loop
- ✓ c₁ = ½(1-α) matches nuclear data to 0.01%
- ✓ Conservation law: 285/285 perfect
- ✓ g-2 coefficient matches QED to 0.45%
- ✓ ℏ emerges from helicity-locked topology

### NOT Claimed
- ✗ All nuclear physics derives from α alone
- ✗ Shell effects fully predicted
- ✗ QFD replaces QCD

---

## Contact

- **Author**: Tracy McSheery
- **Repository**: https://github.com/tracyphasespace/QFD-Universe
- **Issues**: https://github.com/tracyphasespace/QFD-Universe/issues
- **Internal Dev**: `/home/tracy/development/QFD_SpectralGap/`
