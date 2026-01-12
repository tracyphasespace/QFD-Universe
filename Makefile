# QFD-Universe Makefile
# Convenience commands for development and validation

.PHONY: help install install-dev validate validate-quick lean lean-check clean docs

# Default target
help:
	@echo "QFD-Universe Development Commands"
	@echo "================================="
	@echo ""
	@echo "Installation:"
	@echo "  make install      Install core dependencies"
	@echo "  make install-dev  Install with development tools"
	@echo "  make install-all  Install everything (dev + docs)"
	@echo ""
	@echo "Validation:"
	@echo "  make validate       Run all 17 validation tests"
	@echo "  make validate-quick Run validations in quick mode"
	@echo "  make golden-loop    Verify Golden Loop equation"
	@echo ""
	@echo "Lean Proofs:"
	@echo "  make lean           Build all Lean proofs"
	@echo "  make lean-check     Check for remaining sorries"
	@echo ""
	@echo "Other:"
	@echo "  make docs           Generate documentation index"
	@echo "  make clean          Remove build artifacts"
	@echo "  make viz            Generate 3D visualization"

# Installation targets
install:
	pip install -r requirements.txt

install-dev:
	pip install -e ".[dev]"

install-all:
	pip install -e ".[all]"

# Validation targets
validate:
	cd analysis/scripts && python run_all_validations.py

validate-quick:
	cd analysis/scripts && python run_all_validations.py --quick

validate-data:
	cd analysis/scripts && python run_all_validations.py --require-data

golden-loop:
	@python -c "\
import numpy as np; \
beta = 3.043233053; \
alpha_inv = 137.035999084; \
lhs = 2 * np.pi**2 * (np.exp(beta) / beta) + 1; \
error = abs(lhs - alpha_inv) / alpha_inv; \
print(f'Golden Loop: 2pi^2(e^beta/beta) + 1 = {lhs:.9f}'); \
print(f'Target: 1/alpha = {alpha_inv}'); \
print(f'Relative error: {error:.2e}'); \
assert error < 1e-9, f'Error too large: {error}'; \
print('SUCCESS: Golden Loop equation verified')"

# Lean targets
lean:
	cd formalization && lake build QFD

lean-update:
	cd formalization && lake update && lake build QFD

lean-check:
	@echo "Checking for remaining sorries in Lean proofs..."
	@grep -r "sorry" formalization/QFD --include="*.lean" | grep -v ".lake" || echo "No sorries found!"
	@echo ""
	@echo "Sorry count:"
	@grep -r "sorry" formalization/QFD --include="*.lean" | grep -v ".lake" | wc -l

# Documentation
docs:
	python docs/generate_index.py

# Visualization
viz:
	python visualizations/nucleus_3d_interactive.py
	@echo "Generated: visualizations/nucleus_resonance.html"

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ 2>/dev/null || true
	@echo "Cleaned build artifacts"

# Lean cleanup (use with caution - rebuilds take time)
lean-clean:
	cd formalization && rm -rf .lake/build
	@echo "Cleaned Lean build cache (lake build will recompile)"
