"""
Node management commands for FluidGrids CLI
"""

import click
from typing import Dict, Any, List

from ..utils import console, display_table, display_json, create_spinner


@click.group(name="nodes")
def nodes():
    """Manage workflow node types and operations."""
    pass


@nodes.command(name="list")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def list_nodes(obj, output_json):
    """
    List all registered node types.
    
    This command shows all node types available for use in workflows.
    """
    with create_spinner("Fetching node types..."):
        nodes_list = obj.client.nodes.list()
    
    if output_json:
        display_json(nodes_list)
        return
    
    # Format for table display
    display_data = []
    for node in nodes_list:
        display_data.append({
            "node_type": node.get("node_type", "Unknown"),
            "version": node.get("node_version", "Unknown"),
            "kind": ", ".join(node.get("kind", [])),
            "description": node.get("description", "")
        })
    
    # Sort by node type and version
    display_data.sort(key=lambda x: (x["node_type"], x["version"]))
    
    console.print(f"[bold]Available Node Types[/bold] ({len(display_data)})")
    display_table(display_data, columns=["node_type", "version", "kind", "description"])


@nodes.command(name="get")
@click.argument("node_type", required=True)
@click.argument("version", required=True)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def get_node_manifest(obj, node_type, version, output_json):
    """
    Get detailed manifest for a specific node type.
    
    NODE_TYPE is the type of the node (e.g., action:http).
    VERSION is the version of the node.
    
    Example:
    
    fluidgrids nodes get action:http 1.0
    """
    with create_spinner(f"Fetching manifest for {node_type} v{version}..."):
        manifest = obj.client.nodes.get_manifest(node_type, version)
    
    if output_json:
        display_json(manifest)
        return
    
    # Display manifest details
    console.print(f"[bold]Node: {manifest.get('node_type')} v{manifest.get('version')}[/bold]")
    console.print(f"Description: {manifest.get('description', '')}")
    console.print(f"Kind: {', '.join(manifest.get('kind', []))}")
    
    # Display input schema
    input_schema = manifest.get("input_schema", {})
    if input_schema:
        console.print("\n[bold]Input Schema:[/bold]")
        properties = input_schema.get("properties", {})
        required = input_schema.get("required", [])
        
        for prop_name, prop_info in properties.items():
            prop_type = prop_info.get("type", "any")
            is_required = " (required)" if prop_name in required else ""
            description = prop_info.get("description", "")
            
            console.print(f"  {prop_name}: {prop_type}{is_required}")
            if description:
                console.print(f"    {description}")
    
    # Display output schema
    output_schema = manifest.get("output_schema", {})
    if output_schema:
        console.print("\n[bold]Output Schema:[/bold]")
        properties = output_schema.get("properties", {})
        
        for prop_name, prop_info in properties.items():
            prop_type = prop_info.get("type", "any")
            description = prop_info.get("description", "")
            
            console.print(f"  {prop_name}: {prop_type}")
            if description:
                console.print(f"    {description}")
    
    # Display configuration schema if available
    config_schema = manifest.get("config_schema", {})
    if config_schema:
        console.print("\n[bold]Configuration Schema:[/bold]")
        properties = config_schema.get("properties", {})
        required = config_schema.get("required", [])
        
        for prop_name, prop_info in properties.items():
            prop_type = prop_info.get("type", "any")
            is_required = " (required)" if prop_name in required else ""
            description = prop_info.get("description", "")
            
            console.print(f"  {prop_name}: {prop_type}{is_required}")
            if description:
                console.print(f"    {description}")


@nodes.command(name="test")
@click.argument("node_type", required=True)
@click.argument("version", required=True)
@click.option("--input", "input_data", help="JSON string with input data")
@click.option("--input-file", type=click.Path(exists=True), help="JSON file with input data")
@click.option("--config", help="JSON string with configuration data")
@click.option("--config-file", type=click.Path(exists=True), help="JSON file with configuration data")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def test_node(obj, node_type, version, input_data, input_file, config, config_file, output_json):
    """
    Test a node by executing it with sample inputs.
    
    NODE_TYPE is the type of the node (e.g., action:http).
    VERSION is the version of the node.
    """
    # Load input data
    input_dict = {}
    if input_data:
        input_dict = click.json.loads(input_data)
    elif input_file:
        with open(input_file, "r") as f:
            input_dict = click.json.loads(f.read())
    
    # Load config data
    config_dict = {}
    if config:
        config_dict = click.json.loads(config)
    elif config_file:
        with open(config_file, "r") as f:
            config_dict = click.json.loads(f.read())
    
    # Test the node
    with create_spinner(f"Testing {node_type} v{version}..."):
        result = obj.client.nodes.test(
            node_type=node_type,
            node_version=version,
            input_data=input_dict,
            config=config_dict
        )
    
    if output_json:
        display_json(result)
        return
    
    # Display test results
    console.print(f"[bold]Test Results for {node_type} v{version}[/bold]")
    
    status = result.get("status", "unknown")
    if status == "success":
        console.print("[bold green]Success![/bold green]")
    else:
        console.print(f"[bold red]Failed: {result.get('error', 'Unknown error')}[/bold red]")
    
    # Display execution time
    execution_time = result.get("execution_time_ms")
    if execution_time:
        console.print(f"Execution Time: {execution_time} ms")
    
    # Display output data
    output_data = result.get("output")
    if output_data:
        console.print("\n[bold]Output:[/bold]")
        display_json(output_data)
    
    # Display logs if available
    logs = result.get("logs", [])
    if logs:
        console.print("\n[bold]Execution Logs:[/bold]")
        for log in logs:
            level = log.get("level", "INFO")
            message = log.get("message", "")
            
            if level == "ERROR":
                console.print(f"[red]{level}: {message}[/red]")
            elif level == "WARNING":
                console.print(f"[yellow]{level}: {message}[/yellow]")
            else:
                console.print(f"{level}: {message}") 