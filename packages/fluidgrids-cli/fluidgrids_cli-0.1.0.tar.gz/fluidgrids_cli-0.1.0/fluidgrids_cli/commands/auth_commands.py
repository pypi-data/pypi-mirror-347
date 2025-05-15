"""
Authentication commands for FluidGrids CLI
"""

import click
import getpass
from rich.console import Console
from fluidgrids import FluidGridsClient

from ..config import (
    set_api_url, set_api_key, set_credentials, 
    set_token, clear_credentials, get_credentials
)
from ..utils import console, create_spinner

@click.group(name="auth")
def auth():
    """Manage authentication and credentials."""
    pass


@auth.command(name="login")
@click.option("--url", help="API URL for FluidGrids")
@click.option("--username", help="Username for authentication")
@click.option("--password", help="Password for authentication (not recommended, use prompt)")
def login(url, username, password):
    """
    Log in with username and password.
    
    This command will prompt for credentials if not provided and store them securely.
    """
    # Get API URL
    if url:
        set_api_url(url)
    
    # Get credentials from the command line or prompt
    if not username:
        username = click.prompt("Username")
    
    if not password:
        password = getpass.getpass("Password: ")
    
    # Validate credentials by attempting to login
    with create_spinner("Logging in..."):
        try:
            temp_client = FluidGridsClient(
                base_url=get_credentials()["api_url"],
                username=username,
                password=password
            )
            
            # If we're here, login succeeded
            # Store the credentials
            set_credentials(username, password)
            console.print("[bold green]Login successful![/bold green]")
        
        except Exception as e:
            console.print(f"[bold red]Login failed: {str(e)}[/bold red]")
            return


@auth.command(name="set-key")
@click.option("--api-key", required=True, help="API key for authentication")
@click.option("--url", help="API URL for FluidGrids")
def set_key(api_key, url):
    """
    Set an API key for authentication.
    
    This is useful for automation and CI/CD pipelines.
    """
    if url:
        set_api_url(url)
    
    # Validate the API key by making a test request
    with create_spinner("Validating API key..."):
        try:
            temp_client = FluidGridsClient(
                base_url=get_credentials()["api_url"],
                api_key=api_key
            )
            
            # Make a simple request to verify the key works
            temp_client.workflows.list(limit=1)
            
            # If we're here, the key is valid
            set_api_key(api_key)
            console.print("[bold green]API key set successfully![/bold green]")
        
        except Exception as e:
            console.print(f"[bold red]Failed to validate API key: {str(e)}[/bold red]")
            return


@auth.command(name="set-token")
@click.option("--token", required=True, help="JWT token for authentication")
@click.option("--url", help="API URL for FluidGrids")
def set_token_cmd(token, url):
    """
    Set a JWT token for authentication.
    
    This is useful when you have a token from another source.
    """
    if url:
        set_api_url(url)
    
    # Validate the token by making a test request
    with create_spinner("Validating token..."):
        try:
            temp_client = FluidGridsClient(
                base_url=get_credentials()["api_url"],
                token=token
            )
            
            # Make a simple request to verify the token works
            temp_client.workflows.list(limit=1)
            
            # If we're here, the token is valid
            set_token(token)
            console.print("[bold green]Token set successfully![/bold green]")
        
        except Exception as e:
            console.print(f"[bold red]Failed to validate token: {str(e)}[/bold red]")
            return


@auth.command(name="status")
def status():
    """
    Show the current authentication status.
    """
    creds = get_credentials()
    
    console.print("Authentication Status")
    console.print("---------------------")
    console.print(f"API URL: {creds['api_url']}")
    
    # Determine auth method
    if creds["api_key"]:
        console.print("Auth Method: API Key")
        console.print("API Key: ********")
    elif creds["token"]:
        console.print("Auth Method: Token")
        console.print(f"Token: {creds['token'][:10]}...")
    elif creds["username"]:
        console.print("Auth Method: Username/Password")
        console.print(f"Username: {creds['username']}")
        console.print("Password: ********")
    else:
        console.print("[yellow]Not authenticated[/yellow]")


@auth.command(name="logout")
def logout():
    """
    Log out and clear stored credentials.
    """
    if click.confirm("Are you sure you want to log out and clear all stored credentials?"):
        clear_credentials()
        console.print("[bold green]Logged out successfully![/bold green]") 