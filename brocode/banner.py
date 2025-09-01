"""Banner display module for BroCode."""

import pyfiglet
from rich.console import Console
from rich.panel import Panel
from brocode import __version__

console = Console()

def show_banner():
    """Display BroCode ASCII banner with version."""
    banner = pyfiglet.figlet_format("BroCode", font="slant")
    banner_with_version = f"{banner}\n                    v{__version__}"
    console.print(Panel(banner_with_version, border_style="blue"))