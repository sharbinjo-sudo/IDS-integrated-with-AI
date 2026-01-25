from typing import List, Dict

from .flows import generate_flows
from .rules import detect_port_scan, detect_flood
# ML will be added later


def run_detection(pcap_file: str) -> List[Dict]:
    alerts: List[Dict] = []

    flows = generate_flows(pcap_file)

    print(f"[DEBUG] Total flows generated: {len(flows)}")

    # DEBUG: show top 10 flows
    for i, flow in enumerate(flows.values()):
        if i >= 10:
            break
        print(
            f"[DEBUG] {flow.src_ip}:{flow.src_port} -> "
            f"{flow.dst_ip}:{flow.dst_port} "
            f"pkts={flow.packet_count} dur={flow.duration:.4f}"
        )

    alerts.extend(detect_port_scan(flows))
    alerts.extend(detect_flood(flows))

    return alerts

