#!/bin/bash
# URLLC profile B - 10 kbps, 125-byte packets (variant)
# Slightly different defaults (shorter duration) for variety
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-120}
iperf3 -c "$SERVER" -p "$PORT" -u -b 10k -l 125 -t "$DURATION"
