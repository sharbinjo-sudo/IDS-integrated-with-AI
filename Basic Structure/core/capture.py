import subprocess
import shutil
from rich.console import Console
from rich.panel import Panel

console = Console()


def check_tshark() -> None:
    """
    Ensure tshark is installed and accessible.
    """
    if shutil.which("tshark") is None:
        console.print(
            Panel(
                "❌ tshark not found.\n\n"
                "Please install Wireshark and ensure tshark is added to PATH.",
                title="Missing Dependency",
                style="red"
            )
        )
        raise RuntimeError("tshark not found")


def capture_traffic(interface: str, output_file: str, duration: int = 0) -> None:
    """
    Capture network traffic using tshark.

    :param interface: Network interface name (e.g., Ethernet, eth0)
    :param output_file: Output PCAP filename
    :param duration: Capture duration in seconds (0 = until manually stopped)
    """

    if not interface.strip():
        raise ValueError("Interface name cannot be empty")

    if not output_file.endswith(".pcap"):
        output_file += ".pcap"

    if duration < 0:
        raise ValueError("Duration must be 0 or a positive integer")

    check_tshark()

    command = ["tshark", "-i", interface, "-w", output_file]

    if duration > 0:
        command.extend(["-a", f"duration:{duration}"])

    console.print(
        Panel(
            f"📡 Interface : [bold]{interface}[/bold]\n"
            f"💾 Output    : [bold]{output_file}[/bold]\n"
            f"⏱ Duration  : [bold]{'Unlimited' if duration == 0 else str(duration) + ' sec'}[/bold]",
            title="Starting Packet Capture",
            style="cyan"
        )
    )

    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )
        console.print(
            f"✅ Capture completed successfully: {output_file}",
            style="bold green"
        )

    except subprocess.CalledProcessError as e:
        console.print(
            Panel(
                "❌ Packet capture failed.\n\n"
                "Possible reasons:\n"
                "- Incorrect interface name\n"
                "- Insufficient privileges (run as Administrator)\n"
                "- Interface currently down\n\n"
                f"Error:\n{e.stderr}",
                title="Capture Error",
                style="red"
            )
        )
        raise RuntimeError("Packet capture failed") from e
