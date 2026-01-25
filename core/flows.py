import pyshark
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Tuple


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
        return self.end_time - self.start_time


FlowKey = Tuple[str, str, str, str, str]


def generate_flows(pcap_file: str) -> Dict[FlowKey, Flow]:
    """
    Parse PCAP and aggregate packets into flows.
    """
    flows: Dict[FlowKey, Flow] = {}

    capture = pyshark.FileCapture(
        pcap_file,
        keep_packets=False
    )

    for packet in capture:
        try:
            if not hasattr(packet, "ip"):
                continue

            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            protocol = packet.transport_layer

            if protocol is None:
                continue

            layer = packet[protocol.lower()]
            src_port = layer.srcport
            dst_port = layer.dstport

            timestamp = float(packet.sniff_timestamp)
            length = int(packet.length)

            key: FlowKey = (
                src_ip,
                dst_ip,
                src_port,
                dst_port,
                protocol
            )

            if key not in flows:
                flows[key] = Flow(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=src_port,
                    dst_port=dst_port,
                    protocol=protocol,
                    start_time=timestamp,
                    end_time=timestamp,
                    packet_count=1,
                    byte_count=length
                )
            else:
                flow = flows[key]
                flow.packet_count += 1
                flow.byte_count += length
                flow.end_time = timestamp

        except AttributeError:
            # malformed or unsupported packet
            continue

    capture.close()
    return flows
