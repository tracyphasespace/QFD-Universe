#!/bin/bash
# sync_from_internal.sh - Pull updates from internal QFD_SpectralGap repo
#
# Copyright (c) 2026 Tracy McSheery
#
# Usage: ./sync_from_internal.sh [commit message]

set -e

INTERNAL="/home/tracy/development/QFD_SpectralGap"
PUBLIC="/home/tracy/development/QFD-Universe"

echo "=== Syncing from internal repo ==="

# 1. Lean4 proofs (formalization/)
echo "Syncing Lean4 proofs..."
rsync -av --delete \
    "$INTERNAL/projects/Lean4/QFD/" \
    "$PUBLIC/formalization/QFD/"
cp "$INTERNAL/projects/Lean4/QFD.lean" "$PUBLIC/formalization/" 2>/dev/null || true
cp "$INTERNAL/projects/Lean4/lakefile.toml" "$PUBLIC/formalization/" 2>/dev/null || true
cp "$INTERNAL/projects/Lean4/lean-toolchain" "$PUBLIC/formalization/" 2>/dev/null || true

# 2. Key Python scripts (simulation/ and analysis/)
echo "Syncing Python scripts..."

# Alpha derivation
cp "$INTERNAL/To_Review_and_Replicate/01_alpha_derivation/"*.py "$PUBLIC/simulation/scripts/" 2>/dev/null || true

# hbar from topology
cp "$INTERNAL/To_Review_and_Replicate/04_hbar_from_topology/"*.py "$PUBLIC/simulation/scripts/" 2>/dev/null || true

# Nuclear predictions
cp "$INTERNAL/To_Review_and_Replicate/02_nuclear_predictions/"*.py "$PUBLIC/analysis/scripts/" 2>/dev/null || true

# Conservation law
cp "$INTERNAL/To_Review_and_Replicate/03_conservation_law/run_all_validations.py" "$PUBLIC/analysis/scripts/" 2>/dev/null || true
cp "$INTERNAL/To_Review_and_Replicate/03_conservation_law/src/"*.py "$PUBLIC/analysis/src/" 2>/dev/null || true

# g-2 and leptons
cp "$INTERNAL/To_Review_and_Replicate/06_g2_anomaly/"*.py "$PUBLIC/analysis/scripts/" 2>/dev/null || true
cp "$INTERNAL/To_Review_and_Replicate/07_lepton_isomers/"*.py "$PUBLIC/analysis/scripts/" 2>/dev/null || true

# Astrophysics
cp "$INTERNAL/To_Review_and_Replicate/09_astrophysics/"*.py "$PUBLIC/analysis/scripts/" 2>/dev/null || true

# 3. Visualization
cp "$INTERNAL/To_Review_and_Replicate/05_visualization/"*.html "$PUBLIC/manuscript/figures/" 2>/dev/null || true

echo "=== Sync complete ==="

# Show what changed
cd "$PUBLIC"
git status --short

# Prompt for commit
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    read -p "Commit and push? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        MSG="${1:-Sync from internal development}"
        git add -A
        git commit -m "$MSG

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
        git push
        echo "=== Pushed to GitHub ==="
    fi
else
    echo "No changes to sync."
fi
