#!/usr/bin/env python3
"""
Export config values as environment variables for bash scripts
"""
import sys
import os

# Add the config directory to path
config_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, config_dir)

# Import config module directly
import config

# Export all config values as environment variables
print(f"export TOTAL_TRAINING_SETS={config.TOTAL_TRAINING_SETS}")
print(f"export TOTAL_EXPERIMENTS={config.TOTAL_EXPERIMENTS}")
print(f"export MAX_RETRIES={config.MAX_RETRIES}")
print(f"export RETRY_DELAY={config.RETRY_DELAY}")
print(f"export TIMEOUT_UE_CONNECTION={config.TIMEOUT_UE_CONNECTION}")
print(f"export TIMEOUT_SERVICE_READY={config.TIMEOUT_SERVICE_READY}")
print(f"export HEALTH_CHECK_INTERVAL={config.HEALTH_CHECK_INTERVAL}")
print(f"export METRICS_503_CHECK_TIMEOUT={config.METRICS_503_CHECK_TIMEOUT}")
print(f"export EXPECTED_DURATION_SEC={config.EXPECTED_DURATION_SEC}")
print(f"export CSV_FILE=\"{config.CSV_FILE}\"")
print(f"export GNB_CONF=\"{config.GNB_CONF}\"")
print(f"export UE_CONF=\"{config.UE_CONF}\"")
print(f"export METRICS_IP=\"{config.METRICS_IP}\"")
print(f"export RIC_IP=\"{config.RIC_IP}\"")
print(f"export AMF_IP=\"{config.AMF_IP}\"")
print(f"export BASE_IP=\"{config.BASE_IP}\"")
print(f"export EXPERIMENT_STATE_FILE=\"{config.EXPERIMENT_STATE_FILE}\"")
print(f"export BENIGN_OUTPUT_DIR=\"{config.BENIGN_OUTPUT_DIR}\"")
print(f"export MALICIOUS_OUTPUT_DIR=\"{config.MALICIOUS_OUTPUT_DIR}\"")
