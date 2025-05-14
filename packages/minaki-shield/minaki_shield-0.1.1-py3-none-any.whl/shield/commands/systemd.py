import click
import os
import subprocess
from pathlib import Path

@click.command()
@click.option('--logfile', default='/var/log/auth.log', help='Log file to monitor')
@click.option('--log-to-file', is_flag=True, help='Enable logging to ~/.minakishield/shield.log')
@click.option('--json', 'json_output', is_flag=True, help='Output alerts as JSON')
@click.option('--webhook-url', help='Webhook URL for alerts (e.g., Slack)')
def systemd(logfile, log_to_file, json_output, webhook_url):
    """Generate and activate a systemd service for Shield."""

    # Create systemd user directory if it doesn't exist
    config_dir = Path.home() / ".config/systemd/user"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Build the command arguments
    args = f"--logfile {logfile}"
    if log_to_file:
        args += " --log-to-file"
    if json_output:
        args += " --json"
    if webhook_url:
        args += f" --webhook-url {webhook_url}"

    # Define the service file path and the executable path
    service_path = config_dir / "minakishield.service"
    shield_exec = os.path.expanduser("~/.local/bin/shield")

    # Systemd service content
    service_content = f"""[Unit]
Description=MinakiLabs Shield Intrusion Detection
After=network.target

[Service]
ExecStart={shield_exec} monitor {args}
WorkingDirectory={Path.home()}/.minakishield
Environment=PYTHONUNBUFFERED=1
Restart=always
RestartSec=5
StandardOutput=append:{Path.home()}/.minakishield/shield.log
StandardError=append:{Path.home()}/.minakishield/shield.log

[Install]
WantedBy=default.target
"""

    # Write the service file
    try:
        with open(service_path, 'w') as f:
            f.write(service_content)
        click.echo(f"✅ Systemd service created at: {service_path}")
    except Exception as e:
        click.echo(f"❌ Error writing service file: {e}")
        return

    # Restart and enable the service
    try:
        env = os.environ.copy()
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True, env=env)
        subprocess.run(["systemctl", "--user", "enable", "--now", "minakishield.service"], check=True, env=env)
        click.echo("🚀 MinakiShield service enabled and started!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to start service: {e}")

if __name__ == "__main__":
    systemd()
