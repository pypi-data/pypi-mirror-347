import click
import os
import subprocess
from pathlib import Path

@click.command()
def uninstall():
    """Uninstall MinakiShield systemd service and stop monitoring."""
    user_service_path = Path.home() / ".config/systemd/user/minakishield.service"
    system_service_path = Path("/etc/systemd/system/minakishield.service")

    # Stop any running service
    click.echo("🛑 Stopping any running MinakiShield services...")

    subprocess.run(["systemctl", "--user", "stop", "minakishield.service"], stderr=subprocess.DEVNULL)
    subprocess.run(["systemctl", "--user", "disable", "minakishield.service"], stderr=subprocess.DEVNULL)

    subprocess.run(["sudo", "systemctl", "stop", "minakishield.service"], stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "systemctl", "disable", "minakishield.service"], stderr=subprocess.DEVNULL)

    # Remove user-level service
    if user_service_path.exists():
        user_service_path.unlink()
        click.echo("🧹 Removed user systemd service.")

    # Remove system-level service
    if system_service_path.exists():
        subprocess.run(["sudo", "rm", str(system_service_path)])
        click.echo("🧹 Removed system-wide systemd service.")

    subprocess.run(["systemctl", "--user", "daemon-reexec"], stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "systemctl", "daemon-reexec"], stderr=subprocess.DEVNULL)

    click.echo("✅ MinakiShield systemd services have been uninstalled.")
