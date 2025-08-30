.PHONY: help install test lint format clean run-dev run-prod setup-db

# Default target
help:
	@echo "Gita Guru - Development Commands"
	@echo "================================"
	@echo "install     - Install dependencies"
	@echo "test        - Run tests"
	@echo "lint        - Run linting and type checking"
	@echo "format      - Format code"
	@echo "clean       - Clean cache and temporary files"
	@echo "run-dev     - Run development server"
	@echo "run-prod    - Run production server"
	@echo "setup-db    - Setup database schema"
	@echo "help        - Show this help message"

# Install dependencies
install:
	@echo "Installing dependencies..."
	uv sync
	@echo "Dependencies installed successfully!"

# Run tests
test:
	@echo "Running tests..."
	pytest -v --tb=short
	@echo "Tests completed!"

# Run linting and type checking
lint:
	@echo "Running linting and type checking..."
	ruff check .
	mypy .
	@echo "Linting completed!"

# Format code
format:
	@echo "Formatting code..."
	black .
	ruff format .
	@echo "Code formatting completed!"

# Clean cache and temporary files
clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -delete 2>/dev/null || true
	@echo "Cleanup completed!"

# Run development server
run-dev:
	@echo "Starting development server..."
	streamlit run streamlit_app/login.py --server.port=8501 --server.headless=false

# Run production server
run-prod:
	@echo "Starting production server..."
	streamlit run streamlit_app/login.py --server.port=8501 --server.headless=true

# Setup database
setup-db:
	@echo "Setting up database schema..."
	python -c "from database.db_utils import get_db_manager; db = get_db_manager(); print('Database setup completed!')"

# Install pre-commit hooks
install-hooks:
	@echo "Installing pre-commit hooks..."
	pre-commit install
	@echo "Pre-commit hooks installed!"

# Run all quality checks
quality: format lint test
	@echo "All quality checks completed!"

# Development setup
dev-setup: install install-hooks setup-db
	@echo "Development environment setup completed!"

# Production build
build: clean install quality
	@echo "Production build completed!"
