# 🤝 Contributing to Gita Guru

Thank you for your interest in contributing to Gita Guru! This document provides guidelines and information for contributors.

## 🎯 Project Overview

Gita Guru is a comprehensive learning platform for studying the Bhagavad Gita with interactive audio features. We welcome contributions from developers, designers, content creators, and users who want to improve the platform.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- A Supabase account (for backend services)

### Setup Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/gita-guru.git
   cd gita-guru
   ```

2. **Install Dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your Supabase credentials
   nano .env
   ```

4. **Database Setup**
   ```bash
   # Run database schema
   python scripts/setup_database.py
   ```

## 📋 Development Guidelines

### Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting
- **Ruff**: Linting and import sorting
- **MyPy**: Type checking
- **Pre-commit**: Git hooks for quality checks

```bash
# Format code
black .

# Lint code
ruff check .

# Type check
mypy .

# Run all checks
pre-commit run --all-files
```

### Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): add OTP-based login system
fix(upload): resolve audio file upload timeout
docs(readme): update installation instructions
```

### Branch Naming

- `feature/feature-name`: New features
- `fix/bug-description`: Bug fixes
- `docs/documentation-update`: Documentation changes
- `refactor/component-name`: Code refactoring

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_api_client.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

**Example:**
```python
def test_upload_audio_success():
    """Test successful audio upload"""
    # Arrange
    audio_data = b"fake_audio_data"
    
    # Act
    result = upload_audio(audio_data)
    
    # Assert
    assert result.success is True
    assert result.upload_id is not None
```

## 📝 Documentation

### Code Documentation

- Use docstrings for all functions and classes
- Follow Google docstring format
- Include type hints for all parameters and return values

**Example:**
```python
def upload_audio(
    audio_data: bytes,
    filename: str,
    user_id: str
) -> UploadResult:
    """Upload audio file to storage.
    
    Args:
        audio_data: Raw audio bytes
        filename: Name of the audio file
        user_id: ID of the uploading user
        
    Returns:
        UploadResult with success status and upload ID
        
    Raises:
        UploadError: If upload fails
    """
```

### API Documentation

- Document all API endpoints
- Include request/response examples
- Specify error codes and messages

## 🐛 Bug Reports

### Before Submitting

1. Check existing issues for duplicates
2. Try to reproduce the issue
3. Gather relevant information (logs, screenshots, etc.)

### Bug Report Template

```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, macOS 12]
- Browser: [e.g., Chrome 120, Firefox 115]
- Python Version: [e.g., 3.9.7]
- Streamlit Version: [e.g., 1.47.0]

## Additional Information
Screenshots, logs, or other relevant information
```

## 💡 Feature Requests

### Before Submitting

1. Check if the feature already exists
2. Consider if it aligns with project goals
3. Think about implementation complexity

### Feature Request Template

```markdown
## Feature Description
Brief description of the requested feature

## Problem Statement
What problem does this feature solve?

## Proposed Solution
How should this feature work?

## Alternative Solutions
Other ways to solve the problem

## Additional Context
Screenshots, mockups, or other relevant information
```

## 🔄 Pull Request Process

### Before Submitting

1. **Update Documentation**
   - Update README.md if needed
   - Add/update docstrings
   - Update API documentation

2. **Run Tests**
   ```bash
   pytest
   ```

3. **Code Quality Checks**
   ```bash
   black .
   ruff check .
   mypy .
   ```

4. **Test Locally**
   ```bash
   streamlit run streamlit_app/main.py
   ```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] No breaking changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No console errors
```

## 🏷️ Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Example: `1.2.3`

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Release notes written

## 🆘 Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: For sensitive or private matters

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) for details.

## 🙏 Acknowledgments

Thank you to all contributors who have helped make Gita Guru better:

- Code contributors
- Bug reporters
- Feature requesters
- Documentation writers
- Testers and reviewers

---

**🕉️ May the wisdom of the Bhagavad Gita guide our collaborative efforts!**
