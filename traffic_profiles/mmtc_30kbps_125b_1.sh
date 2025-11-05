#!/bin/bash
# mMTC profile A - 30 kbps, 125-byte packets
# Usage: ./mmtc_30kbps_125b_1.sh <server_ip> [port] [duration_sec]
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-300}
iperf3 -c "$SERVER" -p "$PORT" -u -b 30k -l 125 -t "$DURATION"
