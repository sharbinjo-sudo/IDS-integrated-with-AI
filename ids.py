import typer
from rich.console import Console
from core.capture import capture_traffic
from core.engine import run_detection
from ui.console import print_header, print_alert

app = typer.Typer(help="AI-Assisted Intrusion Detection System")
console = Console()


@app.command()
def capture(
    iface: str = typer.Option(..., help="Network interface name"),
    output: str = typer.Option("capture.pcap", help="Output PCAP file"),
):
    """
    Capture network traffic and save to PCAP
    """
    console.print(f"[INFO] Capturing traffic on interface: {iface}", style="cyan")
    console.print(f"[INFO] Output file: {output}", style="cyan")

    capture_traffic(iface, output)



@app.command()
def train(
    pcap: str = typer.Argument(..., help="PCAP file with normal traffic"),
):
    """
    Train anomaly detection model using normal traffic
    """
    console.print(f"[INFO] Training model using {pcap}", style="cyan")

    # TODO: call core.anomaly.train_model()
    console.print("[WARN] Training logic not implemented yet", style="yellow")


@app.command()
def detect(
    pcap: str = typer.Argument(..., help="PCAP file to analyze"),
):
    """
    Detect intrusions from a PCAP file
    """
    print_header()

    alerts = run_detection(pcap)

    if not alerts:
        console.print("\n[INFO] No threats detected", style="green")
        return

    for alert in alerts:
        print_alert(alert)


@app.command()
def live(
    iface: str = typer.Option(..., help="Network interface name"),
):
    """
    Run live intrusion detection
    """
    console.print(f"[INFO] Starting live IDS on interface: {iface}", style="cyan")

    # TODO: call core.engine.run_live()
    console.print("[WARN] Live detection not implemented yet", style="yellow")


if __name__ == "__main__":
    app()
