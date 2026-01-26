import os
import typer
from rich.console import Console
from rich.panel import Panel

from core.capture import capture_traffic
from core.engine import run_detection, run_live
from ui.console import print_header, print_alert

app = typer.Typer(
    help="User-Friendly Intrusion Detection System (CLI-based)"
)
console = Console()


# =====================================================
# CAPTURE COMMAND
# =====================================================

@app.command()
def capture(
    iface: str = typer.Option(..., help="Network interface name or number"),
    output: str = typer.Option("capture.pcap", help="Output PCAP file"),
    duration: int = typer.Option(
        0, help="Capture duration in seconds (0 = until stopped)"
    ),
):
    """
    Capture network traffic and save it to a PCAP file.
    """
    try:
        capture_traffic(iface, output, duration)
    except Exception as e:
        console.print(
            Panel(str(e), title="Capture Failed", style="red")
        )


# =====================================================
# OFFLINE DETECTION COMMAND
# =====================================================

@app.command()
def detect(
    pcap: str = typer.Argument(..., help="PCAP file to analyze"),
    debug: bool = typer.Option(
        False, help="Enable debug output (advanced users)"
    ),
):
    """
    Analyze a PCAP file for possible intrusions.
    """
    if not os.path.exists(pcap):
        console.print(
            Panel(
                f"PCAP file not found:\n{pcap}",
                title="Input Error",
                style="red"
            )
        )
        raise typer.Exit(code=1)

    print_header()

    try:
        alerts = run_detection(pcap, debug=debug)
    except Exception as e:
        console.print(
            Panel(str(e), title="Analysis Failed", style="red")
        )
        raise typer.Exit(code=1)

    if not alerts:
        console.print("\n✅ No threats detected", style="bold green")
        return

    for alert in alerts:
        print_alert(alert)


# =====================================================
# LIVE IDS COMMAND (REAL, WORKING)
# =====================================================

@app.command()
def live(
    iface: str = typer.Option(..., help="Network interface name or number"),
    window: int = typer.Option(
        5, help="Capture window size in seconds"
    ),
    debug: bool = typer.Option(
        False, help="Enable debug output"
    ),
):
    """
    Run LIVE intrusion detection (window-based).
    """
    console.print(
        Panel(
            f"Starting LIVE IDS\n\n"
            f"Interface : {iface}\n"
            f"Window    : {window} seconds\n\n"
            f"Press Ctrl+C to stop",
            title="Live IDS",
            style="cyan"
        )
    )

    try:
        run_live(iface, window=window, debug=debug)
    except Exception as e:
        console.print(
            Panel(str(e), title="Live IDS Failed", style="red")
        )


# =====================================================
# TRAIN PLACEHOLDER
# =====================================================

@app.command()
def train(
    pcap: str = typer.Argument(..., help="PCAP file containing normal traffic"),
):
    """
    Train anomaly detection model (not implemented yet).
    """
    console.print(
        Panel(
            "Training is not implemented yet.\n\n"
            "Current version supports rule-based detection only.",
            title="Not Implemented",
            style="yellow"
        )
    )


if __name__ == "__main__":
    app()
