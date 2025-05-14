import click
import subprocess

@click.command()
def stop():
    """Stop Shield systemd service."""
    try:
        subprocess.run(["systemctl", "--user", "stop", "minakishield.service"], check=True)
        click.echo("🛑 Shield service stopped via systemd.")
    except subprocess.CalledProcessError:
        click.echo("❌ Failed to stop shield. Is it installed?")
