from typing import Dict, List
from core.flows import Flow


PROTOCOL_MAP = {
    "TCP": 1,
    "UDP": 2,
    "ICMP": 3
}


def protocol_to_id(protocol: str) -> int:
    """
    Convert protocol string to stable numeric ID.
    """
    if not protocol:
        return 0
    return PROTOCOL_MAP.get(protocol.upper(), 0)


def safe_port(port: str) -> int:
    """
    Convert port to int safely.
    Non-numeric or missing ports return 0.
    """
    try:
        return int(port)
    except (TypeError, ValueError):
        return 0


def extract_features(flows: Dict) -> List[List[float]]:
    """
    Convert flows into numerical feature vectors.
    Safe for offline ML / statistical analysis.
    """
    feature_vectors: List[List[float]] = []

    for flow in flows.values():
        duration = max(flow.duration, 1e-6)

        packets_per_sec = flow.packet_count / duration
        bytes_per_sec = flow.byte_count / duration

        vector = [
            duration,                    # flow duration
            flow.packet_count,           # total packets
            flow.byte_count,             # total bytes
            packets_per_sec,             # packet rate
            bytes_per_sec,               # byte rate
            protocol_to_id(flow.protocol),
            safe_port(flow.src_port),    # SAFE port encoding
            safe_port(flow.dst_port),
        ]

        feature_vectors.append(vector)

    return feature_vectors
