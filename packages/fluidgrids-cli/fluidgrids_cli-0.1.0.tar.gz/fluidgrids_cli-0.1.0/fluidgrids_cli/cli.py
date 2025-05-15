"""
Main CLI entry point for FluidGrids
"""

import os
import sys
import click
from rich.console import Console
from typing import Optional, Dict, Any

from fluidgrids import FluidGridsClient

from . import __version__
from .config import get_credentials, load_config
from .utils import console, handle_error
from .commands import (
    auth_commands,
    workflow_commands,
    run_commands,
    config_commands,
    credential_commands,
    ai_commands,
    usage_commands,
    dashboard_commands,
    search_commands,
    node_commands,
)

# Create a Click context object for passing the client
class CliContext:
    def __init__(self):
        self.client = None
        self.config = None


def create_client() -> FluidGridsClient:
    """Create a client instance using stored credentials."""
    creds = get_credentials()
    
    # Check if we have credentials
    if not creds["api_url"]:
        handle_error("API URL not configured. Run 'fluidgrids auth login --url URL' first.")
    
    # Create the client based on the credentials we have
    try:
        # API key authentication
        if creds["api_key"]:
            return FluidGridsClient(
                base_url=creds["api_url"],
                api_key=creds["api_key"]
            )
        # Token authentication
        elif creds["token"]:
            return FluidGridsClient(
                base_url=creds["api_url"],
                token=creds["token"]
            )
        # Username/password authentication
        elif creds["username"] and creds["password"]:
            return FluidGridsClient(
                base_url=creds["api_url"],
                username=creds["username"],
                password=creds["password"]
            )
        else:
            handle_error("No credentials found. Run 'fluidgrids auth login' first.")
    except Exception as e:
        handle_error(f"Failed to create client: {str(e)}")


@click.group()
@click.version_option(version=__version__, prog_name="FluidGrids CLI")
@click.pass_context
def cli(ctx):
    """
    FluidGrids CLI - Command-line interface for the FluidGrids Workflow Engine
    
    Use this tool to manage workflows, trigger runs, and more.
    """
    # Initialize the context object
    ctx.obj = CliContext()
    ctx.obj.config = load_config()
    
    # Skip client creation for auth and config commands
    parent_command = ctx.invoked_subcommand.split(' ')[0] if ctx.invoked_subcommand else None
    if parent_command not in ["auth", "config"]:
        ctx.obj.client = create_client()


# Add command groups
cli.add_command(auth_commands.auth)
cli.add_command(workflow_commands.workflows)
cli.add_command(run_commands.runs)
cli.add_command(config_commands.config)
cli.add_command(credential_commands.credentials)
cli.add_command(ai_commands.ai)
cli.add_command(usage_commands.usage)
cli.add_command(dashboard_commands.dashboard)
cli.add_command(search_commands.search)
cli.add_command(node_commands.nodes)


def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main() 