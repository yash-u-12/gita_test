#!/usr/bin/env python3
"""
Setup script for Gita Guru uv environment
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def main():
    print("🚀 Setting up Gita Guru with uv...")
    
    # Check if uv is installed
    uv_check = run_command("uv --version", "Checking uv installation")
    if not uv_check:
        print("❌ uv is not installed. Please install uv first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   or visit: https://docs.astral.sh/uv/getting-started/installation/")
        return
    
    # Create virtual environment and install dependencies
    print("\n📦 Creating virtual environment and installing dependencies...")
    
    # Sync dependencies (creates venv and installs packages)
    sync_result = run_command("uv sync", "Syncing project dependencies")
    if not sync_result:
        print("❌ Failed to sync dependencies")
        return
    
    # Install dev dependencies
    dev_result = run_command("uv sync --dev", "Installing development dependencies")
    if not dev_result:
        print("❌ Failed to install development dependencies")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate the virtual environment:")
    print("   uv shell")
    print("\n2. Run the Streamlit app:")
    print("   streamlit run streamlit_app/__init__.py")
    print("\n3. For development, you can also use:")
    print("   uv run streamlit run streamlit_app/__init__.py")
    print("\n4. To add new dependencies:")
    print("   uv add package_name")
    print("\n5. To add development dependencies:")
    print("   uv add --dev package_name")

if __name__ == "__main__":
    main()
