import subprocess
import re
from rich.console import Console
from rich.table import Table

console = Console()

def typewriter(text, delay=0.03):
    import time
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def show_intro():
    ascii_logo = """
[red]
████              █████████        ███████████████      ██████████
████             ████   █████      ███████████████     ████    ████
████            ████      ████           ███          ████      ████
████            ██████████████         ██             ██████████████
████            ████      ████       ██               ████      ████
████████████    ████      ████     ███████████████    ████      ████
████████████    ████      ████     ███████████████    ████      ████
[/red]
"""
    print(ascii_logo)
    typewriter("[green]>>> Loading deep port module...")
    typewriter("[yellow]>>> Awaiting target input...")

def run_nmap_port_scan(ip):
    try:
        result = subprocess.check_output(
            ["nmap", "-sS", "-Pn", "-p-", ip],
            stderr=subprocess.DEVNULL,
            encoding="utf-8"
        )
        return result
    except Exception as e:
        console.print(f"[bold red]Error running nmap:[/bold red] {e}")
        return ""

def parse_ports(output):
    ports = re.findall(r"(\d+)/tcp\s+open\s+(\S+)", output)
    return ports

def display_ports(ports):
    if not ports:
        console.print("[bold red]No open ports found.[/bold red]")
        return

    table = Table(title="[bold green]Open Ports[/bold green]")
    table.add_column("Port", style="cyan")
    table.add_column("Service", style="magenta")

    for port, service in ports:
        table.add_row(port, service)

    console.print(table)

if __name__ == "__main__":
    show_intro()
    ip = input("\n[?] Enter target IP address: ").strip()
    console.print(f"\n[bold yellow]>>> Scanning {ip}... Please wait.[/bold yellow]\n")
    output = run_nmap_port_scan(ip)
    open_ports = parse_ports(output)
    display_ports(open_ports)
