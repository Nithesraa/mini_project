"""
Authoritative Feature Catalog for Industrial IoT Intrusion Detection
Reconciled against output/checkpoints/preprocessed_meta.pkl (Exactly 79 Features)
"""

FEATURE_CATEGORIES = {
    "1. Endpoint & Protocol": [
        "Src_Port", "Dst_Port", "Protocol"
    ],
    "2. Flow Duration & Rates": [
        "Flow_Duration", "Flow_Byts/s", "Flow_Pkts/s", "Fwd_Pkts/s", "Bwd_Pkts/s"
    ],
    "3. Packet Counts & Volumetric Byte Aggregates": [
        "Tot_Fwd_Pkts", "Tot_Bwd_Pkts", "TotLen_Fwd_Pkts", "TotLen_Bwd_Pkts"
    ],
    "4. Directional Packet Length Statistics": [
        "Fwd_Pkt_Len_Max", "Fwd_Pkt_Len_Min", "Fwd_Pkt_Len_Mean", "Fwd_Pkt_Len_Std",
        "Bwd_Pkt_Len_Max", "Bwd_Pkt_Len_Min", "Bwd_Pkt_Len_Mean", "Bwd_Pkt_Len_Std",
        "Pkt_Len_Min", "Pkt_Len_Max", "Pkt_Len_Mean", "Pkt_Len_Std", "Pkt_Len_Var",
        "Pkt_Size_Avg", "Fwd_Seg_Size_Avg", "Bwd_Seg_Size_Avg", "Fwd_Seg_Size_Min"
    ],
    "5. Inter-Arrival Time (IAT) Statistics": [
        "Flow_IAT_Mean", "Flow_IAT_Std", "Flow_IAT_Max", "Flow_IAT_Min",
        "Fwd_IAT_Tot", "Fwd_IAT_Mean", "Fwd_IAT_Std", "Fwd_IAT_Max", "Fwd_IAT_Min",
        "Bwd_IAT_Tot", "Bwd_IAT_Mean", "Bwd_IAT_Std", "Bwd_IAT_Max", "Bwd_IAT_Min"
    ],
    "6. TCP Flags & Control Signaling": [
        "FIN_Flag_Cnt", "SYN_Flag_Cnt", "RST_Flag_Cnt", "PSH_Flag_Cnt", "ACK_Flag_Cnt", "URG_Flag_Cnt",
        "CWE_Flag_Count", "ECE_Flag_Cnt", "Fwd_PSH_Flags", "Bwd_PSH_Flags", "Fwd_URG_Flags", "Bwd_URG_Flags"
    ],
    "7. Header & Window State Indicators": [
        "Fwd_Header_Len", "Bwd_Header_Len", "Init_Fwd_Win_Byts", "Init_Bwd_Win_Byts", "Fwd_Act_Data_Pkts"
    ],
    "8. Bulk Transfer & Subflow Aggregates": [
        "Down/Up_Ratio",
        "Fwd_Byts/b_Avg", "Fwd_Pkts/b_Avg", "Fwd_Blk_Rate_Avg",
        "Bwd_Byts/b_Avg", "Bwd_Pkts/b_Avg", "Bwd_Blk_Rate_Avg",
        "Subflow_Fwd_Pkts", "Subflow_Fwd_Byts", "Subflow_Bwd_Pkts", "Subflow_Bwd_Byts"
    ],
    "9. Active & Idle Timing States": [
        "Active_Mean", "Active_Std", "Active_Max", "Active_Min",
        "Idle_Mean", "Idle_Std", "Idle_Max", "Idle_Min"
    ]
}

FEATURE_DEFINITIONS = {
    # 1. Endpoint & Protocol
    "Src_Port": {
        "meaning": "Ephemeral client port initiating the communication session.",
        "relevance": "Attack scripts randomize source ports or increment them sequentially to bypass rudimentary stateful firewall filtering.",
        "units": "Port (0-65535)"
    },
    "Dst_Port": {
        "meaning": "Transport-layer port on the destination target device.",
        "relevance": "Specific attacks target specific service ports (e.g., Telnet 23/2323 for Mirai, HTTP 80/8080 for web attacks). Benign IIoT sensors target fixed MQTT (1883) or CoAP (5683) brokers.",
        "units": "Port (0-65535)"
    },
    "Protocol": {
        "meaning": "Transport-layer protocol identifier (6=TCP, 17=UDP, 1=ICMP).",
        "relevance": "Directly isolates UDP-based floods (Mirai UDP) from TCP-based connection attempts (SYN Floods, Port Scans).",
        "units": "IANA Protocol Code"
    },

    # 2. Flow Duration & Rates
    "Flow_Duration": {
        "meaning": "Total duration of bidirectional flow in microseconds.",
        "relevance": "Short durations characterize brute-force scans; long persistent sessions characterize benign telemetry monitoring.",
        "units": "Microseconds (µs)"
    },
    "Flow_Byts/s": {
        "meaning": "Byte transmission rate per second across the flow.",
        "relevance": "High throughput rates indicate volumetric DDoS floods or unauthorized data exfiltration.",
        "units": "Bytes/sec"
    },
    "Flow_Pkts/s": {
        "meaning": "Packet transmission rate per second across the flow.",
        "relevance": "Extreme packet rates overwhelm gateway buffers and router state tables.",
        "units": "Packets/sec"
    },
    "Fwd_Pkts/s": {
        "meaning": "Packet transmission rate in the forward (client-to-server) direction.",
        "relevance": "Measures upstream transmission intensity; high values indicate raw flooding without awaiting responses.",
        "units": "Packets/sec"
    },
    "Bwd_Pkts/s": {
        "meaning": "Packet transmission rate in the backward (server-to-client) direction.",
        "relevance": "Zero or near-zero rates highlight unacknowledged probes or dead-host scanning.",
        "units": "Packets/sec"
    },

    # 3. Packet Counts & Volumetric Bytes
    "Tot_Fwd_Pkts": {
        "meaning": "Total number of packets transmitted in the forward direction.",
        "relevance": "Identifies asymmetric flow structures typical of blind reflection or scanning.",
        "units": "Packet Count"
    },
    "Tot_Bwd_Pkts": {
        "meaning": "Total number of packets transmitted in the backward direction.",
        "relevance": "Absence of backward packets flags incomplete handshakes and stealth scans.",
        "units": "Packet Count"
    },
    "TotLen_Fwd_Pkts": {
        "meaning": "Cumulative payload bytes transferred in the forward direction.",
        "relevance": "Distinguishes small telemetry sensor readings from large bandwidth-saturating floods.",
        "units": "Bytes"
    },
    "TotLen_Bwd_Pkts": {
        "meaning": "Cumulative payload bytes transferred in the backward direction.",
        "relevance": "Reflects server response volume; high response sizes indicate active data retrieval.",
        "units": "Bytes"
    },

    # 4. Directional Packet Length Statistics
    "Fwd_Pkt_Len_Max": {
        "meaning": "Maximum observed packet payload size in the forward direction.",
        "relevance": "Helps distinguish small control packets from large data payloads.",
        "units": "Bytes"
    },
    "Fwd_Pkt_Len_Min": {
        "meaning": "Minimum observed packet payload size in the forward direction.",
        "relevance": "Non-zero minimums indicate fixed padding often used by automated attack scripts.",
        "units": "Bytes"
    },
    "Fwd_Pkt_Len_Mean": {
        "meaning": "Average packet payload size in the forward direction.",
        "relevance": "Captures standard communication payload characteristics.",
        "units": "Bytes"
    },
    "Fwd_Pkt_Len_Std": {
        "meaning": "Standard deviation of forward packet payload sizes.",
        "relevance": "Benign IIoT flows exhibit variable packet sizes; volumetric floods transmit repeated, fixed-size padded packets resulting in near-zero standard deviation.",
        "units": "Bytes"
    },
    "Bwd_Pkt_Len_Max": {
        "meaning": "Maximum observed packet payload size in the backward direction.",
        "relevance": "Identifies maximum service response capacity and protocol headers.",
        "units": "Bytes"
    },
    "Bwd_Pkt_Len_Min": {
        "meaning": "Minimum observed packet payload size in the backward direction.",
        "relevance": "Zero payload in backward packets indicates raw TCP ACK or RST packets.",
        "units": "Bytes"
    },
    "Bwd_Pkt_Len_Mean": {
        "meaning": "Average packet payload size in the backward direction.",
        "relevance": "Reflects typical server response payload volume.",
        "units": "Bytes"
    },
    "Bwd_Pkt_Len_Std": {
        "meaning": "Standard deviation of backward packet payload sizes.",
        "relevance": "Variance in server response indicates diverse application transactions.",
        "units": "Bytes"
    },
    "Pkt_Len_Min": {
        "meaning": "Minimum packet payload size across the bidirectional flow.",
        "relevance": "Zero indicates presence of empty control packets (SYN, ACK, RST).",
        "units": "Bytes"
    },
    "Pkt_Len_Max": {
        "meaning": "Maximum packet payload size across the bidirectional flow.",
        "relevance": "Highlights MTU-sized packets used in bulk data transfer or large UDP floods.",
        "units": "Bytes"
    },
    "Pkt_Len_Mean": {
        "meaning": "Average packet payload size across both directions.",
        "relevance": "Core statistical indicator of flow application behavior.",
        "units": "Bytes"
    },
    "Pkt_Len_Std": {
        "meaning": "Standard deviation of packet lengths across both directions.",
        "relevance": "Low variance points to synthetic automated traffic; high variance points to human or complex multi-sensor sessions.",
        "units": "Bytes"
    },
    "Pkt_Len_Var": {
        "meaning": "Variance of packet lengths across the bidirectional flow.",
        "relevance": "Highly sensitive to protocol diversity; highlights uniform payload botnet traffic.",
        "units": "Bytes²"
    },
    "Pkt_Size_Avg": {
        "meaning": "Average size of all packets in the flow including protocol headers.",
        "relevance": "Measures effective wire packet sizing across the communication link.",
        "units": "Bytes"
    },
    "Fwd_Seg_Size_Avg": {
        "meaning": "Average segment size observed in the forward direction.",
        "relevance": "Mirrors forward packet length mean; tracks TCP segmentation behavior.",
        "units": "Bytes"
    },
    "Bwd_Seg_Size_Avg": {
        "meaning": "Average segment size observed in the backward direction.",
        "relevance": "Mirrors backward packet length mean; tracks responder segmentation.",
        "units": "Bytes"
    },
    "Fwd_Seg_Size_Min": {
        "meaning": "Minimum segment size observed in the forward direction.",
        "relevance": "Zero indicates empty TCP handshake segments.",
        "units": "Bytes"
    },

    # 5. Inter-Arrival Time (IAT) Statistics
    "Flow_IAT_Mean": {
        "meaning": "Average time interval between consecutive packets in the flow.",
        "relevance": "Automated floods compress inter-arrival times down to microseconds, whereas benign IoT telemetry exhibits human- or timer-driven pacing.",
        "units": "Microseconds (µs)"
    },
    "Flow_IAT_Std": {
        "meaning": "Standard deviation of inter-packet arrival times.",
        "relevance": "Jitter and network latency introduce variance in benign flows; script-driven floods maintain constant packet injection intervals.",
        "units": "Microseconds (µs)"
    },
    "Flow_IAT_Max": {
        "meaning": "Maximum time interval between consecutive flow packets.",
        "relevance": "Highlights connection pauses, keepalives, and poll timeouts.",
        "units": "Microseconds (µs)"
    },
    "Flow_IAT_Min": {
        "meaning": "Minimum time interval between consecutive flow packets.",
        "relevance": "Microsecond minimums indicate multi-threaded high-rate attack bursts.",
        "units": "Microseconds (µs)"
    },
    "Fwd_IAT_Tot": {
        "meaning": "Total cumulative time between all forward-direction packets.",
        "relevance": "Captures overall active transmission span from the sender.",
        "units": "Microseconds (µs)"
    },
    "Fwd_IAT_Mean": {
        "meaning": "Average time interval between forward-direction packets.",
        "relevance": "Measures sender transmission cadence and pacing regularity.",
        "units": "Microseconds (µs)"
    },
    "Fwd_IAT_Std": {
        "meaning": "Standard deviation of time intervals between forward packets.",
        "relevance": "Evaluates consistency of upstream transmission bursts.",
        "units": "Microseconds (µs)"
    },
    "Fwd_IAT_Max": {
        "meaning": "Maximum time interval between consecutive forward packets.",
        "relevance": "Detects delayed upstream transmission phases.",
        "units": "Microseconds (µs)"
    },
    "Fwd_IAT_Min": {
        "meaning": "Minimum time interval between consecutive forward packets.",
        "relevance": "Isolates hardware wire-speed packet generation.",
        "units": "Microseconds (µs)"
    },
    "Bwd_IAT_Tot": {
        "meaning": "Total cumulative time between backward-direction packets.",
        "relevance": "Captures overall responder interaction span.",
        "units": "Microseconds (µs)"
    },
    "Bwd_IAT_Mean": {
        "meaning": "Average time interval between backward-direction packets.",
        "relevance": "Reflects gateway processing and response scheduling.",
        "units": "Microseconds (µs)"
    },
    "Bwd_IAT_Std": {
        "meaning": "Standard deviation of time intervals between backward packets.",
        "relevance": "Measures variability in server processing response times.",
        "units": "Microseconds (µs)"
    },
    "Bwd_IAT_Max": {
        "meaning": "Maximum time interval between consecutive backward packets.",
        "relevance": "Identifies long response timeouts or server lag.",
        "units": "Microseconds (µs)"
    },
    "Bwd_IAT_Min": {
        "meaning": "Minimum time interval between consecutive backward packets.",
        "relevance": "Tracks immediate pipeline acknowledgments.",
        "units": "Microseconds (µs)"
    },

    # 6. TCP Flags & Control Signaling
    "FIN_Flag_Cnt": {
        "meaning": "Count of packets with the TCP FIN (Finish) flag set.",
        "relevance": "Premature FIN flags indicate abnormal or reset connections common in port scanners.",
        "units": "Flag Count"
    },
    "SYN_Flag_Cnt": {
        "meaning": "Count of packets with the TCP SYN (Synchronize) flag set.",
        "relevance": "Elevated SYN counts without matching ACKs isolate TCP SYN Flooding (DoS) and stealth port scanning.",
        "units": "Flag Count"
    },
    "RST_Flag_Cnt": {
        "meaning": "Count of packets with the TCP RST (Reset) flag set.",
        "relevance": "High RST counts occur when targets reject connections on closed ports during scanning probes.",
        "units": "Flag Count"
    },
    "PSH_Flag_Cnt": {
        "meaning": "Count of packets with the TCP PSH (Push) flag set.",
        "relevance": "Forces data through application buffers; common in interactive shells or HTTP flood variants.",
        "units": "Flag Count"
    },
    "ACK_Flag_Cnt": {
        "meaning": "Count of packets with the TCP ACK (Acknowledgment) flag set.",
        "relevance": "Legitimate TCP sessions consist primarily of acknowledged exchanges; low ACK rates flag raw floods.",
        "units": "Flag Count"
    },
    "URG_Flag_Cnt": {
        "meaning": "Count of packets with the TCP URG (Urgent) flag set.",
        "relevance": "Rare in industrial IoT networks; unexpected presence indicates protocol fuzzing or evasion attempts.",
        "units": "Flag Count"
    },
    "CWE_Flag_Count": {
        "meaning": "Count of Congestion Window Reduced (CWR) flags.",
        "relevance": "Monitors TCP congestion control negotiation; abnormal values reflect state manipulation.",
        "units": "Flag Count"
    },
    "ECE_Flag_Cnt": {
        "meaning": "Count of ECN-Echo (Explicit Congestion Notification) flags.",
        "relevance": "Signals network bottleneck feedback; exploited in certain protocol evasion attacks.",
        "units": "Flag Count"
    },
    "Fwd_PSH_Flags": {
        "meaning": "Directional PSH flag count in forward packets.",
        "relevance": "Tracks client-side data push behavior.",
        "units": "Flag Count"
    },
    "Bwd_PSH_Flags": {
        "meaning": "Directional PSH flag count in backward packets.",
        "relevance": "Tracks server-side data push behavior.",
        "units": "Flag Count"
    },
    "Fwd_URG_Flags": {
        "meaning": "Directional URG flag count in forward packets.",
        "relevance": "Detects client-side out-of-band signaling.",
        "units": "Flag Count"
    },
    "Bwd_URG_Flags": {
        "meaning": "Directional URG flag count in backward packets.",
        "relevance": "Detects server-side out-of-band signaling.",
        "units": "Flag Count"
    },

    # 7. Header & Window State Indicators
    "Fwd_Header_Len": {
        "meaning": "Cumulative bytes of TCP/IP headers in forward packets.",
        "relevance": "High header-to-payload ratios indicate small-packet probing or TCP option manipulation.",
        "units": "Bytes"
    },
    "Bwd_Header_Len": {
        "meaning": "Cumulative bytes of TCP/IP headers in backward packets.",
        "relevance": "Tracks responder protocol overhead.",
        "units": "Bytes"
    },
    "Init_Fwd_Win_Byts": {
        "meaning": "Initial forward TCP window size in bytes advertised by the client.",
        "relevance": "Mirai botnet toolkits hardcode distinctive non-standard window sizes into their raw socket headers.",
        "units": "Bytes (0-65535)"
    },
    "Init_Bwd_Win_Byts": {
        "meaning": "Initial backward TCP window size in bytes advertised by the server/responder.",
        "relevance": "In SYN flooding, unreachable targets, or spoofed ARP hosts, backward window sizes are 0 or anomalous.",
        "units": "Bytes (0-65535)"
    },
    "Fwd_Act_Data_Pkts": {
        "meaning": "Count of forward packets carrying at least 1 byte of application payload.",
        "relevance": "Distinguishes data-bearing sessions from empty handshake or port scans.",
        "units": "Packet Count"
    },

    # 8. Bulk Transfer & Subflow Aggregates
    "Down/Up_Ratio": {
        "meaning": "Ratio of backward (download) to forward (upload) packets.",
        "relevance": "Symmetric ratios characterize balanced exchanges; extreme ratios characterize one-way floods.",
        "units": "Ratio"
    },
    "Fwd_Byts/b_Avg": {
        "meaning": "Average bytes per bulk transmission in forward direction.",
        "relevance": "Measures upstream bulk transfer volume.",
        "units": "Bytes/bulk"
    },
    "Fwd_Pkts/b_Avg": {
        "meaning": "Average packets per bulk transmission in forward direction.",
        "relevance": "Measures upstream packet clustering.",
        "units": "Packets/bulk"
    },
    "Fwd_Blk_Rate_Avg": {
        "meaning": "Average bulk transmission rate in forward direction.",
        "relevance": "Captures sustained upstream data bursts.",
        "units": "Bulks/sec"
    },
    "Bwd_Byts/b_Avg": {
        "meaning": "Average bytes per bulk transmission in backward direction.",
        "relevance": "Measures downstream bulk transfer volume.",
        "units": "Bytes/bulk"
    },
    "Bwd_Pkts/b_Avg": {
        "meaning": "Average packets per bulk transmission in backward direction.",
        "relevance": "Measures downstream packet clustering.",
        "units": "Packets/bulk"
    },
    "Bwd_Blk_Rate_Avg": {
        "meaning": "Average bulk transmission rate in backward direction.",
        "relevance": "Captures sustained downstream data bursts.",
        "units": "Bulks/sec"
    },
    "Subflow_Fwd_Pkts": {
        "meaning": "Average packets in forward subflows.",
        "relevance": "Tracks multi-stage connection transactions.",
        "units": "Packet Count"
    },
    "Subflow_Fwd_Byts": {
        "meaning": "Average bytes in forward subflows.",
        "relevance": "Monitors multi-stage payload transfers and command-and-control transactions.",
        "units": "Bytes"
    },
    "Subflow_Bwd_Pkts": {
        "meaning": "Average packets in backward subflows.",
        "relevance": "Monitors multi-stage response packets.",
        "units": "Packet Count"
    },
    "Subflow_Bwd_Byts": {
        "meaning": "Average bytes in backward subflows.",
        "relevance": "Monitors multi-stage response payload volume.",
        "units": "Bytes"
    },

    # 9. Active & Idle Timing States
    "Active_Mean": {
        "meaning": "Average time the connection was active before becoming idle.",
        "relevance": "Distinguishes bursty application traffic from steady streams.",
        "units": "Microseconds (µs)"
    },
    "Active_Std": {
        "meaning": "Standard deviation of active connection durations.",
        "relevance": "Measures regularity of active communication windows.",
        "units": "Microseconds (µs)"
    },
    "Active_Max": {
        "meaning": "Maximum time the connection was active before an idle period.",
        "relevance": "Captures longest sustained transmission burst.",
        "units": "Microseconds (µs)"
    },
    "Active_Min": {
        "meaning": "Minimum time the connection was active before an idle period.",
        "relevance": "Tracks shortest observed transmission burst.",
        "units": "Microseconds (µs)"
    },
    "Idle_Mean": {
        "meaning": "Average time the flow remained idle without packet transmission.",
        "relevance": "Distinguishes persistent connections with polling from transient scan probes that terminate immediately.",
        "units": "Microseconds (µs)"
    },
    "Idle_Std": {
        "meaning": "Standard deviation of idle durations between active periods.",
        "relevance": "Regular idle intervals indicate timer-based sensor reporting.",
        "units": "Microseconds (µs)"
    },
    "Idle_Max": {
        "meaning": "Maximum time the connection remained idle before resuming.",
        "relevance": "Highlights longest inactivity timeout before reconnection.",
        "units": "Microseconds (µs)"
    },
    "Idle_Min": {
        "meaning": "Minimum time the connection remained idle before resuming.",
        "relevance": "Reflects minimum inter-session pause.",
        "units": "Microseconds (µs)"
    }
}

def get_feature_info(feature_name):
    """Retrieve definition and relevance for a given feature."""
    return FEATURE_DEFINITIONS.get(feature_name, {
        "meaning": "Industrial IoT network flow metric.",
        "relevance": "Contributes to behavioral flow profiling.",
        "units": "Numerical"
    })
