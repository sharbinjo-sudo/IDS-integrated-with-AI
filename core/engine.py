from typing import List, Dict
import os
import time
from rich.console import Console

from .flows import generate_flows
from .rules import (
    detect_port_scan,
    detect_flood,
    detect_bruteforce
)
from core.capture import capture_traffic
from ui.console import print_alert

console = Console()


# =====================================================
# OFFLINE DETECTION
# =====================================================

def run_detection(pcap_file: str, debug: bool = False) -> List[Dict]:
    """
    Run rule-based intrusion detection on a PCAP file.
    """
    console.print("[INFO] Starting intrusion analysis", style="cyan")

    flows = generate_flows(pcap_file)

    if not flows:
        console.print(
            "[INFO] No valid network flows found in PCAP",
            style="yellow"
        )
        return []

    console.print(
        f"[INFO] Total flows generated: {len(flows)}",
        style="green"
    )

    if debug:
        console.print("[DEBUG] Sample flows:", style="blue")
        for i, flow in enumerate(flows.values()):
            if i >= 10:
                break
            console.print(
                f"  {flow.src_ip}:{flow.src_port} → "
                f"{flow.dst_ip}:{flow.dst_port} | "
                f"pkts={flow.packet_count} dur={flow.duration:.3f}s"
            )

    alerts: List[Dict] = []

    console.print("[INFO] Running port scan detection", style="cyan")
    alerts.extend(detect_port_scan(flows))

    console.print("[INFO] Running brute-force detection", style="cyan")
    alerts.extend(detect_bruteforce(flows))

    console.print("[INFO] Running flood detection", style="cyan")
    alerts.extend(detect_flood(flows))

    if not alerts:
        console.print(
            "[INFO] Analysis complete — no threats detected",
            style="green"
        )
    else:
        console.print(
            f"[WARN] Analysis complete — {len(alerts)} threat(s) detected",
            style="bold red"
        )

    return alerts


# =====================================================
# LIVE IDS (WINDOW-BASED)
# =====================================================

def run_live(
    iface: str,
    window: int = 5,
    debug: bool = False
):
    """
    Run LIVE intrusion detection using sliding capture windows.
    Storage-safe: guarantees PCAP cleanup.
    """
    console.print(
        f"[INFO] Starting LIVE IDS (window = {window}s)",
        style="bold cyan"
    )

    seen_alerts = set()
    iteration = 0

    try:
        while True:
            iteration += 1
            pcap_file = f"live_window_{iteration}.pcap"

            try:
                console.print(
                    f"\n[INFO] Capturing traffic window #{iteration}",
                    style="cyan"
                )

                # Capture traffic
                capture_traffic(iface, pcap_file, duration=window)

                # Analyze traffic
                alerts = run_detection(pcap_file, debug=debug)

                # Print only NEW alerts (avoid spam)
                for alert in alerts:
                    key = (
                        alert.get("type"),
                        alert.get("src_ip"),
                        alert.get("dst_ip"),
                        alert.get("dst_port")
                    )
                    if key not in seen_alerts:
                        seen_alerts.add(key)
                        print_alert(alert)

            finally:
                # 🔒 GUARANTEED CLEANUP
                if os.path.exists(pcap_file):
                    try:
                        os.remove(pcap_file)
                    except Exception:
                        pass

            time.sleep(0.5)

    except KeyboardInterrupt:
        console.print(
            "\n[INFO] Live IDS stopped by user",
            style="yellow"
        )
