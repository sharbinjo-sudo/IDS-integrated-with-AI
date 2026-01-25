import subprocess
import shutil
from rich.console import Console

console = Console()


def check_tshark():
    """
    Ensure tshark is installed and accessible
    """
    if shutil.which("tshark") is None:
        raise RuntimeError(
            "tshark not found. Install Wireshark and add it to PATH."
        )


def capture_traffic(interface: str, output_file: str, duration: int = 0):
    """
    Capture traffic using tshark.

    :param interface: Network interface name (e.g., Ethernet)
    :param output_file: Output PCAP filename
    :param duration: Capture duration in seconds (0 = until stopped)
    """
    check_tshark()

    command = [
        "tshark",
        "-i", interface,
        "-w", output_file
    ]

    if duration > 0:
        command.extend(["-a", f"duration:{duration}"])

    console.print(
        f"[INFO] Starting capture on interface: {interface}",
        style="cyan"
    )
    console.print(
        f"[INFO] Writing packets to: {output_file}",
        style="cyan"
    )

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        console.print(
            "[CRITICAL] Packet capture failed. "
            "Run PowerShell as Administrator and verify interface name.",
            style="bold red"
        )
        raise e
