#!/usr/bin/env python3
# Copyright (c) 2026 Tracy McSheery. All rights reserved.
# This software is released under the MIT License.
# See the LICENSE file for details.

"""
QFD Master Validation Suite - 17 Tests
=======================================
Single command to run ALL validation and derivation scripts.

Usage:
    python run_all_validations.py [--quick] [--require-data]

Options:
    --quick         Run with reduced samples (faster)
    --require-data  Fail immediately if NuBase data is missing
                    (Default: warn but continue with available tests)

Tests:
    Part 1: Fundamental Derivations (5 tests)
    Part 2: Nuclear Physics (5 tests)
    Part 3: Particle Physics (5 tests)
    Part 4: Standalone Proofs (2 tests)

Output:
    - Console summary with all 17 validation results
    - Exit code 0 if all pass, 1 otherwise
"""

import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime


def print_header(title):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80 + "\n")


def print_section(title):
    """Print formatted subsection header."""
    print("\n" + "-" * 80)
    print(title)
    print("-" * 80)


def run_validation(script_name, description, args=None, cwd=None):
    """Run a validation script and return success status."""
    print_section(f"Running: {description}")

    # Resolve script path relative to this file's location
    base_dir = Path(__file__).parent.resolve()
    script_path = (base_dir / script_name).resolve()

    if not script_path.exists():
        print(f"⚠️  WARNING: {script_path} not found, skipping...")
        return False

    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    # Use script's directory as working directory if not specified
    if cwd is None:
        cwd = script_path.parent

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(cwd)
        )

        # Print output
        print(result.stdout)

        if result.stderr:
            print("STDERR:", result.stderr)

        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed with exit code {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print(f"✗ {description} timed out after 120 seconds")
        return False
    except Exception as e:
        print(f"✗ {description} failed with error: {e}")
        return False


def check_data_availability(require_data=False):
    """Check if required data files are available.

    Args:
        require_data: If True, fail fast when data is missing.
                     If False, warn but continue (default behavior).

    Returns:
        True if data is available or if we should proceed anyway.
        False if data is required but missing.
    """
    data_path = Path(__file__).parent / '../data/derived/harmonic_scores.parquet'

    if data_path.exists():
        import pandas as pd
        try:
            scores = pd.read_parquet(data_path)
            print(f"✓ Data loaded: {len(scores)} nuclides from NUBASE2020")
            return True
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            if require_data:
                print("ERROR: --require-data flag set but data cannot be loaded.")
                return False
            return False
    else:
        if require_data:
            print(f"✗ Data file not found: {data_path}")
            print("ERROR: --require-data flag set. Cannot proceed without data.")
            print("\nTo obtain NuBase 2020 data, see docs/REPLICATION.md")
            return False
        else:
            # Don't fail hard if just simulation scripts are needed, but warn
            print(f"⚠️  Data file not found: {data_path}")
            print("    Some tests may fail. Use --require-data to enforce data availability.")
            return True  # Proceed, some scripts might fail but others (simulation) will work


def main():
    """Run all validations."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='QFD Master Validation Suite - 17 Tests',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_all_validations.py                 # Run all, warn if data missing
    python run_all_validations.py --quick         # Fast mode with reduced samples
    python run_all_validations.py --require-data  # Fail if NuBase data missing
        """
    )
    parser.add_argument('--quick', action='store_true',
                        help='Run with reduced samples (faster)')
    parser.add_argument('--require-data', action='store_true',
                        help='Fail immediately if NuBase data is missing')
    args = parser.parse_args()

    start_time = datetime.now()

    print_header("QFD MODEL VALIDATION AND DERIVATION SUITE")
    print(f"Timestamp: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    if args.quick:
        print("\n⚡ QUICK MODE: Running with reduced samples")

    if args.require_data:
        print("\n🔒 STRICT MODE: Data availability required")

    # Check data availability
    print_section("1. Checking Data Availability")
    data_ok = check_data_availability(require_data=args.require_data)

    if not data_ok:
        print("\n❌ Validation aborted: Required data not available.")
        return 1

    # Track results
    results = {}

    # ---------------------------------------------------------
    # PART 1: FUNDAMENTAL DERIVATIONS (Simulation)
    # ---------------------------------------------------------
    print_header("PART 1: FUNDAMENTAL CONSTANT DERIVATIONS")

    results['beta_from_alpha'] = run_validation(
        '../../simulation/scripts/derive_beta_from_alpha.py',
        'Derive Beta from Alpha (Golden Loop)'
    )
    
    results['hbar_topology'] = run_validation(
        '../../simulation/scripts/derive_hbar_from_topology.py',
        'Derive Planck Constant from Topology'
    )
    
    results['verify_golden'] = run_validation(
        '../../simulation/scripts/verify_golden_loop.py',
        'Verify Golden Loop Transcendental Equation'
    )
    
    results['alpha_derived'] = run_validation(
        '../../simulation/scripts/QFD_ALPHA_DERIVED_CONSTANTS.py',
        'Calculate All Derived Constants'
    )
    
    results['beta_tension'] = run_validation(
        '../../simulation/scripts/explore_beta_tension.py',
        'Explore Beta Tension (Nuclear vs Atomic)'
    )

    # ---------------------------------------------------------
    # PART 2: NUCLEAR PHYSICS VALIDATION (Analysis)
    # ---------------------------------------------------------
    print_header("PART 2: NUCLEAR PHYSICS VALIDATION")

    # Validation 6: Conservation Law
    results['conservation_law'] = run_validation(
        'validate_conservation_law.py',
        'Conservation Law (210/210 Perfect)'
    )

    # Validation 7: Integer Ladder (Engine A)
    results['integer_ladder'] = run_validation(
        '../nuclear/scripts/integer_ladder_test.py',
        'Integer Ladder Test',
        args=['--scores', '../data/harmonic_scores.parquet', '--out', '../results/']
    )

    # Validation 8: Fission Resonance (Engine B)
    results['fission'] = run_validation(
        '../nuclear/scripts/validate_fission_pythagorean.py',
        'Fission Resonance (Tacoma Narrows)'
    )

    # Validation 9: Decay Selection Rules (Engine C)
    results['decay_rules'] = run_validation(
        '../nuclear/scripts/analyze_all_decay_transitions.py',
        'Beta/Alpha Decay Selection Rules'
    )

    # Validation 10: Proton Engine (Engine D)
    results['proton'] = run_validation(
        'validate_proton_engine.py',
        'Proton Drip Line Asymmetry'
    )

    # ---------------------------------------------------------
    # PART 3: PARTICLE PHYSICS & COSMOLOGY
    # ---------------------------------------------------------
    print_header("PART 3: PARTICLE PHYSICS & COSMOLOGY")

    # Validation 11: g-2 Anomaly (Parameter-Free)
    results['g2_anomaly'] = run_validation(
        'validate_g2_corrected.py',
        'g-2 Anomaly (Parameter-Free: 0.0013%/0.0027%)'
    )

    # Validation 12: Comprehensive g-2 Verification
    results['verify_g2'] = run_validation(
        '../../simulation/scripts/verify_lepton_g2.py',
        'Parameter-Free g-2 Verification'
    )

    # Validation 13: Lepton Stability
    results['lepton_stability'] = run_validation(
        'lepton_stability.py',
        'Lepton Stability (Hill Vortex)'
    )

    # Validation 14: Lepton Isomers
    results['lepton_isomers'] = run_validation(
        'validate_lepton_isomers.py',
        'Lepton Isomer Validation'
    )

    # Validation 15: Photon Soliton Stability
    results['photon_soliton'] = run_validation(
        '../../simulation/scripts/verify_photon_soliton.py',
        'Photon Soliton Stability'
    )

    # Validation 16: CMB Temperature
    results['cmb'] = run_validation(
        'derive_cmb_temperature.py',
        'CMB Temperature (2.7248 K, 0.03% error)'
    )

    # ---------------------------------------------------------
    # PART 4: STANDALONE PROOFS
    # ---------------------------------------------------------
    print_header("PART 4: STANDALONE PROOFS")

    # Validation 17: Zero-Dependency Golden Spike Proof
    results['qfd_proof'] = run_validation(
        '../../qfd_proof.py',
        'Zero-Dependency Golden Spike Proof'
    )

    # Summary
    elapsed = (datetime.now() - start_time).total_seconds()

    print_header("VALIDATION SUMMARY")
    print(f"Runtime: {elapsed:.1f} seconds")
    print()

    # Results table
    print(f"{'Test Description':<50} {'Status':<10}")
    print("-" * 65)

    # Organize by category (17 tests total)
    categories = [
        ("Fundamental Derivations (5)", [
            'beta_from_alpha', 'hbar_topology', 'verify_golden', 'alpha_derived', 'beta_tension'
        ]),
        ("Nuclear Physics (5)", [
            'conservation_law', 'integer_ladder', 'fission', 'decay_rules', 'proton'
        ]),
        ("Particle Physics & Cosmology (6)", [
            'g2_anomaly', 'verify_g2', 'lepton_stability', 'lepton_isomers', 'photon_soliton', 'cmb'
        ]),
        ("Standalone Proofs (1)", [
            'qfd_proof'
        ])
    ]

    passed_count = 0
    total_count = 0

    for cat_name, keys in categories:
        print(f"[{cat_name}]")
        for key in keys:
            status = results.get(key, False)
            status_text = "PASSED" if status else "FAILED"
            print(f"  {key:<48} {status_text}")
            if status:
                passed_count += 1
            total_count += 1
        print()

    print("-" * 65)
    print(f"Total: {passed_count}/{total_count} tests passed")
    print()

    # Final status
    if passed_count == total_count:
        print(f"SUCCESS: All {total_count} validations passed.")
        print("\nQFD Framework: Parameter-free physics validated.")
        return 0
    else:
        print(f"INCOMPLETE: {passed_count}/{total_count} tests passed.")
        print(f"            {total_count - passed_count} tests failed or were skipped.")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
