"""
Utility functions for the FluidGrids CLI
"""

import json
import sys
from typing import Dict, Any, List, Union, Optional
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from tabulate import tabulate
from datetime import datetime

console = Console()


class SDKObjectEncoder(json.JSONEncoder):
    """JSON encoder that can handle custom SDK objects."""
    def default(self, obj):
        # First try to convert SDK objects with __dict__ attribute
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        
        # For objects with attribute access but no __dict__
        try:
            # Try to convert to a dictionary
            if hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):
                return obj.dict()
            # For objects that only have __getattr__ or __getattribute__
            elif hasattr(obj, 'keys') and callable(getattr(obj, 'keys')):
                return {key: getattr(obj, key) for key in obj.keys()}
            elif dir(obj):
                # Get all attributes that don't start with '_'
                attrs = [attr for attr in dir(obj) if not attr.startswith('_') 
                         and not callable(getattr(obj, attr))]
                return {attr: getattr(obj, attr) for attr in attrs}
        except:
            pass
            
        # Call the parent class default method for other types
        return super().default(obj)


def format_json(data: Any) -> str:
    """Format data as JSON with proper indentation."""
    return json.dumps(data, indent=2, sort_keys=False, cls=SDKObjectEncoder)


def display_json(data: Any) -> None:
    """Display data as formatted JSON."""
    console.print(format_json(data))


def safe_get_attr(obj: Any, attr: str, default: Any = "") -> Any:
    """Safely get an attribute from an object with fallbacks for different object types."""
    # If object is a dictionary
    if isinstance(obj, dict):
        return obj.get(attr, default)
    
    # Try direct attribute access
    try:
        if hasattr(obj, attr):
            return getattr(obj, attr)
    except:
        pass
    
    # Try dictionary method if available
    try:
        if hasattr(obj, 'get') and callable(getattr(obj, 'get')):
            return obj.get(attr, default)
    except:
        pass
    
    # Try dictionary-like access if available
    try:
        if hasattr(obj, '__getitem__'):
            return obj[attr]
    except:
        pass
    
    return default


def display_table(data: List[Dict[str, Any]], columns: Optional[List[str]] = None) -> None:
    """Display data as a table."""
    if not data:
        console.print("No data found.")
        return
    
    # If columns not specified, use all keys from the first item
    if not columns:
        if isinstance(data[0], dict):
            columns = list(data[0].keys())
        else:
            # Try to get attributes from the object
            columns = [attr for attr in dir(data[0]) 
                      if not attr.startswith('_') and not callable(getattr(data[0], attr))]
    
    table = Table(show_header=True)
    
    # Add columns to the table
    for column in columns:
        table.add_column(column.replace("_", " ").title())
    
    # Add rows to the table
    for item in data:
        row = []
        for column in columns:
            value = safe_get_attr(item, column)
            if isinstance(value, (dict, list)):
                value = format_json(value)
            elif value is None:
                value = ""
            elif isinstance(value, bool):
                value = "Yes" if value else "No"
            row.append(str(value))
        table.add_row(*row)
    
    console.print(table)


def parse_key_value_pairs(pairs: List[str]) -> Dict[str, str]:
    """Parse key-value pairs from the command line (key=value format)."""
    result = {}
    for pair in pairs:
        if "=" not in pair:
            console.print(f"[red]Error: Invalid key=value pair: {pair}[/red]")
            sys.exit(1)
        
        key, value = pair.split("=", 1)
        result[key] = value
    
    return result


def parse_json_object(json_str: str) -> Dict[str, Any]:
    """Parse a JSON object from a string."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON: {e}[/red]")
        sys.exit(1)


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load a JSON object from a file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        console.print(f"[red]Error loading JSON file: {e}[/red]")
        sys.exit(1)


def format_datetime(dt_str: str) -> str:
    """Format a datetime string for display."""
    if not dt_str:
        return ""
    
    try:
        # Parse ISO 8601 datetime
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        # Format for display
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    except (ValueError, TypeError):
        return dt_str


def create_spinner(message: str = "Processing..."):
    """Create a spinner for long-running operations."""
    return Progress(
        SpinnerColumn(),
        TextColumn(f"[bold blue]{message}"),
        transient=True,
    )


def handle_error(message: str, exit_code: int = 1) -> None:
    """Handle an error by displaying a message and exiting."""
    console.print(f"[bold red]Error: {message}[/bold red]")
    sys.exit(exit_code) 