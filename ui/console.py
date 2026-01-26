from rich.console import Console
from rich.panel import Panel

console = Console()


def print_header():
    """
    Print IDS header for analysis output.
    """
    console.print(
        Panel(
            "AI-Assisted Intrusion Detection System\n"
            "Mode   : Offline Analysis\n"
            "Engine : Rule-Based Detection",
            title="IDS Report",
            style="bold cyan"
        )
    )


def print_alert(alert: dict):
    """
    Print a single intrusion alert in a user-friendly way.
    """
    if not isinstance(alert, dict):
        console.print("[WARN] Invalid alert format", style="yellow")
        return

    severity = str(alert.get("severity", "INFO")).upper()
    alert_type = alert.get("type", "UNKNOWN")

    if severity == "CRITICAL":
        style = "bold red"
        icon = "🚨"
    elif severity == "WARNING":
        style = "yellow"
        icon = "⚠️"
    else:
        style = "cyan"
        icon = "ℹ️"

    body_lines = []

    for key, value in alert.items():
        if key in ("type", "severity"):
            continue
        body_lines.append(f"[bold]{key.replace('_', ' ').title()}[/bold]: {value}")

    body = "\n".join(body_lines) if body_lines else "No additional details"

    console.print(
        Panel(
            body,
            title=f"{icon} {alert_type} ({severity})",
            style=style
        )
    )
