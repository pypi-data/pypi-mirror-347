"""
Configuration commands for FluidGrids CLI
"""

import os
import click
from typing import Dict, Any

from ..config import load_config, save_config, CONFIG_DIR, CONFIG_FILE
from ..utils import console, display_json, parse_key_value_pairs


@click.group(name="config")
def config():
    """Manage CLI configuration."""
    pass


@config.command(name="show")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def show_config(output_json):
    """
    Show current configuration.
    """
    config_data = load_config()
    
    if output_json:
        display_json(config_data)
        return
    
    console.print("[bold]Current Configuration:[/bold]")
    console.print(f"Configuration directory: {CONFIG_DIR}")
    console.print(f"Configuration file: {CONFIG_FILE}")
    console.print("")
    
    if not config_data:
        console.print("[yellow]No configuration found.[/yellow]")
        return
    
    for key, value in config_data.items():
        # Mask sensitive values
        if key in ["token", "api_key"]:
            if isinstance(value, str):
                value = value[:5] + "..." if len(value) > 5 else "*****"
        
        console.print(f"{key}: {value}")


@config.command(name="set")
@click.argument("key_value_pairs", nargs=-1)
def set_config(key_value_pairs):
    """
    Set configuration values.
    
    Provide key-value pairs as KEY=VALUE. For example:
    
    fluidgrids config set api_url=https://api.example.com
    """
    if not key_value_pairs:
        console.print("[yellow]No key-value pairs provided.[/yellow]")
        return
    
    # Parse key-value pairs
    values = parse_key_value_pairs(key_value_pairs)
    
    # Update configuration
    config_data = load_config()
    for key, value in values.items():
        config_data[key] = value
    
    # Save configuration
    save_config(config_data)
    
    console.print("[bold green]Configuration updated successfully![/bold green]")
    for key, value in values.items():
        console.print(f"Set {key} = {value}")


@config.command(name="unset")
@click.argument("keys", nargs=-1)
def unset_config(keys):
    """
    Remove configuration values.
    
    Provide keys to remove. For example:
    
    fluidgrids config unset api_url
    """
    if not keys:
        console.print("[yellow]No keys provided.[/yellow]")
        return
    
    # Update configuration
    config_data = load_config()
    removed = []
    
    for key in keys:
        if key in config_data:
            del config_data[key]
            removed.append(key)
    
    # Save configuration
    save_config(config_data)
    
    if removed:
        console.print("[bold green]Configuration updated successfully![/bold green]")
        console.print(f"Removed: {', '.join(removed)}")
    else:
        console.print("[yellow]No matching keys found in configuration.[/yellow]")


@config.command(name="clear")
@click.option("--force", is_flag=True, help="Skip confirmation")
def clear_config(force):
    """
    Clear all configuration.
    """
    if not force and not click.confirm("Are you sure you want to clear all configuration?"):
        return
    
    # Save empty configuration
    save_config({})
    
    console.print("[bold green]Configuration cleared successfully![/bold green]") 