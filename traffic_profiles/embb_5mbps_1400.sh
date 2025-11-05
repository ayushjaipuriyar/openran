#!/bin/bash
# eMBB profile - high (5 Mbps)
# UDP constant bitrate with 1400-byte datagrams
# Usage: ./embb_5mbps_1400.sh <server_ip> [port] [duration_sec]
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-480}
iperf3 -c "$SERVER" -p "$PORT" -u -b 5M -l 1400 -t "$DURATION"
