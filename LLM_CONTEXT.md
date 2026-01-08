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
