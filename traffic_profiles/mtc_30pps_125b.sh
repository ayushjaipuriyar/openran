#!/bin/bash
# MTC traffic profile (Poisson-like via bandwidth approximation)
# Description: Small packets (125 bytes) at an average of 30 packets/sec per UE.
# We approximate this with iperf3 UDP using the equivalent bandwidth: 30 * 125 * 8 = 30000 bps (30k).
# Usage: ./mtc_30pps_125b.sh <server_ip> [port] [duration_sec]
# Example: ./mtc_30pps_125b.sh 192.168.1.10 5201 480

SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-480}

# iperf3 UDP with small datagram length (-l) and appropriate bandwidth (-b)
iperf3 -c "$SERVER" -p "$PORT" -u -b 30k -l 125 -t "$DURATION"
