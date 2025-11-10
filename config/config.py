# Common configuration for experiment generation
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

UE_COUNT = 3
EXPERIMENTS_PER_TR = 1
TRAFFIC_PROFILE_DIR = PROJECT_ROOT / "traffic_profiles"
SCENARIO_SCRIPT = PROJECT_ROOT / "lib" / "multi_ue_scenario_nogui.py"
DURATION_SEC = 480  # 8 minutes

# Experiment counts
CSV_FILE = PROJECT_ROOT / "dataset" / "ue_data.csv"
GNB_CONF = PROJECT_ROOT / "config" / "gnb_zmq.yaml"
UE_CONF = PROJECT_ROOT / "config" / "ue_zmq.conf"
METRICS_IP = "127.0.0.1"
RIC_IP = "127.0.0.1"
AMF_IP = "10.53.1.2"
BASE_IP = "10.45.1.2"
TRAINING_RUNS = 100
MAX_RETRIES = 3
RETRY_DELAY = 10
TIMEOUT_GNURADIO = 10
TIMEOUT_UE_CONNECTION = 10
TIMEOUT_SERVICE_READY = 10
HEALTH_CHECK_INTERVAL = 5
METRICS_503_CHECK_TIMEOUT = 10
EXPERIMENT_STATE_FILE = "/tmp/experiment_state.json"

# Training set counts (for backward compatibility with scripts)
TOTAL_TRAINING_SETS = TRAINING_RUNS
BENIGN_TRAINING_RUNS = TRAINING_RUNS  # Use same value as TRAINING_RUNS
MALICIOUS_TRAINING_RUNS = TRAINING_RUNS  # Use same value as TRAINING_RUNS

# Output directories
BENIGN_OUTPUT_DIR = PROJECT_ROOT / "generated_experiments"
MALICIOUS_OUTPUT_DIR = PROJECT_ROOT / "generated_malicious_experiments"

# Expected experiment duration (seconds)
EXPECTED_DURATION_SEC = DURATION_SEC
