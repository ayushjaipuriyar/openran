#!/bin/bash
# eMBB traffic profile (constant bitrate)
# Description: Constant UDP bitrate of 4 Mbps per UE. Intended to simulate continuous high-throughput traffic (e.g., HD video).
# Usage: ./embb_4mbps.sh <server_ip> [port] [duration_sec]
# Example: ./embb_4mbps.sh 192.168.1.10 5201 480

SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-480}  # default 8 minutes

# iperf3 UDP with fixed bandwidth. -l sets datagram size (payload) — keep reasonably large to reduce overhead.
iperf3 -c "$SERVER" -p "$PORT" -u -b 4M -l 1200 -t "$DURATION"
