#!/bin/bash
# VoIP continuous profile - 24 kbps, 60-byte payloads
# Usage: ./voip_24kbps_60b_continuous.sh <server_ip> [port] [duration_sec]
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-180}
iperf3 -c "$SERVER" -p "$PORT" -u -b 24k -l 60 -t "$DURATION"
