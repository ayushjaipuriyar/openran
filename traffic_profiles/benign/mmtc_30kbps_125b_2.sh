#!/bin/bash
# mMTC profile B - 30 kbps, 125-byte packets (variant)
SERVER=${1:-127.0.0.1}
PORT=${2:-5201}
DURATION=${3:-120}
iperf3 -c "$SERVER" -p "$PORT" -u -b 30k -l 125 -t "$DURATION"
