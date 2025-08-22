
# Contributing to Gita Guru

Thank you for your interest in contributing to Gita Guru! We welcome contributions from everyone.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, please include:

- **Description**: Clear description of the bug
- **Steps to reproduce**: Step-by-step instructions
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: OS, Python version, browser (if applicable)
- **Screenshots**: If applicable

### Suggesting Enhancements

We welcome feature requests! Please provide:

- **Clear description** of the enhancement
- **Use case**: Why this feature would be useful
- **Implementation ideas**: If you have any

### Code Contributions

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes
4. **Test** your changes thoroughly
5. **Commit** with clear messages: `git commit -m 'Add amazing feature'`
6. **Push** to your fork: `git push origin feature/amazing-feature`
7. **Create** a Pull Request

## 📋 Development Setup

1. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/gita-guru.git
   cd gita-guru
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**:
   - Copy `.env.example` to `.env`
   - Configure your Supabase credentials

4. **Run the application**:
   ```bash
   streamlit run streamlit_app/login.py
   ```

## 🔧 Code Style

- **Python**: Follow PEP 8 standards
- **Comments**: Write clear, concise comments
- **Functions**: Keep functions small and focused
- **Variables**: Use descriptive variable names
- **Imports**: Group imports logically

## 🧪 Testing

- Test your changes thoroughly before submitting
- Include test cases for new features
- Ensure existing functionality isn't broken
- Test on different screen sizes (for UI changes)

## 📁 Project Structure

```
Gita_Guru/
├── config.py              # Configuration settings
├── database/               # Database utilities and schema
├── scripts/                # Utility scripts
├── streamlit_app/          # Main application
│   ├── pages/             # Application pages
│   ├── login.py           # Login system
│   └── admin_dashboard.py # Admin interface
└── data/                  # JSON data files
```

## 🎯 Areas for Contribution

We especially welcome contributions in:

- **UI/UX improvements**: Making the interface more intuitive
- **Performance optimization**: Faster loading and processing
- **Audio features**: Better audio handling and processing
- **Mobile responsiveness**: Improving mobile experience
- **Documentation**: Code documentation and user guides
- **Testing**: Adding automated tests
- **Accessibility**: Making the app more accessible

## 📝 Pull Request Guidelines

- **Title**: Clear, descriptive title
- **Description**: Explain what changes you made and why
- **Link issues**: Reference any related issues
- **Screenshots**: Include before/after screenshots for UI changes
- **Testing**: Describe how you tested your changes

## 🐛 Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or improvement
- `documentation`: Documentation improvements
- `good-first-issue`: Good for newcomers
- `help-wanted`: Extra attention needed
- `ui/ux`: User interface/experience related

## 🌟 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes for significant contributions
- Special mention for first-time contributors

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Documentation**: Check README.md for setup help

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

Thank you for contributing to Gita Guru! 🕉️
