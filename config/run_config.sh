#!/usr/bin/env bash
# Runtime configuration exported for bash run scripts (run_benign.sh / run_malicious.sh)

# Resolve project root (directory above this config folder)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

export CSV_FILE="$PROJECT_ROOT/dataset/ue_data.csv"
export GNB_CONF="$PROJECT_ROOT/config/gnb_zmq.yaml"
export UE_CONF="$PROJECT_ROOT/config/ue_zmq.conf"

export METRICS_IP="127.0.0.1"
export RIC_IP="127.0.0.1"
export AMF_IP="10.53.1.2"
export BASE_IP="10.45.1.2"

# Experiment counts used by the run scripts
export TOTAL_TRAINING_SETS=100
export TOTAL_EXPERIMENTS=1

# Timeouts and retry settings
export EXPECTED_DURATION_SEC=480
export MAX_RETRIES=3
export RETRY_DELAY=10
export TIMEOUT_GNURADIO=10
export TIMEOUT_UE_CONNECTION=10
export TIMEOUT_SERVICE_READY=10
export HEALTH_CHECK_INTERVAL=5
export METRICS_503_CHECK_TIMEOUT=10

export EXPERIMENT_STATE_FILE="/tmp/experiment_state.json"
export LOG_DIR="$PROJECT_ROOT/logs"
# Output directories
export BENIGN_OUTPUT_DIR="$PROJECT_ROOT/generated_experiments"
export MALICIOUS_OUTPUT_DIR="$PROJECT_ROOT/generated_malicious_experiments"

unset PROJECT_ROOT
