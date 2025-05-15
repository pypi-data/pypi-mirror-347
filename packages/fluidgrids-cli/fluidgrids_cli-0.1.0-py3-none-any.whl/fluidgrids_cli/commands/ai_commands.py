"""
AI-assisted workflow management commands for FluidGrids CLI
"""

import click
from typing import Dict, Any

from ..utils import console, display_json, create_spinner


@click.group(name="ai")
def ai():
    """Use AI to manage workflows with natural language."""
    pass


@ai.command(name="manage")
@click.argument("prompt", required=True)
@click.option("--workflow-key", help="Target workflow key")
@click.option("--workflow-version", help="Target workflow version")
@click.option("--model", help="AI model to use")
@click.option("--role", help="Caller role for AI")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def manage_workflow(obj, prompt, workflow_key, workflow_version, model, role, output_json):
    """
    Use AI to manage workflows based on natural language prompts.
    
    PROMPT is a natural language description of what you want the AI to do.
    
    Examples:
    
    fluidgrids ai manage "Create a workflow that reads from a CSV file, filters rows where status equals 'active', and writes the results to a new file"
    
    fluidgrids ai manage "Add error handling to my workflow" --workflow-key my-workflow --workflow-version latest
    """
    # Build parameters
    params = {
        "prompt": prompt,
    }
    
    if workflow_key:
        params["target_workflow_key"] = workflow_key
    if workflow_version:
        params["target_workflow_version"] = workflow_version
    if model:
        params["model"] = model
    if role:
        params["caller_role"] = role
    
    # Call the AI
    with create_spinner("AI is processing your request..."):
        result = obj.client.ai.manage_workflow(**params)
    
    if output_json:
        display_json(result)
        return
    
    # Display results
    if result.get("status") == "success":
        console.print("[bold green]AI completed successfully![/bold green]")
    else:
        console.print("[bold yellow]AI completed with some issues.[/bold yellow]")
    
    # Display explanation
    if result.get("explanation"):
        console.print("\n[bold]AI Explanation:[/bold]")
        console.print(result["explanation"])
    
    # Display executed plan
    if result.get("executed_plan"):
        console.print("\n[bold]Executed Plan:[/bold]")
        for step in result["executed_plan"]:
            step_status = step.get("status", "unknown")
            
            # Format based on status
            if step_status == "success":
                status_str = "[green]✓[/green]"
            elif step_status == "failure":
                status_str = "[red]✗[/red]"
            else:
                status_str = "[yellow]?[/yellow]"
                
            console.print(f"{status_str} {step.get('description', 'Unknown step')}")
            
            # Show error if step failed
            if step_status == "failure" and step.get("error"):
                console.print(f"  [red]Error: {step['error']}[/red]")
    
    # Display generated workflow information if available
    if result.get("created_workflows") or result.get("updated_workflows"):
        console.print("\n[bold]Affected Workflows:[/bold]")
        
        if result.get("created_workflows"):
            console.print("[bold]Created:[/bold]")
            for wf in result["created_workflows"]:
                console.print(f"  - {wf['workflow_key']} v{wf['version']}: {wf.get('name', '')}")
        
        if result.get("updated_workflows"):
            console.print("[bold]Updated:[/bold]")
            for wf in result["updated_workflows"]:
                console.print(f"  - {wf['workflow_key']} v{wf['version']}: {wf.get('name', '')}")
    
    # Offer to view full result
    if not output_json and click.confirm("View full AI response?"):
        display_json(result) 