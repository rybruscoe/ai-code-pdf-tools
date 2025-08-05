# Contributing to PDF Tools

Thank you for your interest in contributing to PDF Tools! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/kilo-code-pdf-tools.git
   cd kilo-code-pdf-tools
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

1. **Install dependencies**:
   ```bash
   ./scripts/install-pdf-tools.sh
   ```

2. **Set up VS Code** (optional):
   ```bash
   ./scripts/setup-vscode.sh
   ```

3. **Test your changes**:
   ```bash
   python3 tools/validate_links.py .
   python3 tools/generate_doc_index.py .
   ```

## 📝 Contribution Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise

### Documentation
- Update README.md if adding new features
- Add inline comments for complex logic
- Update PDF_INTEGRATION.md for integration changes
- Test all documentation links

### Testing
- Test your changes on multiple platforms when possible
- Verify PDF processing works with various PDF types
- Ensure VS Code integration functions correctly
- Run existing tools to ensure no regressions

## 🐛 Bug Reports

When reporting bugs, please include:
- Operating system and version
- Python version
- Steps to reproduce the issue
- Expected vs actual behavior
- Any error messages or logs

## ✨ Feature Requests

For new features, please:
- Check existing issues to avoid duplicates
- Describe the use case and benefits
- Provide examples of how it would work
- Consider backward compatibility

## 📋 Pull Request Process

1. **Update documentation** as needed
2. **Test thoroughly** on your local environment
3. **Write clear commit messages**:
   ```
   Add feature: Brief description
   
   - Detailed explanation of changes
   - Any breaking changes noted
   - References to related issues
   ```
4. **Submit pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots if UI changes
   - Testing notes

## 🔍 Code Review

All contributions go through code review:
- Be responsive to feedback
- Make requested changes promptly
- Ask questions if feedback is unclear
- Be respectful and constructive

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Community

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and best practices
- Follow the project's code of conduct

Thank you for contributing to PDF Tools! 🎉