"""
Workflow management commands for FluidGrids CLI
"""

import json
import click
from typing import Dict, Any, List

from ..utils import (
    console, display_table, display_json, create_spinner,
    load_json_file, format_datetime, safe_get_attr
)


@click.group(name="workflows")
def workflows():
    """Manage workflow definitions."""
    pass


@workflows.command(name="list")
@click.option("--limit", type=int, default=50, help="Maximum number of workflows to return")
@click.option("--offset", type=int, default=0, help="Offset for pagination")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def list_workflows(obj, limit, offset, output_json):
    """
    List all workflow definitions.
    """
    with create_spinner("Fetching workflows..."):
        workflows = obj.client.workflows.list(limit=limit, offset=offset)
    
    if output_json:
        display_json(workflows)
        return
    
    # Format for table display
    display_data = []
    for wf in workflows:
        display_data.append({
            "workflow_key": safe_get_attr(wf, "workflow_key"),
            "version": safe_get_attr(wf, "version"),
            "name": safe_get_attr(wf, "name"),
            "creator": safe_get_attr(wf, "creator"),
            "created_at": format_datetime(safe_get_attr(wf, "created_at")),
            "is_latest": "Yes" if safe_get_attr(wf, "is_latest", False) else "No"
        })
    
    display_table(
        display_data, 
        columns=["workflow_key", "version", "name", "creator", "created_at", "is_latest"]
    )


@workflows.command(name="get")
@click.argument("key", required=True)
@click.argument("version", required=False, default="latest")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def get_workflow(obj, key, version, output_json):
    """
    Get a specific workflow definition.
    
    KEY is the workflow key and VERSION is the version (default: latest).
    """
    with create_spinner(f"Fetching workflow {key} v{version}..."):
        workflow = obj.client.workflows.get(key, version)
    
    if output_json:
        display_json(workflow)
        return
    
    # Display workflow details
    console.print(f"[bold]Workflow: {safe_get_attr(workflow, 'name')}[/bold]")
    console.print(f"Key: {safe_get_attr(workflow, 'workflow_key')}")
    console.print(f"Version: {safe_get_attr(workflow, 'version')}")
    console.print(f"Description: {safe_get_attr(workflow, 'description')}")
    console.print(f"Created by: {safe_get_attr(workflow, 'creator')}")
    console.print(f"Created at: {format_datetime(safe_get_attr(workflow, 'created_at'))}")
    console.print(f"Updated at: {format_datetime(safe_get_attr(workflow, 'updated_at'))}")
    
    # Display node and edge counts
    definition_json = safe_get_attr(workflow, "definition_json", {})
    if isinstance(definition_json, str):
        try:
            definition_json = json.loads(definition_json)
        except:
            definition_json = {}
    
    data = definition_json.get("data", {})
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    console.print(f"Nodes: {len(nodes)}")
    console.print(f"Edges: {len(edges)}")
    
    # Offer to view full definition
    if click.confirm("View full workflow definition?"):
        display_json(definition_json)


@workflows.command(name="create")
@click.argument("file", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.pass_obj
def create_workflow(obj, file):
    """
    Create or update a workflow from a JSON file.
    
    FILE is the path to a JSON file containing the workflow definition.
    """
    # Load the workflow definition from the file
    definition = load_json_file(file)
    
    # Check that required fields are present
    required_fields = ["workflow_key", "version", "name", "definition_json"]
    missing_fields = [field for field in required_fields if field not in definition]
    if missing_fields:
        console.print(f"[bold red]Error: Missing required fields: {', '.join(missing_fields)}[/bold red]")
        return
    
    # Create or update the workflow
    with create_spinner(f"Creating workflow {definition['workflow_key']} v{definition['version']}..."):
        result = obj.client.workflows.create_or_update(
            workflow_key=definition["workflow_key"],
            version=definition["version"],
            name=definition["name"],
            description=definition.get("description", ""),
            definition_json=definition["definition_json"],
            context=definition.get("context")
        )
    
    console.print(f"[bold green]Workflow {safe_get_attr(result, 'workflow_key')} v{safe_get_attr(result, 'version')} created successfully![/bold green]")


@workflows.command(name="delete")
@click.argument("key", required=True)
@click.argument("version", required=True)
@click.option("--force", is_flag=True, help="Skip confirmation")
@click.pass_obj
def delete_workflow(obj, key, version, force):
    """
    Delete a workflow definition.
    
    KEY is the workflow key and VERSION is the version.
    """
    # Confirm deletion
    if not force and not click.confirm(f"Are you sure you want to delete workflow {key} v{version}?"):
        return
    
    # Delete the workflow
    with create_spinner(f"Deleting workflow {key} v{version}..."):
        obj.client.workflows.delete(key, version)
    
    console.print(f"[bold green]Workflow {key} v{version} deleted successfully![/bold green]")


@workflows.command(name="duplicate")
@click.argument("key", required=True)
@click.argument("version", required=False, default="latest")
@click.option("--new-key", help="New workflow key (default: same as source)")
@click.option("--new-version", help="New workflow version")
@click.option("--new-name", help="New workflow name")
@click.pass_obj
def duplicate_workflow(obj, key, version, new_key, new_version, new_name):
    """
    Duplicate a workflow definition.
    
    KEY is the source workflow key and VERSION is the source version (default: latest).
    """
    # Get the workflow to duplicate
    with create_spinner(f"Fetching workflow {key} v{version}..."):
        source = obj.client.workflows.get(key, version)
    
    # Determine new key, version, and name
    new_key = new_key or safe_get_attr(source, "workflow_key")
    source_version = safe_get_attr(source, "version")
    try:
        version_float = float(source_version)
        new_version = new_version or f"{version_float + 0.1:.1f}"
    except (ValueError, TypeError):
        new_version = new_version or f"{source_version}_copy"
    
    new_name = new_name or f"{safe_get_attr(source, 'name')} (Copy)"
    
    # Duplicate the workflow
    with create_spinner(f"Duplicating to {new_key} v{new_version}..."):
        result = obj.client.workflows.create_or_update(
            workflow_key=new_key,
            version=new_version,
            name=new_name,
            description=safe_get_attr(source, "description"),
            definition_json=safe_get_attr(source, "definition_json"),
            context=safe_get_attr(source, "context")
        )
    
    console.print(f"[bold green]Workflow duplicated to {safe_get_attr(result, 'workflow_key')} v{safe_get_attr(result, 'version')}![/bold green]") 