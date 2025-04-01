import numpy as np
import pandas as pd
def extract_features(pcap_file):
    """
    Extract features from a PCAP file for intrusion detection
    Requires scapy library to be installed
    """
    try:
        from scapy.all import rdpcap, IP, TCP, UDP
    except ImportError:
        print("Scapy library not found. Install it using 'pip install scapy'")
        return None
    print(f"Extracting features from {pcap_file}...")
    packets = rdpcap(pcap_file)
    features = []
    # Group packets by flow (source IP, dest IP, source port, dest port)
    flows = {}
    for packet in packets:
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            proto = packet[IP].proto
            if TCP in packet:
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                flags = packet[TCP].flags
            elif UDP in packet:
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
                flags = 0
            else:
                continue
            flow_key = (src_ip, dst_ip, src_port, dst_port, proto)
            if flow_key not in flows:
                flows[flow_key] = {
                    'packets': [],
                    'start_time': packet.time,
                    'bytes': 0,
                    'flags': set()
                }
            flows[flow_key]['packets'].append(packet)
            flows[flow_key]['bytes'] += len(packet)
            if TCP in packet:
                flows[flow_key]['flags'].add(flags)
    # Extract features for each flow
    for flow_key, flow in flows.items():
        src_ip, dst_ip, src_port, dst_port, proto = flow_key
        # Basic features
        duration = flow['packets'][-1].time - flow['start_time']
        packet_count = len(flow['packets'])
        byte_count = flow['bytes']
        # Calculate packet rate and byte rate
        packet_rate = packet_count / duration if duration > 0 else 0
        byte_rate = byte_count / duration if duration > 0 else 0
        # Flag features
        flag_features = 0
        if flow['flags']:
            flag_features = sum(1 for f in flow['flags'])
        # Packet size statistics
        sizes = [len(p) for p in flow['packets']]
        avg_size = np.mean(sizes) if sizes else 0
        std_size = np.std(sizes) if sizes else 0
        # Inter-arrival time statistics
        times = [p.time for p in flow['packets']]
        inter_arrival = np.diff(times)
        avg_inter = np.mean(inter_arrival) if len(inter_arrival) > 0 else 0
        std_inter = np.std(inter_arrival) if len(inter_arrival) > 0 else 0
        # Create feature vector
        feature_vector = {
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port,
            'protocol': proto,
            'duration': duration,
            'packet_count': packet_count,
            'byte_count': byte_count,
            'packet_rate': packet_rate,
            'byte_rate': byte_rate,
            'flag_features': flag_features,
            'avg_packet_size': avg_size,
            'std_packet_size': std_size,
            'avg_inter_arrival': avg_inter,
            'std_inter_arrival': std_inter
        }
        features.append(feature_vector)
    # Convert to DataFrame
    df = pd.DataFrame(features)
    return df
    