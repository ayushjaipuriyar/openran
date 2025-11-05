#!/bin/bash
# URLLC traffic profile (Poisson-like via bandwidth approximation)
# Description: Small packets (125 bytes) at an average of 10 packets/sec per UE.
# Equivalent bandwidth: 10 * 125 * 8 = 10000 bps (10k).
# Usage: ./urllc_10pps_125b.sh <server_ip> [port] [duration_sec]
# Example: ./urllc_10pps_125b.sh 192.168.1.10 5201 480

SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-480}

iperf3 -c "$SERVER" -p "$PORT" -u -b 10k -l 125 -t "$DURATION"
