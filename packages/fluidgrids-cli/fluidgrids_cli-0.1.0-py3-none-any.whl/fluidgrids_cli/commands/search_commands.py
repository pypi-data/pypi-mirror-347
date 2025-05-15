"""
Search commands for FluidGrids CLI
"""

import click
from typing import Dict, Any, List

from ..utils import (
    console, display_table, display_json, create_spinner,
    format_datetime, parse_json_object
)


@click.group(name="search")
def search():
    """Search across workflows, runs, and other entities."""
    pass


@search.command(name="query")
@click.argument("query", required=True)
@click.option("--entity-type", multiple=True, help="Entity types to search (can be specified multiple times)")
@click.option("--filters", help="JSON object with search filters")
@click.option("--limit", type=int, default=10, help="Maximum number of results per entity type")
@click.option("--offset", type=int, default=0, help="Offset for pagination")
@click.option("--sort", type=click.Choice(["relevance", "date_asc", "date_desc"]), default="relevance", help="Sort order (default: relevance)")
@click.option("--highlight", is_flag=True, help="Highlight matching text in results")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def search_query(obj, query, entity_type, filters, limit, offset, sort, highlight, output_json):
    """
    Search across multiple entity types with a unified query.
    
    QUERY is the search query string.
    
    Examples:
    
    fluidgrids search query "data processing"
    
    fluidgrids search query "failed runs" --entity-type run --sort date_desc
    """
    # Parse filters if provided
    filter_dict = {}
    if filters:
        filter_dict = parse_json_object(filters)
    
    # Build parameters
    params = {
        "query": query,
        "limit": limit,
        "offset": offset,
        "sort": sort,
        "highlight": highlight
    }
    
    if entity_type:
        params["entity_types"] = list(entity_type)
    
    if filter_dict:
        params["filters"] = filter_dict
    
    # Execute search
    with create_spinner(f"Searching for '{query}'..."):
        results = obj.client.search.search(**params)
    
    if output_json:
        display_json(results)
        return
    
    # Display results
    total = results.get("total_results", 0)
    entity_counts = results.get("entity_counts", {})
    
    console.print(f"[bold]Search Results for '{query}'[/bold]")
    console.print(f"Found {total} results across {len(entity_counts)} entity types")
    
    # Display results grouped by entity type
    results_dict = results.get("results", {})
    for entity_type, items in results_dict.items():
        if not items:
            continue
            
        console.print(f"\n[bold]{entity_type.title()} Results[/bold] ({len(items)} found)")
        
        for item in items:
            title = item.get("title", "Unnamed")
            description = item.get("description", "")
            url = item.get("url", "")
            created_at = format_datetime(item.get("created_at", ""))
            
            console.print(f"[bold cyan]{title}[/bold cyan]")
            if description:
                # Truncate description if too long
                desc_display = description[:100] + "..." if len(description) > 100 else description
                console.print(f"  {desc_display}")
            if created_at:
                console.print(f"  Created: {created_at}")
            if url:
                console.print(f"  URL: {url}")
            
            # Display metadata if present
            metadata = item.get("metadata", {})
            if metadata:
                relevant_metadata = {}
                # Filter out less useful metadata
                for key, value in metadata.items():
                    if key not in ["title", "description", "url", "created_at", "updated_at"]:
                        relevant_metadata[key] = value
                
                if relevant_metadata:
                    metadata_str = ", ".join(f"{k}: {v}" for k, v in relevant_metadata.items())
                    console.print(f"  {metadata_str}")
            
            console.print("")  # Empty line between results


@search.command(name="entity")
@click.argument("entity_type", required=True)
@click.argument("query", required=True)
@click.option("--limit", type=int, default=10, help="Maximum number of results")
@click.option("--offset", type=int, default=0, help="Offset for pagination")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def search_entity(obj, entity_type, query, limit, offset, output_json):
    """
    Search within a specific entity type.
    
    ENTITY_TYPE is the type of entity to search (e.g., workflow, run).
    QUERY is the search query string.
    
    Examples:
    
    fluidgrids search entity workflow "data processing"
    
    fluidgrids search entity run "failed" --limit 20
    """
    with create_spinner(f"Searching for '{query}' in {entity_type}..."):
        results = obj.client.search.search_entity(
            entity_type=entity_type,
            query=query,
            limit=limit,
            offset=offset
        )
    
    if output_json:
        display_json(results)
        return
    
    # Display results
    total = results.get("total_results", 0)
    console.print(f"[bold]Search Results for '{query}' in {entity_type}[/bold]")
    console.print(f"Found {total} results")
    
    # Display results for the entity type
    items = results.get("results", {}).get(entity_type, [])
    
    if not items:
        console.print("No results found.")
        return
    
    for item in items:
        title = item.get("title", "Unnamed")
        description = item.get("description", "")
        url = item.get("url", "")
        created_at = format_datetime(item.get("created_at", ""))
        
        console.print(f"[bold cyan]{title}[/bold cyan]")
        if description:
            # Truncate description if too long
            desc_display = description[:100] + "..." if len(description) > 100 else description
            console.print(f"  {desc_display}")
        if created_at:
            console.print(f"  Created: {created_at}")
        if url:
            console.print(f"  URL: {url}")
        
        # Display metadata if present
        metadata = item.get("metadata", {})
        if metadata:
            relevant_metadata = {}
            # Filter out less useful metadata
            for key, value in metadata.items():
                if key not in ["title", "description", "url", "created_at", "updated_at"]:
                    relevant_metadata[key] = value
            
            if relevant_metadata:
                metadata_str = ", ".join(f"{k}: {v}" for k, v in relevant_metadata.items())
                console.print(f"  {metadata_str}")
        
        console.print("")  # Empty line between results


@search.command(name="entities")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_obj
def get_entities(obj, output_json):
    """
    Get information about entities that can be searched.
    
    This command shows what entities are searchable and what fields can be searched.
    """
    with create_spinner("Fetching searchable entities..."):
        result = obj.client.search.get_searchable_entities()
    
    if output_json:
        display_json(result)
        return
    
    # Display entities
    entities = result.get("entities", {})
    console.print("[bold]Searchable Entities[/bold]")
    
    for entity_name, entity_info in entities.items():
        console.print(f"\n[bold cyan]{entity_name.title()}[/bold cyan]")
        
        # Display fields
        fields = entity_info.get("fields", [])
        if fields:
            console.print("  Searchable Fields:")
            for field in fields:
                console.print(f"    - {field}")
        
        # Display filters
        filters = entity_info.get("filters", [])
        if filters:
            console.print("  Available Filters:")
            for filter_info in filters:
                console.print(f"    - {filter_info}") 