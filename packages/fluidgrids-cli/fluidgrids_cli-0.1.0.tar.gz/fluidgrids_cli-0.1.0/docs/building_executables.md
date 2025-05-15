# Building Executable Files

The FluidGrids CLI can be packaged as a standalone executable for various platforms using PyInstaller. This allows you to distribute the CLI to users without requiring them to install Python or any dependencies.

## Prerequisites

Before building executables, you need to have PyInstaller installed:

```bash
pip install pyinstaller
```

## Building Executables

### For All Platforms

The easiest way to build executables for all platforms is to use the included build script:

```bash
python build_executables.py
```

This will create executables for your current platform in the `dist` directory.

### For Windows

To build a Windows executable manually:

```bash
# For a single-file executable
pyinstaller --name fluidgrids --onefile --add-data "fluidgrids_cli:fluidgrids_cli" fluidgrids-cli/fluidgrids_cli/cli.py

# For a directory-based executable (faster startup)
pyinstaller --name fluidgrids --add-data "fluidgrids_cli:fluidgrids_cli" fluidgrids-cli/fluidgrids_cli/cli.py
```

The executable will be created in the `dist` directory.

### For macOS

To build a macOS executable manually:

```bash
# For a single-file executable
pyinstaller --name fluidgrids --onefile --add-data "fluidgrids_cli:fluidgrids_cli" fluidgrids-cli/fluidgrids_cli/cli.py

# For a directory-based executable (faster startup)
pyinstaller --name fluidgrids --add-data "fluidgrids_cli:fluidgrids_cli" fluidgrids-cli/fluidgrids_cli/cli.py

# To create a signed app (requires Apple Developer account)
pyinstaller --name fluidgrids --onefile --windowed --add-data "fluidgrids_cli:fluidgrids_cli" --osx-bundle-identifier "ai.fluidgrids.cli" fluidgrids-cli/fluidgrids_cli/cli.py
```

### For Linux

To build a Linux executable manually:

```bash
# For a single-file executable
pyinstaller --name fluidgrids --onefile --add-data "fluidgrids_cli:fluidgrids_cli" fluidgrids-cli/fluidgrids_cli/cli.py

# For a directory-based executable (faster startup)
pyinstaller --name fluidgrids --add-data "fluidgrids_cli:fluidgrids_cli" fluidgrids-cli/fluidgrids_cli/cli.py
```

## Cross-Platform Building

Building executables for platforms other than your current one can be challenging. Here are some approaches:

### Using Docker

You can use Docker to build executables for different platforms:

```bash
# For Linux executable on any host
docker run --rm -v $(pwd):/src -w /src python:3.9 /bin/bash -c "pip install pyinstaller && pip install -e . && pyinstaller --name fluidgrids --onefile --add-data 'fluidgrids_cli:fluidgrids_cli' fluidgrids-cli/fluidgrids_cli/cli.py"
```

### Using GitHub Actions

For automated building across platforms, you can use GitHub Actions. Here's a sample workflow:

```yaml
name: Build Executables

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.9]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pyinstaller
        pip install -e .
    - name: Build executable
      run: |
        pyinstaller --name fluidgrids --onefile --add-data "fluidgrids_cli:fluidgrids_cli" fluidgrids-cli/fluidgrids_cli/cli.py
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: fluidgrids-${{ matrix.os }}
        path: dist/fluidgrids*
```

## Troubleshooting

### Missing Modules

If you're getting "module not found" errors when running the executable, you may need to explicitly include some modules:

```bash
pyinstaller --name fluidgrids --onefile --hidden-import=click --hidden-import=yaml --hidden-import=keyring --add-data "fluidgrids_cli:fluidgrids_cli" fluidgrids-cli/fluidgrids_cli/cli.py
```

### Missing Data Files

If data files are missing, make sure you're specifying the correct path for `--add-data`. The format is `source:destination`, where the path is relative to the current directory.

### Executable Size

PyInstaller executables include the Python interpreter and all dependencies, so they can be quite large. To reduce the size:

```bash
pyinstaller --name fluidgrids --onefile --strip --add-data "fluidgrids_cli:fluidgrids_cli" fluidgrids-cli/fluidgrids_cli/cli.py
```

## Distribution

After building, you can distribute the executables in several ways:

1. **GitHub Releases**: Upload the executables as release assets
2. **Package Managers**: Create packages for Homebrew, Chocolatey, apt, etc.
3. **Custom Installer**: Create an installer using tools like NSIS (Windows), pkgbuild (macOS), or deb/rpm for Linux

For more information, see the [PyInstaller Documentation](https://pyinstaller.readthedocs.io/). 