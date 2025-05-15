"""
Workflow run commands for FluidGrids CLI
"""

import json
import time
import click
from typing import Dict, Any, List

from ..utils import (
    console, display_table, display_json, create_spinner,
    load_json_file, format_datetime, parse_json_object
)


@click.group(name="runs")
def runs():
    """Manage workflow runs."""
    pass


@runs.command(name="list")
@click.option("--workflow-key", help="Filter by workflow key")
@click.option("--status", help="Filter by status (PENDING, RUNNING, COMPLETED, FAILED, etc.)")
@click.option("--limit", type=int, default=50, help="Maximum number of runs to return")
@click.option("--offset", type=int, default=0, help="Offset for pagination")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def list_runs(obj, workflow_key, status, limit, offset, output_json):
    """
    List workflow runs.
    """
    # Build filters
    filters = {}
    if workflow_key:
        filters["workflow_key"] = workflow_key
    if status:
        filters["status"] = status
    
    with create_spinner("Fetching workflow runs..."):
        runs = obj.client.runs.list(
            limit=limit,
            offset=offset,
            **filters
        )
    
    if output_json:
        display_json(runs)
        return
    
    # Format for table display
    display_data = []
    for run in runs:
        display_data.append({
            "run_id": run.run_id,
            "workflow_key": run.workflow_key,
            "version": run.workflow_version,
            "status": run.status,
            "started_at": format_datetime(run.started_at),
            "completed_at": format_datetime(run.completed_at),
        })
    
    display_table(
        display_data, 
        columns=["run_id", "workflow_key", "version", "status", "started_at", "completed_at"]
    )


@runs.command(name="get")
@click.argument("run_id", required=True)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def get_run(obj, run_id, output_json):
    """
    Get details about a specific workflow run.
    
    RUN_ID is the ID of the workflow run.
    """
    with create_spinner(f"Fetching run {run_id}..."):
        run = obj.client.runs.get(run_id)
    
    if output_json:
        display_json(run)
        return
    
    # Display run details
    console.print(f"[bold]Run: {run.run_id}[/bold]")
    console.print(f"Workflow: {run.workflow_key} v{run.workflow_version}")
    console.print(f"Status: {run.status}")
    console.print(f"Started at: {format_datetime(run.started_at)}")
    console.print(f"Completed at: {format_datetime(run.completed_at)}")
    
    # Display context/inputs
    if hasattr(run, "context") and run.context:
        console.print("\n[bold]Context/Inputs:[/bold]")
        display_json(run.context)
    
    # Display outputs
    if hasattr(run, "outputs") and run.outputs:
        console.print("\n[bold]Outputs:[/bold]")
        display_json(run.outputs)
    
    # Display status history if available
    if hasattr(run, "status_history") and run.status_history:
        console.print("\n[bold]Status History:[/bold]")
        for status in run.status_history:
            console.print(f"  {format_datetime(status.timestamp)}: {status.status}")


@runs.command(name="trigger")
@click.argument("workflow_key", required=True)
@click.argument("version", required=False, default="latest")
@click.option("--context", help="JSON context/inputs for the workflow")
@click.option("--context-file", type=click.Path(exists=True), help="File containing JSON context/inputs")
@click.option("--async", "is_async", is_flag=True, help="Trigger asynchronously and return immediately")
@click.option("--wait", is_flag=True, help="Wait for the run to complete")
@click.option("--timeout", type=int, default=300, help="Timeout in seconds when waiting (default: 300)")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def trigger_run(obj, workflow_key, version, context, context_file, is_async, wait, timeout, output_json):
    """
    Trigger a workflow run.
    
    WORKFLOW_KEY is the key of the workflow to run and VERSION is the version (default: latest).
    """
    # Get context from options
    if context and context_file:
        console.print("[bold red]Error: Cannot specify both --context and --context-file[/bold red]")
        return
    
    run_context = {}
    if context:
        run_context = parse_json_object(context)
    elif context_file:
        run_context = load_json_file(context_file)
    
    # Trigger the run
    with create_spinner(f"Triggering workflow {workflow_key} v{version}..."):
        run = obj.client.runs.trigger(
            workflow_key=workflow_key,
            version=version,
            context=run_context,
            async_execution=is_async
        )
    
    console.print(f"[bold green]Run triggered: {run.run_id}[/bold green]")
    
    # Wait for completion if requested
    if wait and not is_async:
        console.print("Waiting for run to complete...")
        
        start_time = time.time()
        last_status = None
        
        while time.time() - start_time < timeout:
            current_run = obj.client.runs.get(run.run_id)
            
            # Print status if it changed
            if current_run.status != last_status:
                console.print(f"Status: {current_run.status}")
                last_status = current_run.status
            
            # Break if run is finished
            if current_run.status in ["COMPLETED", "FAILED", "CANCELED"]:
                run = current_run
                break
            
            # Wait before checking again
            time.sleep(2)
        else:
            console.print("[yellow]Timeout reached while waiting for run to complete[/yellow]")
    
    # Display run details
    if output_json:
        display_json(run)
    else:
        console.print(f"Run ID: {run.run_id}")
        console.print(f"Status: {run.status}")


@runs.command(name="cancel")
@click.argument("run_id", required=True)
@click.pass_obj
def cancel_run(obj, run_id):
    """
    Cancel a running workflow.
    
    RUN_ID is the ID of the workflow run.
    """
    with create_spinner(f"Canceling run {run_id}..."):
        obj.client.runs.cancel(run_id)
    
    console.print(f"[bold green]Run {run_id} canceled successfully![/bold green]")


@runs.command(name="logs")
@click.argument("run_id", required=True)
@click.option("--follow", "-f", is_flag=True, help="Follow logs in real-time")
@click.option("--timeout", type=int, default=300, help="Timeout in seconds when following (default: 300)")
@click.pass_obj
def get_run_logs(obj, run_id, follow, timeout):
    """
    Get logs for a workflow run.
    
    RUN_ID is the ID of the workflow run.
    """
    # Get initial logs
    with create_spinner(f"Fetching logs for run {run_id}..."):
        logs = obj.client.runs.get_logs(run_id)
    
    # Display logs
    if logs:
        for log in logs:
            console.print(f"[{format_datetime(log.timestamp)}] [{log.level}] {log.message}")
    else:
        console.print("No logs found.")
    
    # Follow logs if requested
    if follow:
        console.print("\n[bold]Following logs in real-time...[/bold] (Press Ctrl+C to stop)")
        
        start_time = time.time()
        last_log_id = logs[-1].log_id if logs else None
        
        try:
            while time.time() - start_time < timeout:
                # Get run status to check if it's still running
                run = obj.client.runs.get(run_id)
                if run.status not in ["PENDING", "RUNNING", "PAUSED"]:
                    console.print(f"\n[bold]Run finished with status: {run.status}[/bold]")
                    break
                
                # Get new logs
                new_logs = obj.client.runs.get_logs(run_id, after_log_id=last_log_id)
                
                # Display new logs
                for log in new_logs:
                    console.print(f"[{format_datetime(log.timestamp)}] [{log.level}] {log.message}")
                    last_log_id = log.log_id
                
                # Wait before checking again
                time.sleep(1)
            else:
                console.print("\n[yellow]Timeout reached while following logs[/yellow]")
        
        except KeyboardInterrupt:
            console.print("\n[bold]Stopped following logs[/bold]") 