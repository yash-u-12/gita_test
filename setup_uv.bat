@echo off
echo 🚀 Setting up Gita Guru with uv...

REM Check if uv is installed
uv --version >nul 2>&1
if errorlevel 1 (
    echo ❌ uv is not installed. Please install uv first:
    echo    Visit: https://docs.astral.sh/uv/getting-started/installation/
    echo    Or run: curl -LsSf https://astral.sh/uv/install.sh ^| sh
    pause
    exit /b 1
)

echo ✅ uv is installed

echo.
echo 📦 Creating virtual environment and installing dependencies...
uv sync

if errorlevel 1 (
    echo ❌ Failed to sync dependencies
    pause
    exit /b 1
)

echo.
echo 🔧 Installing development dependencies...
uv sync --dev

if errorlevel 1 (
    echo ❌ Failed to install development dependencies
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Activate the virtual environment:
echo    uv shell
echo.
echo 2. Run the Streamlit app:
echo    streamlit run streamlit_app/__init__.py
echo.
echo 3. For development, you can also use:
echo    uv run streamlit run streamlit_app/__init__.py
echo.
echo 4. To add new dependencies:
echo    uv add package_name
echo.
echo 5. To add development dependencies:
echo    uv add --dev package_name
echo.
pause
