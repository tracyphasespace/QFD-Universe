#!/bin/bash
# sync_to_internal.sh - Push external contributions back to internal repo
#
# Copyright (c) 2026 Tracy McSheery
#
# Usage: ./sync_to_internal.sh
#
# Use this after accepting PRs or external contributions

set -e

INTERNAL="/home/tracy/development/QFD_SpectralGap"
PUBLIC="/home/tracy/development/QFD-Universe"

echo "=== Syncing TO internal repo ==="
echo "WARNING: This will overwrite internal files with public versions"
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Pull latest from GitHub first
cd "$PUBLIC"
git pull

# 1. Lean4 proofs
echo "Syncing Lean4 proofs to internal..."
rsync -av --delete \
    "$PUBLIC/formalization/QFD/" \
    "$INTERNAL/projects/Lean4/QFD/"

# 2. Update To_Review_and_Replicate (the staging area)
echo "Syncing Python to internal staging..."

# Alpha derivation
cp "$PUBLIC/simulation/scripts/QFD_ALPHA_DERIVED_CONSTANTS.py" "$INTERNAL/To_Review_and_Replicate/01_alpha_derivation/" 2>/dev/null || true
cp "$PUBLIC/simulation/scripts/derive_beta_from_alpha.py" "$INTERNAL/To_Review_and_Replicate/01_alpha_derivation/" 2>/dev/null || true

# Conservation law
cp "$PUBLIC/analysis/scripts/run_all_validations.py" "$INTERNAL/To_Review_and_Replicate/03_conservation_law/" 2>/dev/null || true
cp "$PUBLIC/analysis/src/"*.py "$INTERNAL/To_Review_and_Replicate/03_conservation_law/src/" 2>/dev/null || true

# g-2
cp "$PUBLIC/analysis/scripts/validate_g2_corrected.py" "$INTERNAL/To_Review_and_Replicate/06_g2_anomaly/" 2>/dev/null || true

# Astrophysics
cp "$PUBLIC/analysis/scripts/compare_models.py" "$INTERNAL/To_Review_and_Replicate/09_astrophysics/" 2>/dev/null || true

echo "=== Sync to internal complete ==="
echo ""
echo "Changes are in $INTERNAL/To_Review_and_Replicate/"
echo "Review and merge manually into main development files as needed."
