"""
Credential management commands for FluidGrids CLI
"""

import json
import click
from typing import Dict, Any, List

from ..utils import (
    console, display_table, display_json, create_spinner,
    load_json_file, format_datetime, parse_json_object
)


@click.group(name="credentials")
def credentials():
    """Manage credentials for workflows."""
    pass


@credentials.command(name="list")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def list_credentials(obj, output_json):
    """
    List all available credentials.
    """
    with create_spinner("Fetching credentials..."):
        credentials = obj.client.credentials.list()
    
    if output_json:
        display_json(credentials)
        return
    
    # Format for table display
    display_data = []
    for cred in credentials:
        display_data.append({
            "credential_id": cred.credential_id,
            "name": cred.name,
            "type": cred.type,
            "created_at": format_datetime(cred.created_at),
            "updated_at": format_datetime(cred.updated_at),
        })
    
    display_table(
        display_data, 
        columns=["credential_id", "name", "type", "created_at", "updated_at"]
    )


@credentials.command(name="get")
@click.argument("credential_id", required=True)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--show-config", is_flag=True, help="Show credential configuration (may contain sensitive info)")
@click.pass_obj
def get_credential(obj, credential_id, output_json, show_config):
    """
    Get details about a specific credential.
    
    CREDENTIAL_ID is the ID of the credential.
    """
    with create_spinner(f"Fetching credential {credential_id}..."):
        credential = obj.client.credentials.get(credential_id)
    
    if output_json:
        if not show_config:
            # Remove config if not requested
            credential_dict = credential.dict() if hasattr(credential, "dict") else credential
            if isinstance(credential_dict, dict) and "config" in credential_dict:
                credential_dict["config"] = "*** REDACTED ***"
            display_json(credential_dict)
        else:
            display_json(credential)
        return
    
    # Display credential details
    console.print(f"[bold]Credential: {credential.name}[/bold]")
    console.print(f"ID: {credential.credential_id}")
    console.print(f"Type: {credential.type}")
    console.print(f"Created at: {format_datetime(credential.created_at)}")
    console.print(f"Updated at: {format_datetime(credential.updated_at)}")
    
    # Display config if requested
    if show_config and hasattr(credential, "config"):
        console.print("\n[bold]Configuration:[/bold]")
        display_json(credential.config)
    elif hasattr(credential, "config"):
        console.print("\n[yellow]Configuration redacted. Use --show-config to display.[/yellow]")


@credentials.command(name="create")
@click.argument("file", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.pass_obj
def create_credential(obj, file):
    """
    Create a new credential from a JSON file.
    
    FILE is the path to a JSON file containing the credential definition.
    Example credential JSON:
    
    {
        "name": "My API Credential",
        "type": "api_key",
        "config": {
            "api_key": "your-api-key",
            "base_url": "https://api.example.com"
        }
    }
    """
    # Load the credential definition from the file
    definition = load_json_file(file)
    
    # Check that required fields are present
    required_fields = ["name", "type", "config"]
    missing_fields = [field for field in required_fields if field not in definition]
    if missing_fields:
        console.print(f"[bold red]Error: Missing required fields: {', '.join(missing_fields)}[/bold red]")
        return
    
    # Create the credential
    with create_spinner(f"Creating credential '{definition['name']}'..."):
        result = obj.client.credentials.create(definition)
    
    console.print(f"[bold green]Credential created successfully![/bold green]")
    console.print(f"Credential ID: {result.credential_id}")


@credentials.command(name="update")
@click.argument("credential_id", required=True)
@click.argument("file", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.pass_obj
def update_credential(obj, credential_id, file):
    """
    Update an existing credential from a JSON file.
    
    CREDENTIAL_ID is the ID of the credential to update.
    FILE is the path to a JSON file containing the credential update.
    
    Example credential update JSON:
    
    {
        "name": "Updated API Credential",
        "config": {
            "api_key": "new-api-key",
            "base_url": "https://api.example.com"
        }
    }
    """
    # Load the credential update from the file
    update = load_json_file(file)
    
    # Update the credential
    with create_spinner(f"Updating credential {credential_id}..."):
        result = obj.client.credentials.update(credential_id, update)
    
    console.print(f"[bold green]Credential updated successfully![/bold green]")


@credentials.command(name="delete")
@click.argument("credential_id", required=True)
@click.option("--force", is_flag=True, help="Skip confirmation")
@click.pass_obj
def delete_credential(obj, credential_id, force):
    """
    Delete a credential.
    
    CREDENTIAL_ID is the ID of the credential to delete.
    """
    # Confirm deletion
    if not force and not click.confirm(f"Are you sure you want to delete credential {credential_id}?"):
        return
    
    # Delete the credential
    with create_spinner(f"Deleting credential {credential_id}..."):
        obj.client.credentials.delete(credential_id)
    
    console.print(f"[bold green]Credential deleted successfully![/bold green]") 