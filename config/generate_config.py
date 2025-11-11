from pathlib import Path

# Small focused config used by the experiment generation scripts
PROJECT_ROOT = Path(__file__).parent.parent

# Number of UEs per experiment
UE_COUNT = 3

# Experiments per training run
EXPERIMENTS_PER_TR = 1

# Directory where traffic profiles live (benign/ malicious subdirs)
TRAFFIC_PROFILE_DIR = PROJECT_ROOT / "traffic_profiles"

# Path to the no-gui GNU Radio scenario script
SCENARIO_SCRIPT = PROJECT_ROOT / "lib" / "multi_ue_scenario_nogui.py"

# Per-experiment duration in seconds
DURATION_SEC = 480

# How many training runs to generate (separate values for benign/malicious)
TRAINING_RUNS = 100
BENIGN_TRAINING_RUNS = TRAINING_RUNS
MALICIOUS_TRAINING_RUNS = TRAINING_RUNS

# Output directories for generated experiments
BENIGN_OUTPUT_DIR = PROJECT_ROOT / "generated_experiments"
MALICIOUS_OUTPUT_DIR = PROJECT_ROOT / "generated_malicious_experiments"
