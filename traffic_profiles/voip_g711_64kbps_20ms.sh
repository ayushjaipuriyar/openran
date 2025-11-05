#!/bin/bash
# VoIP traffic profile (G.711-like)
# Description: Simulate a VoIP call using UDP at ~64 kbps with 20 ms frame size (~160 bytes payload).
# Typical RTP/UDP headers add small overhead; this uses -l 160 to approximate voice payload size.
# Usage: ./voip_g711_64kbps_20ms.sh <server_ip> [port] [duration_sec]
# Example: ./voip_g711_64kbps_20ms.sh 192.168.1.10 5201 180

SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-180}  # default 3 minutes

# G.711 bitrate ~64k. Use UDP iperf3 with datagram length ~160 bytes to simulate 20ms frames of payload.
iperf3 -c "$SERVER" -p "$PORT" -u -b 64k -l 160 -t "$DURATION"
