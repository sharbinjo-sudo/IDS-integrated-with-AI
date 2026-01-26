from typing import Dict, List
from collections import defaultdict
from core.flows import Flow


# -----------------------------
# Utility
# -----------------------------

def _is_valid_port(port: str) -> bool:
    try:
        p = int(port)
        return 0 < p <= 65535
    except (TypeError, ValueError):
        return False


# -----------------------------
# PORT SCAN DETECTION
# -----------------------------
def detect_port_scan(
    flows: Dict,
    port_threshold: int = 10
) -> List[Dict]:
    """
    Detect port scanning behavior (direction-aware).
    """
    ports_by_pair = defaultdict(set)
    alerts: List[Dict] = []

    for flow in flows.values():
        if not _is_valid_port(flow.dst_port):
            continue

        key = (flow.src_ip, flow.dst_ip)
        ports_by_pair[key].add(flow.dst_port)

    for (src_ip, dst_ip), ports in ports_by_pair.items():
        if len(ports) >= port_threshold:
            alerts.append({
                "type": "PORT_SCAN",
                "severity": "CRITICAL",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "details": {
                    "unique_ports_attempted": len(ports),
                    "threshold": port_threshold,
                    "description": "Multiple ports probed on same host"
                }
            })

    return alerts

# -----------------------------
# SINGLE, CORRECT FLOOD DETECTION
# -----------------------------

def detect_flood(
    flows: Dict,
    pps_threshold: float = 500.0,
    min_packets: int = 500,
    min_duration: float = 1.0
) -> List[Dict]:
    """
    Detect REAL floods by aggregating traffic per source IP.
    Prevents short bursts (e.g., nmap) from being misclassified.
    """
    alerts: List[Dict] = []
    traffic_by_src = {}

    for flow in flows.values():
        duration = max(flow.duration, 0.001)

        if flow.src_ip not in traffic_by_src:
            traffic_by_src[flow.src_ip] = {
                "packets": 0,
                "first_seen": flow.start_time,
                "last_seen": flow.end_time,
                "dst_ips": set()
            }

        data = traffic_by_src[flow.src_ip]
        data["packets"] += flow.packet_count
        data["first_seen"] = min(data["first_seen"], flow.start_time)
        data["last_seen"] = max(data["last_seen"], flow.end_time)
        data["dst_ips"].add(flow.dst_ip)

    for src_ip, data in traffic_by_src.items():
        duration = max(data["last_seen"] - data["first_seen"], 0.001)

        if data["packets"] < min_packets:
            continue

        if duration < min_duration:
            continue

        pps = data["packets"] / duration

        if pps >= pps_threshold:
            alerts.append({
                "type": "FLOOD",
                "severity": "CRITICAL",
                "src_ip": src_ip,
                "details": {
                    "packets_per_sec": round(pps, 2),
                    "total_packets": data["packets"],
                    "duration_sec": round(duration, 2),
                    "unique_targets": len(data["dst_ips"]),
                    "threshold": pps_threshold,
                    "description": "Sustained high-rate traffic from single source"
                }
            })

    return alerts
def detect_bruteforce(
    flows: Dict,
    attempt_threshold: int = 10,
    max_duration: float = 60.0,
    monitored_ports = {22, 21, 3389}
) -> List[Dict]:
    """
    Detect brute-force login attempts (SSH, RDP, FTP).
    """
    alerts = []
    attempts = {}

    for flow in flows.values():
        try:
            dst_port = int(flow.dst_port)
        except (TypeError, ValueError):
            continue

        if dst_port not in monitored_ports:
            continue

        key = (flow.src_ip, flow.dst_ip, dst_port)

        if key not in attempts:
            attempts[key] = {
                "packets": 0,
                "start": flow.start_time,
                "end": flow.end_time
            }

        attempts[key]["packets"] += flow.packet_count
        attempts[key]["start"] = min(attempts[key]["start"], flow.start_time)
        attempts[key]["end"] = max(attempts[key]["end"], flow.end_time)

    for (src_ip, dst_ip, port), data in attempts.items():
        duration = max(data["end"] - data["start"], 0.001)

        if data["packets"] >= attempt_threshold and duration <= max_duration:
            alerts.append({
                "type": "BRUTE_FORCE",
                "severity": "CRITICAL",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "dst_port": port,
                "details": {
                    "attempts": data["packets"],
                    "duration_sec": round(duration, 2),
                    "threshold": attempt_threshold,
                    "description": "Multiple login attempts in short time window"
                }
            })

    return alerts
