# traffic_profiles

This directory now contains two subfolders, `benign/` and `malicious/`, which hold iperf3-based traffic profile scripts used by the experiment generator.

Each profile is a small shell script that invokes `iperf3` (client mode) and accepts the server IP as the first argument, optional port as the second (default 5201), and optional duration in seconds as the third argument. Scripts in `benign/` model normal slice traffic. Scripts in `malicious/` model attack traffic for testing detection and resilience.

Benign profiles (examples):

- `benign/embb_3mbps_1400.sh`, `benign/embb_4mbps.sh`, `benign/embb_5mbps_1400.sh` — eMBB constant UDP bitrates (3/4/5 Mbps)
- `benign/urllc_10kbps_125b_1.sh`, `benign/urllc_10kbps_125b_2.sh` — URLLC small-packet low-rate profiles (10 kbps)
- `benign/mmtc_30kbps_125b_1.sh`, `benign/mmtc_30kbps_125b_2.sh` — mMTC (IoT-like) small-packet profiles (30 kbps)
- `benign/voip_24kbps_60b_continuous.sh`, `benign/voip_24kbps_60b_onoff.sh`, `benign/voip_g711_64kbps_20ms.sh` — VoIP call simulations (24 kbps variants and G.711 ~64 kbps)

Malicious profiles (examples):

- `malicious/udp_flood_highrate.sh` — UDP flood at very high bandwidth
- `malicious/pulsing_udp_flood.sh` — Pulsing high/low bandwidth UDP flood
- `malicious/udp_fragmentation.sh` — Oversized UDP packets (forces fragmentation)
- `malicious/small_packet_flood.sh` — Very small UDP packets at high rate
- `malicious/parallel_tcp_flood.sh` — Multiple TCP connections to target (parallel)
- `malicious/parallel_udp_flood.sh` — Multiple parallel UDP clients

Notes & usage
- A matching `iperf3` server must be running on the destination. Start the server with:

  iperf3 -s -p 5201

- Example client usage (eMBB):

  ./benign/embb_4mbps.sh 192.168.1.10 5201 480

- For MTC/URLLC we approximate Poisson arrivals by setting the UDP bandwidth and small datagram sizes. If you need strict Poisson timing, consider a small Python sender that draws inter-arrival times from an exponential distribution — these scripts are provided for compatibility with the experiment generator that expects shell scripts.

- Malicious scripts use high bandwidths or fragmentation and should only be used in controlled test environments.

These profiles are intended to be referenced by `generate_experiments.py` which scans `traffic_profiles/**/*.sh` and will pick scripts from the new subfolders as well.
Additional profiles included in this directory:

- eMBB (three variants):
  - `embb_3mbps_1400.sh` — 3 Mbps, 1400 B UDP datagrams
  - `embb_4mbps.sh` — 4 Mbps, 1200 B UDP datagrams (existing)
  - `embb_5mbps_1400.sh` — 5 Mbps, 1400 B UDP datagrams

- URLLC (two variants):
  - `urllc_10kbps_125b_1.sh` — 10 kbps, 125 B datagrams
  - `urllc_10kbps_125b_2.sh` — 10 kbps, 125 B datagrams (variant)

- mMTC (two variants):
  - `mmtc_30kbps_125b_1.sh` — 30 kbps, 125 B datagrams
  - `mmtc_30kbps_125b_2.sh` — 30 kbps, 125 B datagrams (variant)

- VoIP (two variants):
  - `voip_24kbps_60b_continuous.sh` — 24 kbps, 60 B payload, continuous
  - `voip_24kbps_60b_onoff.sh` — 24 kbps, 60 B payload, conversational on/off pattern

- Malicious profiles:
  - `udp_flood_highrate.sh` — UDP flood at very high bandwidth
  - `pulsing_udp_flood.sh` — Pulsing high/low bandwidth UDP flood
  - `udp_fragmentation.sh` — Oversized UDP packets (forces fragmentation)
  - `small_packet_flood.sh` — Very small UDP packets at high rate
  - `parallel_tcp_flood.sh` — Multiple TCP connections to target (parallel)
  - `parallel_udp_flood.sh` — Multiple parallel UDP clients

Notes & usage
- A matching `iperf3` server must be running on the server IP and port. Start server with:

  iperf3 -s -p 5201

- Example client usage (eMBB):

  ./embb_4mbps.sh 192.168.1.10 5201 480

- For MTC/URLLC we approximate Poisson arrivals by setting the UDP bandwidth and small datagram sizes. If you need stricter Poisson timing, consider a small Python sender that draws inter-arrival times from an exponential distribution — these scripts are intended for the experiment generator's existing usage and are iperf-compatible.

- These profiles are intended to be referenced by `generate_experiments.py` which scans `traffic_profiles/**/*.sh`.
