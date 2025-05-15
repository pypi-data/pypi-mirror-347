"""
Usage monitoring commands for FluidGrids CLI
"""

import click
from datetime import datetime, timedelta
from typing import Dict, Any, List

from ..utils import (
    console, display_table, display_json, create_spinner,
    format_datetime, parse_key_value_pairs
)


@click.group(name="usage")
def usage():
    """Monitor workflow engine usage and metrics."""
    pass


@usage.command(name="metrics")
@click.option("--start-date", type=click.DateTime(), help="Start date for metrics (format: YYYY-MM-DD)")
@click.option("--end-date", type=click.DateTime(), help="End date for metrics (format: YYYY-MM-DD)")
@click.option("--context", multiple=True, help="Context filters as key=value pairs (can be specified multiple times)")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def get_metrics(obj, start_date, end_date, context, output_json):
    """
    Get comprehensive usage metrics.
    
    This command shows metrics about workflow runs, node executions, and more.
    """
    # Set default dates if not provided
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()
    
    # Parse context filters
    context_filters = {}
    if context:
        context_filters = parse_key_value_pairs(context)
    
    # Get metrics
    with create_spinner("Fetching usage metrics..."):
        metrics = obj.client.usage.get_metrics(
            start_date=start_date,
            end_date=end_date,
            context=context_filters
        )
    
    if output_json:
        display_json(metrics)
        return
    
    # Display time period
    time_period = metrics.get("time_period", {})
    console.print(f"[bold]Usage Metrics[/bold]")
    console.print(f"Time Period: {time_period.get('start_date')} to {time_period.get('end_date')} ({time_period.get('duration_days')} days)")
    
    # Display context filters if any
    context_filter = metrics.get("context_filter", {})
    if context_filter:
        console.print("\n[bold]Context Filters:[/bold]")
        for key, value in context_filter.items():
            console.print(f"  {key}: {value}")
    
    # Display workflow execution metrics
    wf_metrics = metrics.get("workflow_execution_metrics", {})
    console.print("\n[bold]Workflow Execution Metrics:[/bold]")
    console.print(f"Total Runs: {wf_metrics.get('total_runs', 0)}")
    console.print(f"Successful Runs: {wf_metrics.get('successful_runs', 0)}")
    console.print(f"Failed Runs: {wf_metrics.get('failed_runs', 0)}")
    
    if wf_metrics.get("total_runs", 0) > 0:
        success_rate = (wf_metrics.get("successful_runs", 0) / wf_metrics.get("total_runs", 0)) * 100
        console.print(f"Success Rate: {success_rate:.1f}%")
    
    console.print(f"Total Duration: {wf_metrics.get('total_duration_seconds', 0):.1f} seconds")
    console.print(f"Average Duration: {wf_metrics.get('average_duration_seconds', 0):.1f} seconds")
    
    # Display node execution metrics
    node_metrics = metrics.get("node_execution_metrics", {})
    console.print("\n[bold]Node Execution Metrics:[/bold]")
    console.print(f"Total Node Executions: {node_metrics.get('total_node_executions', 0)}")
    console.print(f"Successful Node Executions: {node_metrics.get('successful_node_executions', 0)}")
    console.print(f"Failed Node Executions: {node_metrics.get('failed_node_executions', 0)}")
    
    # Display top nodes
    top_nodes = node_metrics.get("top_nodes_by_usage", [])
    if top_nodes:
        console.print("\n[bold]Top Nodes by Usage:[/bold]")
        for node in top_nodes[:5]:  # Show top 5
            console.print(f"  {node.get('node_id', 'Unknown')}: {node.get('usage_count', 0)} executions")
    
    # Display workflow definition metrics
    def_metrics = metrics.get("workflow_definition_metrics", {})
    console.print("\n[bold]Workflow Definition Metrics:[/bold]")
    console.print(f"Total Workflow Definitions: {def_metrics.get('total_workflow_definitions', 0)}")
    console.print(f"Total Workflow Versions: {def_metrics.get('total_workflow_versions', 0)}")
    
    # Display top workflows
    top_workflows = def_metrics.get("top_workflows_by_usage", [])
    if top_workflows:
        console.print("\n[bold]Top Workflows by Usage:[/bold]")
        for wf in top_workflows[:5]:  # Show top 5
            console.print(f"  {wf.get('workflow_key', 'Unknown')}: {wf.get('usage_count', 0)} runs")


@usage.command(name="time-series")
@click.option("--start-date", type=click.DateTime(), help="Start date for the time series (format: YYYY-MM-DD)")
@click.option("--end-date", type=click.DateTime(), help="End date for the time series (format: YYYY-MM-DD)")
@click.option("--interval", type=click.Choice(["hour", "day", "week", "month"]), default="day", help="Time interval (default: day)")
@click.option("--workflow-key", help="Filter by workflow key")
@click.option("--context", multiple=True, help="Context filters as key=value pairs (can be specified multiple times)")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def get_time_series(obj, start_date, end_date, interval, workflow_key, context, output_json):
    """
    Get time series data for usage metrics.
    
    This command shows usage trends over time.
    """
    # Set default dates if not provided
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()
    
    # Parse context filters
    context_filters = {}
    if context:
        context_filters = parse_key_value_pairs(context)
    
    # Get time series data
    with create_spinner("Fetching time series data..."):
        time_series = obj.client.usage.get_time_series(
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            workflow_key=workflow_key,
            context=context_filters
        )
    
    if output_json:
        display_json(time_series)
        return
    
    # Display time period and interval
    console.print(f"[bold]Usage Time Series[/bold]")
    console.print(f"Time Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    console.print(f"Interval: {interval}")
    
    if workflow_key:
        console.print(f"Workflow: {workflow_key}")
    
    # Display context filters if any
    if context_filters:
        console.print("\n[bold]Context Filters:[/bold]")
        for key, value in context_filters.items():
            console.print(f"  {key}: {value}")
    
    # Display run data
    run_data = time_series.get("runs", {}).get("data", [])
    if run_data:
        console.print("\n[bold]Runs by {interval}:[/bold]")
        
        # Format as table
        table_data = []
        for point in run_data:
            table_data.append({
                "timestamp": point.get("timestamp", ""),
                "count": point.get("count", 0),
                "successful": point.get("successful", 0),
                "failed": point.get("failed", 0)
            })
        
        display_table(table_data, columns=["timestamp", "count", "successful", "failed"])
    
    # Display node execution data
    node_data = time_series.get("node_executions", {}).get("data", [])
    if node_data:
        console.print("\n[bold]Node Executions by {interval}:[/bold]")
        
        # Format as table
        table_data = []
        for point in node_data:
            table_data.append({
                "timestamp": point.get("timestamp", ""),
                "count": point.get("count", 0),
                "successful": point.get("successful", 0),
                "failed": point.get("failed", 0)
            })
        
        display_table(table_data, columns=["timestamp", "count", "successful", "failed"]) 