"""
Dashboard commands for FluidGrids CLI
"""

import click
from typing import Dict, Any, List

from ..utils import console, display_table, display_json, create_spinner, format_datetime


@click.group(name="dashboard")
def dashboard():
    """Get dashboard insights for the workflow engine."""
    pass


@dashboard.command(name="summary")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def get_summary(obj, output_json):
    """
    Get a consolidated summary of workflow engine activities.
    
    This command shows a high-level overview of workflows, runs, and system health.
    """
    with create_spinner("Fetching dashboard summary..."):
        summary = obj.client.dashboard.get_summary()
    
    if output_json:
        display_json(summary)
        return
    
    # Display workflow statistics
    wf_stats = summary.get("workflows", {})
    console.print("[bold]Workflow Statistics[/bold]")
    console.print(f"Total Workflows: {wf_stats.get('total', 0)}")
    console.print(f"Active Workflows: {wf_stats.get('active', 0)}")
    console.print(f"Created This Week: {wf_stats.get('created_this_week', 0)}")
    console.print(f"Updated This Week: {wf_stats.get('updated_this_week', 0)}")
    
    # Display run statistics
    run_stats = summary.get("runs", {})
    console.print("\n[bold]Run Statistics[/bold]")
    console.print(f"Active Runs: {run_stats.get('active', 0)}")
    console.print(f"Completed Today: {run_stats.get('completed_today', 0)}")
    console.print(f"Failed Today: {run_stats.get('failed_today', 0)}")
    console.print(f"Total Runs: {run_stats.get('total', 0)}")
    
    # Display top workflows by usage
    top_wfs = summary.get("top_workflows", [])
    if top_wfs:
        console.print("\n[bold]Top Workflows by Usage[/bold]")
        top_wf_data = []
        for wf in top_wfs:
            top_wf_data.append({
                "workflow_key": wf.get("workflow_key", "Unknown"),
                "name": wf.get("name", ""),
                "run_count": wf.get("run_count", 0),
                "success_rate": f"{wf.get('success_rate', 0) * 100:.1f}%" if "success_rate" in wf else "N/A"
            })
        
        display_table(top_wf_data, columns=["workflow_key", "name", "run_count", "success_rate"])
    
    # Display recent runs
    recent_runs = summary.get("recent_runs", [])
    if recent_runs:
        console.print("\n[bold]Recent Runs[/bold]")
        recent_run_data = []
        for run in recent_runs:
            recent_run_data.append({
                "run_id": run.get("run_id", "Unknown"),
                "workflow_key": run.get("workflow_key", ""),
                "status": run.get("status", ""),
                "started_at": format_datetime(run.get("started_at", "")),
                "duration": f"{run.get('duration_seconds', 0):.1f}s" if "duration_seconds" in run else "N/A"
            })
        
        display_table(recent_run_data, columns=["run_id", "workflow_key", "status", "started_at", "duration"])
    
    # Display system health
    health = summary.get("system_health", {})
    if health:
        console.print("\n[bold]System Health[/bold]")
        for key, value in health.items():
            if isinstance(value, dict):
                console.print(f"{key}:")
                for sub_key, sub_value in value.items():
                    console.print(f"  {sub_key}: {sub_value}")
            else:
                console.print(f"{key}: {value}") 