import os
import pyshark
from dataclasses import dataclass
from typing import Dict, Tuple
from rich.console import Console

console = Console()


@dataclass
class Flow:
    src_ip: str
    dst_ip: str
    src_port: str
    dst_port: str
    protocol: str
    start_time: float
    end_time: float
    packet_count: int = 0
    byte_count: int = 0

    @property
    def duration(self) -> float:
        return max(self.end_time - self.start_time, 0.001)


FlowKey = Tuple[str, str, str, str, str]


def generate_flows(pcap_file: str) -> Dict[FlowKey, Flow]:
    if not os.path.exists(pcap_file):
        raise FileNotFoundError(f"PCAP file not found: {pcap_file}")

    flows: Dict[FlowKey, Flow] = {}

    console.print(f"[INFO] Parsing PCAP file: {pcap_file}", style="cyan")

    capture = pyshark.FileCapture(
        pcap_file,
        keep_packets=False
    )

    packet_count = 0

    for packet in capture:
        try:
            packet_count += 1

            if not hasattr(packet, "ip"):
                continue

            protocol = packet.transport_layer
            if protocol is None:
                continue

            layer = packet[protocol.lower()]

            # Some packets may not have ports (e.g., malformed)
            src_port = getattr(layer, "srcport", "0")
            dst_port = getattr(layer, "dstport", "0")

            timestamp = float(packet.sniff_timestamp)
            length = int(packet.length)

            key: FlowKey = (
                packet.ip.src,
                packet.ip.dst,
                src_port,
                dst_port,
                protocol,
            )

            if key not in flows:
                flows[key] = Flow(
                    src_ip=key[0],
                    dst_ip=key[1],
                    src_port=key[2],
                    dst_port=key[3],
                    protocol=key[4],
                    start_time=timestamp,
                    end_time=timestamp,
                    packet_count=1,
                    byte_count=length,
                )
            else:
                flow = flows[key]
                flow.packet_count += 1
                flow.byte_count += length
                flow.end_time = timestamp

        except AttributeError:
            # Known pyshark parsing issue — safe to ignore
            continue
        except Exception as e:
            console.print(
                f"[WARN] Skipping malformed packet: {e}",
                style="yellow"
            )
            continue

    capture.close()

    console.print(
        f"[INFO] Processed {packet_count} packets, "
        f"generated {len(flows)} flows",
        style="green"
    )

    return flows
