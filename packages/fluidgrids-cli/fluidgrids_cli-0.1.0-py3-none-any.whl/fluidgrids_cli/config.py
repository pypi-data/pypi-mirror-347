"""
Configuration management for the FluidGrids CLI
"""

import os
import yaml
import keyring
from pathlib import Path
from typing import Dict, Any, Optional

# Constants
CONFIG_DIR = os.path.expanduser("~/.fluidgrids")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yaml")
KEYRING_SERVICE = "fluidgrids-cli"


def ensure_config_dir() -> None:
    """Ensure the configuration directory exists."""
    os.makedirs(CONFIG_DIR, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """Load the configuration from the YAML file."""
    ensure_config_dir()
    
    if not os.path.exists(CONFIG_FILE):
        return {"api_url": "https://api.fluidgrids.ai"}
    
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f) or {"api_url": "https://api.fluidgrids.ai"}


def save_config(config: Dict[str, Any]) -> None:
    """Save the configuration to the YAML file."""
    ensure_config_dir()
    
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f, default_flow_style=False)


def get_credentials() -> Dict[str, Optional[str]]:
    """Get credentials from the configuration and keyring."""
    config = load_config()
    creds = {
        "api_url": config.get("api_url"),
        "api_key": None,
        "username": config.get("username"),
        "password": None,
        "token": config.get("token"),
    }
    
    # Try to get API key from keyring
    if not creds["api_key"] and config.get("use_api_key", False):
        creds["api_key"] = keyring.get_password(KEYRING_SERVICE, "api_key")
    
    # Try to get password from keyring
    if creds["username"] and not creds["password"]:
        creds["password"] = keyring.get_password(KEYRING_SERVICE, creds["username"])
        
    return creds


def set_api_url(url: str) -> None:
    """Set the API URL in the configuration."""
    config = load_config()
    config["api_url"] = url
    save_config(config)


def set_api_key(api_key: str) -> None:
    """Set the API key in the keyring and update the configuration."""
    config = load_config()
    config["use_api_key"] = True
    if "username" in config:
        del config["username"]
    if "token" in config:
        del config["token"]
    save_config(config)
    
    keyring.set_password(KEYRING_SERVICE, "api_key", api_key)


def set_credentials(username: str, password: str) -> None:
    """Set the username in the configuration and password in the keyring."""
    config = load_config()
    config["username"] = username
    config["use_api_key"] = False
    if "token" in config:
        del config["token"]
    save_config(config)
    
    keyring.set_password(KEYRING_SERVICE, username, password)


def set_token(token: str) -> None:
    """Set the token in the configuration."""
    config = load_config()
    config["token"] = token
    config["use_api_key"] = False
    if "username" in config:
        del config["username"]
    save_config(config)


def clear_credentials() -> None:
    """Clear all credentials from the configuration and keyring."""
    config = load_config()
    
    # Clear credentials from config
    for key in ["username", "token", "use_api_key"]:
        if key in config:
            del config[key]
    
    save_config(config)
    
    # Clear API key from keyring
    try:
        keyring.delete_password(KEYRING_SERVICE, "api_key")
    except keyring.errors.PasswordDeleteError:
        pass
    
    # Clear password from keyring if username existed
    if "username" in config:
        try:
            keyring.delete_password(KEYRING_SERVICE, config["username"])
        except keyring.errors.PasswordDeleteError:
            pass 