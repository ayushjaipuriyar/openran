#!/bin/bash
# VoIP on/off conversation profile - alternating talk/silence periods
# Simulates intermittent speech activity: default 1s on / 1s off pattern aggregated into longer frames
# Usage: ./voip_24kbps_60b_onoff.sh <server_ip> [port] [duration_sec] [on_sec] [off_sec]
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-180}
ON_SEC=${4:-10}
OFF_SEC=${5:-10}

ELAPSED=0
while [ "$ELAPSED" -lt "$DURATION" ]; do
  REMAIN=$((DURATION-ELAPSED))
  # On period (send voice)
  T_ON=$(( ON_SEC < REMAIN ? ON_SEC : REMAIN ))
  if [ "$T_ON" -le 0 ]; then break; fi
  iperf3 -c "$SERVER" -p "$PORT" -u -b 24k -l 60 -t "$T_ON"
  ELAPSED=$((ELAPSED+T_ON))
  if [ "$ELAPSED" -ge "$DURATION" ]; then break; fi
  # Off period (silence): just sleep
  T_OFF=$(( OFF_SEC < (DURATION-ELAPSED) ? OFF_SEC : (DURATION-ELAPSED) ))
  sleep "$T_OFF"
  ELAPSED=$((ELAPSED+T_OFF))
done
