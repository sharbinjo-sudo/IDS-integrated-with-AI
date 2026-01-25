from rich.console import Console

console = Console()


def print_header():
    console.print("\nAI-Assisted Intrusion Detection System", style="bold white")
    console.print("Mode      : Offline Detection")
    console.print("Engine    : Rule-Based (ML pending)")
    console.print("────────────────────────────────────")


def print_alert(alert: dict):
    severity = alert.get("severity", "INFO")

    if severity == "CRITICAL":
        style = "bold red"
    elif severity == "WARNING":
        style = "yellow"
    else:
        style = "cyan"

    console.print(f"\n[{severity}] {alert['type']}", style=style)

    for key, value in alert.items():
        if key not in ("type", "severity"):
            console.print(f"  {key}: {value}")
