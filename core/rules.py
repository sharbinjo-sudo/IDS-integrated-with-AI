from typing import Dict, List
from collections import defaultdict
from core.flows import Flow


def detect_port_scan(flows, port_threshold=10):
    from collections import defaultdict

    ports_by_src = defaultdict(set)
    alerts = []

    for flow in flows.values():
        # only count client-originated attempts
        if flow.packet_count < 1:
            continue

        ports_by_src[flow.src_ip].add(flow.dst_port)

    for src_ip, ports in ports_by_src.items():
        if len(ports) >= port_threshold:
            alerts.append({
                "type": "PORT_SCAN",
                "severity": "CRITICAL",
                "src_ip": src_ip,
                "details": {
                    "unique_ports_attempted": len(ports),
                    "threshold": port_threshold
                }
            })

    return alerts


def detect_flood(
    flows: Dict,
    pps_threshold: float = 1000.0,
    min_packets: int = 100
) -> List[Dict]:
    alerts = []

    seen = set()  # prevent duplicates

    for flow in flows.values():
        # Ignore very small flows
        if flow.packet_count < min_packets:
            continue

        duration = max(flow.duration, 0.1)  # clamp duration
        pps = flow.packet_count / duration

        key = (flow.src_ip, flow.dst_ip)

        if pps >= pps_threshold and key not in seen:
            alerts.append({
                "type": "FLOOD",
                "severity": "CRITICAL",
                "src_ip": flow.src_ip,
                "dst_ip": flow.dst_ip,
                "details": {
                    "packets_per_sec": round(pps, 2),
                    "packet_count": flow.packet_count,
                    "duration_sec": round(duration, 2),
                    "threshold": pps_threshold
                }
            })
            seen.add(key)

    return alerts
