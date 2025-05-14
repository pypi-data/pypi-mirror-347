# pylint: disable=consider-using-with,import-outside-toplevel
"""Command line utilities."""
import subprocess
import sys
import time

import requests
import typer

from . import config

app = typer.Typer(help="Linalgo CLI", no_args_is_help=True)
config_app = typer.Typer(help="Configuration commands", no_args_is_help=True)
hub_app = typer.Typer(help="Linhub commands")

app.add_typer(config_app, name="config")
app.add_typer(hub_app, name="hub")


def _get_user_credentials(username=None, password=None):
    """Get username and password from user or config."""
    # Get the server URL from config or prompt
    server_url = config.get_config('hub.server_url')
    if not server_url:
        server_url = typer.prompt(
            "Enter hub server URL",
            default="http://localhost:8000/v1",
            show_default=True
        )
        config.set_config("hub.server_url", server_url)

    # Get credentials - use saved username as default if available
    if not username:
        saved_username = config.get_config('hub.username')
        if saved_username:
            username = typer.prompt(
                "Username", default=saved_username, show_default=True)
        else:
            username = typer.prompt("Username")

    if not password:
        password = typer.prompt("Password", hide_input=True)

    return server_url, username, password


def _handle_organizations(client):
    """Handle organization selection and save to config."""
    orgs = client.get_organizations()
    if not orgs or len(orgs) == 0:
        typer.echo("No organizations found.")
        return False

    # Default to first org
    org = orgs[0]

    # Let user select an organization if there are multiple
    if len(orgs) > 1:
        typer.echo("\nAvailable organizations:")
        for i, org in enumerate(orgs):
            typer.echo(f"{i+1}. {org['name']} (ID: {org['id']})")
        org_choice = typer.prompt(
            "Select organization number",
            type=int,
            default=1,
            show_default=True
        )
        org = orgs[org_choice-1]

    # Save organization info including UUID
    config.set_config("hub.organization", org['id'])
    config.set_config("hub.organization_name", org['name'])
    typer.echo(f"Organization set to: {org['name']}")
    return True


@app.command()
def login(username: str = None, password: str = None):
    """Login to the Linalgo hub and save authentication token."""
    server_url, username, password = _get_user_credentials(username, password)

    # Login to get token
    url = f"{server_url}/auth/token/login/"
    try:
        response = requests.post(
            url,
            data={"username": username, "password": password},
            timeout=30
        )

        if response.status_code != 200:
            typer.echo(
                f"Error: Login failed (HTTP {response.status_code})", err=True)
            if response.text:
                typer.echo(f"Details: {response.text}", err=True)
            return False

        token_data = response.json()
        if 'auth_token' not in token_data:
            typer.echo("Error: Unexpected response format", err=True)
            return False

        # Extract and save token
        token = token_data['auth_token']
        config.set_config("hub.token", token)
        config.set_config("hub.username", username)
        typer.echo("Login successful! Token saved.")

        # Get organization info
        typer.echo("Fetching organization information...")
        try:
            # Create a temporary client to get organization info
            from linalgo.hub.client import LinalgoClient
            client = LinalgoClient(token=token, api_url=server_url)
            _handle_organizations(client)
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught
            typer.echo(
                f"Warning: Could not fetch organization info: {str(e)}", err=True)
            return True
    except Exception as e:  # pylint: disable=broad-exception-caught
        typer.echo(f"Error: {str(e)}", err=True)
        return False


def run_server_in_background():
    """Run the linhub server in the background."""
    try:
        # Don't use 'with' here as we need to return the process for later termination
        process = subprocess.Popen(
            ["linhub", "runserver"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # Ensure the process runs in the background
            start_new_session=True
        )
        # Give the process a moment to start
        time.sleep(0.5)
        # Make sure the process is still running
        if process.poll() is not None:
            exit_code = process.returncode
            typer.echo(
                f"Server process exited with code {exit_code}", err=True)
            stdout, stderr = process.communicate()
            if stdout:
                typer.echo(
                    f"Server output: {stdout.decode('utf-8')}", err=True)
            if stderr:
                typer.echo(f"Server error: {stderr.decode('utf-8')}", err=True)
            return None
        return process
    except Exception as e:  # pylint: disable=broad-exception-caught
        typer.echo(f"Error starting server: {e}", err=True)
        return None


def wait_for_server(max_attempts=10, delay=2):
    """Wait for the server to be ready."""
    server_url = "http://localhost:8000"

    typer.echo("Waiting for server to start...")

    for attempt in range(max_attempts):
        try:
            response = requests.get(server_url, timeout=5)
            if response.status_code == 200:
                typer.echo("Server is ready!")
                return True
        except requests.RequestException:
            # We expect connection errors until the server is ready
            pass

        time.sleep(delay)
        typer.echo(f"Waiting for server... ({attempt + 1}/{max_attempts})")

    typer.echo("Server did not become ready in time", err=True)
    return False


def _setup_local_server(username, org_name, password):
    """Set up and initialize local hub server."""
    typer.echo("\nInitializing local hub server...")
    try:
        init_cmd = [
            "linhub", "init",
            "--username", username,
            "--org-name", org_name,
            "--password", password
        ]
        subprocess.run(init_cmd, check=True)

        # Start the server in the background
        typer.echo("\nStarting the server...")
        server_process = run_server_in_background()
        if not server_process:
            typer.echo("Failed to start server. Please check if linhub is "
                       "installed correctly.", err=True)
            return False

        server_ready = wait_for_server()
        if not server_ready:
            typer.echo(
                "Server started but did not become ready. Stopping server...", err=True)
            server_process.terminate()
            return False

        typer.echo("\nAttempting to login to local server...")
        if login(username=username, password=password):
            typer.echo("Login successful!")
        else:
            typer.echo(
                "Login failed. You can try again later with 'linalgo login'")

        typer.echo("\nStopping server...")
        # Make sure to terminate the process properly
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # If it doesn't terminate gracefully, kill it
            server_process.kill()

        typer.echo("Server stopped.")
        typer.echo(
            "Initialization complete! You can start the server again "
            "with 'linalgo hub runserver'")
        return True

    except subprocess.CalledProcessError as e:
        typer.echo(f"Error initializing local hub server: {e}", err=True)
        return False


@app.command()
def init():
    """Initialize linalgo configuration with interactive prompts."""
    try:
        # Check if linhub is installed
        __import__('linhub')
    except ImportError:
        print("Error: linalgo[hub] is not installed. Please install it using:")
        print("pip install linalgo[hub]")
        sys.exit(1)

    # Get user input using typer prompts
    username = typer.prompt("Enter your username")
    org_name = typer.prompt("Enter organization name")
    server_url = typer.prompt(
        "Enter hub server URL",
        default="http://localhost:8000/v1",
        show_default=True
    )

    # Get password (will be reused for login)
    password = typer.prompt("Enter your password", hide_input=True)

    # Save to config
    config.set_config("hub.username", username)
    config.set_config("hub.organization", org_name)
    config.set_config("hub.server_url", server_url)

    typer.echo("\nConfiguration saved successfully!")
    typer.echo(f"Username: {username}")
    typer.echo(f"Organization: {org_name}")
    typer.echo(f"Server URL: {server_url}")

    # If using localhost, run linhub init with username and org
    if server_url.startswith("http://localhost"):
        try:
            if not _setup_local_server(username, org_name, password):
                sys.exit(1)
        except KeyboardInterrupt:
            typer.echo("\nSetup interrupted by user.")
            sys.exit(0)


def check_linhub_installed():
    """Check if linhub is installed."""
    try:
        __import__('linhub')
        return True
    except ImportError:
        typer.echo(
            "Error: linalgo[hub] is not installed. Please install it using:", err=True)
        typer.echo("pip install linalgo[hub]", err=True)
        return False


@hub_app.callback(invoke_without_command=True)
def hub_callback(ctx: typer.Context):
    """Commands for interacting with Linhub."""
    # If no command is provided, show help
    if ctx.invoked_subcommand is None:
        if not check_linhub_installed():
            sys.exit(1)
        try:
            subprocess.run(["linhub", "--help"], check=True)
        except subprocess.CalledProcessError as e:
            typer.echo(f"Error running linhub: {e}", err=True)
            sys.exit(1)


@hub_app.command(
    name="",
    hidden=True,
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True
    }
)
def hub_passthrough(ctx: typer.Context):  # pylint: disable=unused-argument
    """Pass all commands and arguments to linhub."""
    if not check_linhub_installed():
        sys.exit(1)

    args = sys.argv[sys.argv.index("hub") + 1:]

    try:
        subprocess.run(["linhub"] + args, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error running linhub: {e}", err=True)
        sys.exit(1)


@config_app.callback()
def config_callback():
    """Commands for managing configuration."""


@config_app.command()
def show():
    """Show all configuration values."""
    config_data = config.load_config()
    if not config_data:
        print("No configuration found")
        return

    for key, value in config_data.items():
        print(f"{key} = {value}")


@config_app.command()
def get(key: str):
    """Get a configuration value."""
    value = config.get_config(key)
    if value is None:
        print(f"No value found for key: {key}")
        sys.exit(1)
    print(value)


@config_app.command()
def config_set(key: str, value: str):
    """Set a configuration value."""
    try:
        config.set_config(key, value)
        print(f"Set {key} = {value}")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error setting configuration: {e}")
        sys.exit(1)


@config_app.command()
def load(env_file: str = ".env"):
    """Load configuration from .env file."""
    try:
        # Check if function exists before calling
        if hasattr(config, 'load_env_file'):
            config.load_env_file(env_file)
            print(f"Configuration loaded from {env_file}")
        else:
            print("Error: load_env_file function not available in config module")
            sys.exit(1)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error loading configuration: {e}")
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    # Special handling of hub commands
    if len(sys.argv) > 1 and sys.argv[1] == "hub" and len(sys.argv) > 2:
        if not check_linhub_installed():
            sys.exit(1)

        # Extract all arguments after "hub"
        hub_args = sys.argv[2:]

        # Run linhub with the arguments
        try:
            subprocess.run(["linhub"] + hub_args, check=True)
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            typer.echo(f"Error running linhub: {e}", err=True)
            sys.exit(1)

    app()


if __name__ == "__main__":
    main()
