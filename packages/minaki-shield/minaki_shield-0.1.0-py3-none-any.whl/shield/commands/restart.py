import click
import subprocess

@click.command()
def restart():
    """Restart Shield systemd service."""
    try:
        subprocess.run(["systemctl", "--user", "restart", "minakishield.service"], check=True)
        click.echo("🔁 Shield service restarted.")
    except subprocess.CalledProcessError:
        click.echo("❌ Failed to restart Shield.")
