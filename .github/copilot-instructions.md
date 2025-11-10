# O-RAN Malicious UE Detection - AI Coding Guidelines

## Project Overview

This is an end-to-end O-RAN (Open Radio Access Network) framework for detecting malicious UE (User Equipment) behavior using machine learning in a Near-RT RIC (Real-time RAN Intelligent Controller). The system generates realistic 4G/5G RAN experiments, collects E2SM-KPM Style 5 metrics, performs temporal feature engineering, and runs cascaded ML inference.

## Architecture & Key Components

### Core xApps (`openran/oran-sc-ric/xApps/python/lib/`)

- **`kpm5_xapp.py`**: Collects E2SM-KPM Style 5 metrics, writes wide CSV per UE per indication
- **`detector_xapp.py`**: Buffers metrics, engineers temporal features, runs cascaded Stage 1 (binary) → Stage 2 (subtype) ML detection
- **`xAppBase.py`**: RMR threading abstraction for HTTP subscriptions and E2 indications

### Experiment Orchestration

- **`run_enhanced.sh`**: Master orchestrator managing RIC, core, gNB, UEs, GNU Radio, traffic generation with retries and health checks
- **`generate_experiments.py`**: Creates benign experiment folders with M-map stochastic traffic assignment
- **`generate_malicious_experiments.py`**: Injects malicious traffic profiles (UDP floods, fragmentation, pulsing attacks)

### Traffic & Channel Modeling

- **Traffic Profiles** (`traffic_profiles/`): iperf3 scripts for eMBB/MTC/URLLC/VoIP patterns plus malicious variants
- **GNU Radio Scenarios** (`multi_ue_scenario.grc`): RF channel impairment modeling with SNR, delay, path loss, Doppler
- **M-map Generator** (`lib/mmap_generator.py`): Pseudo-random but controllable sequence generation for reproducible experiments

## Critical Developer Workflows

### Starting the Full Stack

```bash
# 1. Start Near-RT RIC (Docker Compose)
cd openran/oran-sc-ric && docker compose up -d

# 2. Start Open5GS core network
cd openran/srsRAN_Project/docker && docker compose up -d

# 3. Start gNB with extensive logging
sudo gnb -c config/gnb_zmq.yaml --metrics_addr 127.0.0.1 --metrics_port 55555

# 4. Create UE network namespaces and start srsUE instances
sudo ip netns add ue1 && sudo srsue config/ue_zmq.conf --gw.netns ue1

# 5. Launch GNU Radio channel scenario
python3 multi_ue_scenario_nogui.py --snr-db 20 --delay-ms 5

# 6. Generate and run traffic
python3 generate_experiments.py  # Creates experiment folders
bash run_enhanced.sh 0 1        # Run training set 0, experiment 1
```

### Running xApps

```bash
# KPM metrics collector
docker compose exec python_xapp_runner ./kpm5_xapp.py --ue_ids 0,1,2

# Malicious detector with cascaded models
docker compose exec python_xapp_runner ./detector_xapp.py \
  --s1_model_path s1_model.joblib \
  --s2_ben_path s2_benign_model.joblib \
  --s2_mal_path s2_malicious_model.joblib \
  --buffer_size 60
```

## Project-Specific Patterns & Conventions

### E2SM-KPM Style 5 Metrics Processing

Raw metrics collected per UE per indication:

```
RRU.PrbAvailDl/Ul, RRU.PrbUsedDl/Ul, RACH.PreambleDedCell,
DRB.UEThpDl/Ul, DRB.RlcPacketDropRateDl, DRB.RlcSduTransmittedVolumeDL/UL,
CQI, RSRP, RSRQ, DRB.RlcDelayDl/Ul
```

**Feature Engineering Pattern** (see `detector_xapp.py`):

- Rolling window aggregations (mean/std) over 5 samples
- Derived ratios: `prb_utilization_dl = PrbUsedDl / PrbAvailDl`
- Signal composites: `signal_index = (CQI + RSRP + RSRQ) / 3`
- Jitter metrics: `rlc_delay_jitter = diff(rolling_mean(RlcDelayDl))`
- Zero-activity flags and imbalance ratios

### Cascaded ML Detection Pipeline

```python
# Stage 1: Binary classification (malicious vs benign)
stage1_pred = s1_model.predict_proba(features)[:, 1] > threshold

# Stage 2: Subtype classification (conditional on Stage 1)
if stage1_pred:
    subtype_pred = s2_malicious_model.predict(features)
else:
    subtype_pred = s2_benign_model.predict(features)
```

### Experiment Folder Structure

Each experiment (`generated_experiments/tr0/exp1/`) contains:

```
conditions.csv     # UE ↔ traffic profile mappings + channel params
run_scenario.sh    # GNU Radio launcher with PID tracking
metrics/           # KPM CSV outputs
ue_logs/           # Per-UE srsUE logs, pcaps, metrics
gnb_logs/          # gNB logs, extensive protocol pcaps
```

### Network Namespace Management

```bash
# Create UE network namespaces
for i in {1..3}; do sudo ip netns add ue$i; done

# Configure routing for UE traffic
sudo ip route add 10.45.0.0/16 via 10.53.1.2

# Run commands in UE namespace
sudo ip netns exec ue1 iperf3 -c 10.53.1.2 -u -b 3M
```

## Integration Points & Dependencies

### Docker Compose Services

- **RIC Stack**: `ric_submgr`, `python_xapp_runner` (E2/RMR messaging)
- **Core Network**: `open5gs_5gc` (health checks, iperf servers)
- **Process Management**: tmux sessions for gNB/UE isolation

### External Service Coordination

- **Port Management**: ZMQ ports (2000-2301), metrics (55555), iperf (5201-5203)
- **Health Checks**: Docker health status, E2/N2 connection logs, UE RRC/PDU establishment
- **Cleanup**: Process killing, namespace deletion, route removal, temp file cleanup

### Model Artifacts

Models loaded as `.joblib` files supporting:

- PyTorch `nn.Module` with `.predict()` method
- sklearn-compatible estimators
- Feature alignment via `self.selected_features` ordering

## Common Development Tasks

### Adding New Traffic Profiles

1. Create iperf3 script in `traffic_profiles/benign/` or `malicious/`
2. Update experiment generators to include new profile
3. Test with single UE: `sudo ip netns exec ue1 ./new_profile.sh`

### Extending Feature Engineering

1. Add computation in `_feature_engineer_network_data()`
2. Include in rolling window aggregations if temporal
3. Update `self.selected_features` list for model compatibility
4. Retrain models with new feature signature

### Debugging RIC Communications

- Check RMR logs: `docker logs ric_submgr | grep "RMR is ready"`
- Verify E2 connections: `docker logs ric_submgr | grep "E2 connection"`
- Monitor xApp subscriptions: Check HTTP callback logs

### Troubleshooting Experiments

- **UE Connection Issues**: Check N2/E2 logs, verify AMF IP routing
- **Metrics Gaps**: Monitor 503 errors, check buffer sizes, validate timestamps
- **Channel Problems**: Verify GNU Radio PID, check ZMQ port availability
- **Traffic Failures**: Confirm iperf servers running in core container

## Key Files & Directories

- `run_enhanced.sh`: Master orchestration script with retry logic
- `config/config.py`: Experiment parameters and path constants
- `lib/mmap_generator.py`: Stochastic assignment generator
- `traffic_profiles/`: iperf3 traffic pattern definitions
- `generated_experiments/`: Output experiment folders
- `openran/oran-sc-ric/xApps/python/lib/`: xApp implementations

## Quality Assurance

- Validate experiment duration (480s ±10s) via metrics timestamps
- Check for 503 errors in metrics collection logs
- Verify UE RRC/PDU establishment in srsUE logs
- Confirm E2/N2 connections in gNB logs
- Test cascaded model predictions with known traffic patterns
