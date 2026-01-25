from typing import Dict, List
from core.flows import Flow


PROTOCOL_MAP = {
    "TCP": 1,
    "UDP": 2,
    "ICMP": 3
}


def protocol_to_id(protocol: str) -> int:
    return PROTOCOL_MAP.get(protocol.upper(), 0)


def extract_features(flows: Dict) -> List[List[float]]:
    """
    Convert flows into numerical feature vectors.
    """
    feature_vectors: List[List[float]] = []

    for flow in flows.values():
        duration = max(flow.duration, 1e-6)  # prevent divide by zero

        packets_per_sec = flow.packet_count / duration
        bytes_per_sec = flow.byte_count / duration

        vector = [
            duration,
            flow.packet_count,
            flow.byte_count,
            packets_per_sec,
            bytes_per_sec,
            protocol_to_id(flow.protocol),
            int(flow.src_port),
            int(flow.dst_port),
        ]

        feature_vectors.append(vector)

    return feature_vectors
