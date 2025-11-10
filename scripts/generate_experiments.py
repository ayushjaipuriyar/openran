import os
import shutil
import random
from pathlib import Path
from argparse import ArgumentParser
import sys

sys.path.append("..")
from lib.mmap_generator import MMapGenerator, generate_channel_parameters
from config.config import (
    UE_COUNT,
    EXPERIMENTS_PER_TR,
    TRAFFIC_PROFILE_DIR,
    SCENARIO_SCRIPT,
    DURATION_SEC,
    BENIGN_TRAINING_RUNS,
    BENIGN_OUTPUT_DIR,
)

# === Configuration ===
TOTAL_TRAINING_RUNS = BENIGN_TRAINING_RUNS
OUTPUT_DIR = BENIGN_OUTPUT_DIR


def list_available_profiles():
    """Returns list of all available UE traffic profiles"""
    benign_dir = TRAFFIC_PROFILE_DIR / "benign"
    return sorted(list(benign_dir.glob("**/*.sh"))) if benign_dir.exists() else []


def assign_profiles(generator, available_profiles):
    """Randomly assign a traffic profile to each UE using M-map"""
    assignments = {}
    for i in range(1, UE_COUNT + 1):
        idx = int(generator.next() * len(available_profiles)) % len(available_profiles)
        assignments[f"UE{i}"] = available_profiles[idx]
    return assignments


def create_exp_folder(tr_id, exp_id, g, channel_params, profile_assignments):
    exp_path = OUTPUT_DIR / f"tr{tr_id}" / f"exp{exp_id}"
    exp_path.mkdir(parents=True, exist_ok=True)

    # Save run script
    run_script_path = exp_path / "run_scenario.sh"
    with open(run_script_path, "w") as f:
        f.write("#!/bin/bash\n\n")
        f.write(f"# Run script for tr{tr_id} exp{exp_id}\n")
        f.write(f"# Conditions generated with seed={g.seed} and p={g.p}\n")
        args_str = " ".join(
            [f"--{k.replace('_', '-')} {v}" for k, v in channel_params.items()]
        )
        f.write(f"python3 {SCENARIO_SCRIPT} {args_str} &\n")
        f.write("PYTHON_PID=$!\n")
        f.write("sleep 5\n")
        f.write('echo "GNURADIO PID: $PYTHON_PID"\n')
        f.write("echo $PYTHON_PID > /tmp/python_scenario.pid\n")
    os.chmod(run_script_path, 0o755)

    # Save conditions.csv
    cond_path = exp_path / "conditions.csv"
    with open(cond_path, "w") as f:
        f.write("UE,Profile\n")
        for ue, profile_path in profile_assignments.items():
            f.write(f"{ue},{str(profile_path)}\n")
        f.write("\n# M-map Parameters\n")
        f.write(f"seed,{g.seed}\n")
        f.write(f"p,{g.p}\n")
        f.write("\n# Channel Parameters\n")
        for k, v in channel_params.items():
            f.write(f"{k},{v}\n")

    print(f"  ✅ Created: {exp_path.relative_to(OUTPUT_DIR)}")


def main():
    parser = ArgumentParser(
        description="Generate training experiments using M-map and Iperf profiles"
    )
    parser.add_argument(
        "--seed",
        type=float,
        default=None,
        help="Base seed for M-map generator. If not set, a random seed is used for each run.",
    )
    parser.add_argument(
        "--p",
        type=float,
        default=None,
        help="M-map parameter (0.25 to 0.5). If not set, a random p is used for each run.",
    )
    args = parser.parse_args()

    available_profiles = list_available_profiles()
    if not available_profiles:
        print(f"Error: No Iperf profiles found in {TRAFFIC_PROFILE_DIR}")
        return

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    for tr in range(TOTAL_TRAINING_RUNS):
        # Determine the seed for this training run.
        tr_seed = (args.seed + tr) if args.seed is not None else None

        # Create a single generator for this entire training run.
        g = MMapGenerator(tr_seed, p=args.p)

        # Generate all conditions for this run.
        channel_params = generate_channel_parameters(g)
        profile_assignments = assign_profiles(g, available_profiles)

        print(f"\nTR{tr}: Generating experiments with seed={g.seed:.4f}, p={g.p:.4f}")

        for exp in range(1, EXPERIMENTS_PER_TR + 1):
            create_exp_folder(tr, exp, g, channel_params, profile_assignments)

    print(f"\n🎯 All experiments generated in: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
