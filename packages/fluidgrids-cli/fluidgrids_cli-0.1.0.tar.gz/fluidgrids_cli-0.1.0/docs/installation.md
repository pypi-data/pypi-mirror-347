# Installation Guide

This guide provides instructions for installing the FluidGrids CLI on various platforms.

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Installation Methods

### Using pip (Recommended)

The FluidGrids CLI is available on PyPI and can be installed using pip:

```bash
pip install fluidgrids-cli
```

To install a specific version:

```bash
pip install fluidgrids-cli==0.1.0
```

To upgrade to the latest version:

```bash
pip install --upgrade fluidgrids-cli
```

### Using pip with Virtual Environment

It's recommended to install the CLI in a virtual environment to avoid conflicts with other Python packages:

#### For Unix/macOS:

```bash
# Create a virtual environment
python -m venv fluidgrids-env

# Activate the virtual environment
source fluidgrids-env/bin/activate

# Install the CLI
pip install fluidgrids-cli

# Use the CLI
fluidgrids --help
```

#### For Windows:

```bash
# Create a virtual environment
python -m venv fluidgrids-env

# Activate the virtual environment
fluidgrids-env\Scripts\activate

# Install the CLI
pip install fluidgrids-cli

# Use the CLI
fluidgrids --help
```

### From Source Code

To install the latest development version from source:

```bash
# Clone the repository
git clone https://github.com/algoshred/fluidgrids-cli.git
cd fluidgrids-cli

# Install in development mode
pip install -e .
```

### Using Pre-built Executables

Pre-built executables are available for Windows, macOS, and Linux platforms. These executables don't require Python to be installed:

1. Download the appropriate executable for your platform from [GitHub Releases](https://github.com/algoshred/fluidgrids-cli/releases)
2. Make the file executable (Linux/macOS only): `chmod +x fluidgrids`
3. Run the executable: `./fluidgrids` (Linux/macOS) or `fluidgrids.exe` (Windows)

## Verifying Installation

To verify that the installation was successful, run:

```bash
fluidgrids --version
```

This should display the version of the CLI that you have installed.

## Troubleshooting

### Command Not Found

If you get a "command not found" error after installation, it might be because the Python scripts directory is not in your PATH. Try the following:

1. Find the Python scripts directory:
   ```bash
   python -c "import site; print(site.USER_BASE + '/bin')"  # Unix/macOS
   python -c "import site; print(site.USER_BASE + '\\Scripts')"  # Windows
   ```
2. Add this directory to your PATH environment variable.

### Permission Errors

If you get permission errors when installing globally, you might need to use `sudo` (on Unix/macOS) or run the command prompt as administrator (on Windows):

```bash
sudo pip install fluidgrids-cli  # Unix/macOS
```

### SSL Certificate Errors

If you encounter SSL certificate errors when installing, you may need to provide additional certificates or skip verification (not recommended for production):

```bash
pip install fluidgrids-cli --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

## Next Steps

Once you have successfully installed the FluidGrids CLI, you can [authenticate](authentication.md) with the FluidGrids API and start using the CLI. 