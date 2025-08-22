# UV Environment Setup for Gita Guru

This guide will help you set up and use the uv package manager for the Gita Guru project.

## What is uv?

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and resolver, written in Rust. It's designed to be a drop-in replacement for pip and virtualenv, with much better performance.

## Prerequisites

1. **Install uv** (if not already installed):
   ```bash
   # On Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Or using pip
   pip install uv
   ```

2. **Verify installation**:
   ```bash
   uv --version
   ```

## Quick Setup

### Option 1: Automated Setup (Recommended)

**Windows:**
```cmd
setup_uv.bat
```

**macOS/Linux:**
```bash
python setup_uv.py
```

### Option 2: Manual Setup

1. **Create virtual environment and install dependencies**:
   ```bash
   uv sync
   ```

2. **Install development dependencies**:
   ```bash
   uv sync --dev
   ```

## Using the Environment

### Activating the Environment

```bash
uv shell
```

This activates the virtual environment and gives you access to all installed packages.

### Running the Application

```bash
# Activate environment first
uv shell
streamlit run streamlit_app/__init__.py

# Or run directly without activation
uv run streamlit run streamlit_app/__init__.py
```

### Managing Dependencies

**Add a new dependency:**
```bash
uv add package_name
```

**Add a development dependency:**
```bash
uv add --dev package_name
```

**Remove a dependency:**
```bash
uv remove package_name
```

**Update dependencies:**
```bash
uv sync --upgrade
```

**Lock dependencies:**
```bash
uv lock
```

## Project Structure

The project now uses `pyproject.toml` for dependency management, which includes:

- **Main dependencies**: All packages needed to run the application
- **Development dependencies**: Testing, linting, and development tools
- **Build configuration**: Project metadata and build settings

## Development Workflow

1. **Start development**:
   ```bash
   uv shell
   ```

2. **Run tests** (when implemented):
   ```bash
   uv run pytest
   ```

3. **Format code**:
   ```bash
   uv run black .
   ```

4. **Lint code**:
   ```bash
   uv run flake8 .
   ```

5. **Type checking**:
   ```bash
   uv run mypy .
   ```

## Benefits of uv

- **Faster**: Much faster than pip for dependency resolution and installation
- **Reliable**: Better dependency resolution with fewer conflicts
- **Modern**: Uses `pyproject.toml` for configuration
- **Compatible**: Works with existing Python projects and tools
- **Cross-platform**: Works on Windows, macOS, and Linux

## Troubleshooting

### Common Issues

1. **uv not found**: Make sure uv is installed and in your PATH
2. **Permission errors**: On Unix systems, you might need to use `sudo` for installation
3. **Network issues**: Check your internet connection and proxy settings

### Getting Help

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub Repository](https://github.com/astral-sh/uv)
- [uv Discord Community](https://discord.gg/astral-sh)

## Migration from requirements.txt

The project now uses `pyproject.toml` instead of `requirements.txt`. The old `requirements.txt` file is kept for reference but is no longer the primary dependency specification.

To migrate existing projects:
1. Create a `pyproject.toml` file (already done for this project)
2. Run `uv sync` to install dependencies
3. Remove or archive the old `requirements.txt` file

## Next Steps

After setting up the uv environment:

1. Configure your environment variables (see `.env.example` if available)
2. Set up your Supabase credentials
3. Run the application: `uv run streamlit run streamlit_app/__init__.py`
4. Start developing!

Happy coding! 🚀
