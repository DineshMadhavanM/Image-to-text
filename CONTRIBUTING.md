# Contributing to Sports Image Captioning AI

🎉 **Thank you for considering contributing to our project!** We welcome contributions of all kinds, from code to documentation to bug reports.

## 📋 Table of Contents
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Code Style & Standards](#code-style--standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Areas for Contribution](#areas-for-contribution)
- [Getting Help](#getting-help)

## 🚀 How to Contribute

### 1. Find Something to Work On
- **Good First Issues**: Look for issues labeled [`good first issue`](https://github.com/DineshMadhavanM/Image-to-text/labels/good%20first%20issue)
- **Help Wanted**: Check issues labeled [`help wanted`](https://github.com/DineshMadhavanM/Image-to-text/labels/help%20wanted)
- **Bug Reports**: Help fix existing bugs
- **Feature Requests**: Implement new features
- **Documentation**: Improve docs, examples, and tutorials

### 2. Fork and Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/Image-to-text.git
cd Image-to-text

# Add the original repository as upstream
git remote add upstream https://github.com/DineshMadhavanM/Image-to-text.git
```

### 3. Create a Branch
```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/your-bug-fix
```

## 🛠️ Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of Python and web development

### Environment Setup
```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate it
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install development dependencies
pip install pytest pytest-cov black flake8 isort pre-commit

# 5. Set up pre-commit hooks
pre-commit install
```

### Running the Application
```bash
# Run the command-line version
python sports_captioner.py

# Run the web interface
python app.py
# Then visit http://localhost:5000
```

## 📐 Code Style & Standards

We use the following tools to maintain code quality:

### Python Code Style
- **Black** for code formatting
- **Flake8** for linting
- **isort** for import sorting

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .
```

### Code Guidelines
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Add type hints where appropriate

### Commit Message Format
We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(web): add image upload progress bar`
- `fix(captioner): resolve memory leak in image processing`
- `docs(readme): update installation instructions`
- `test(api): add integration tests for caption generation`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_sports_captioner.py

# Run with verbose output
pytest -v
```

### Writing Tests
- Write tests for all new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

### Test Structure
```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── fixtures/       # Test data and fixtures
```

## 🔄 Pull Request Process

### 1. Before Submitting
- [ ] Run all tests and ensure they pass
- [ ] Format code with Black
- [ ] Check code with Flake8
- [ ] Update documentation if needed
- [ ] Rebase your branch on the latest main

### 2. Submitting a PR
```bash
# Ensure your branch is up to date
git fetch upstream
git rebase upstream/main

# Push to your fork
git push origin feature/your-feature-name
```

### 3. PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added tests for new functionality
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

### 4. Review Process
- Maintainers will review your PR
- Address any feedback promptly
- Keep the conversation constructive and friendly

## 🎯 Areas for Contribution

### 🧪 Testing & Quality
- Expand test coverage
- Add integration tests
- Improve CI/CD pipeline
- Add performance benchmarks

### 📚 Documentation
- Improve API documentation
- Add more examples and tutorials
- Create video walkthroughs
- Translate documentation

### 🌐 Web Interface
- Enhance UI/UX
- Add dark mode
- Improve mobile responsiveness
- Add real-time caption generation

### 🏆 Sports & Features
- Add support for more sports
- Improve caption accuracy
- Add batch processing
- Implement custom models

### 🚀 Performance & Infrastructure
- Optimize image processing
- Add caching
- Implement Docker support
- Add cloud deployment options

## 💬 Getting Help

### Resources
- 📖 [Project Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/DineshMadhavanM/Image-to-text/issues)
- 💬 [GitHub Discussions](https://github.com/DineshMadhavanM/Image-to-text/discussions)

### Contact
- Create an issue for bugs or feature requests
- Start a discussion for questions
- Mention maintainers for urgent issues

## 🏆 Recognition

Contributors are recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md) - List of all contributors
- Release notes - Specific contributions are highlighted
- README - Top contributors are featured

## 📄 License

By contributing, you agree that your contributions will be licensed under the same [MIT License](LICENSE) as the project.

---

## 🎉 Thank You!

Your contributions help make this project better for everyone. Whether you're fixing bugs, adding features, improving documentation, or just reporting issues, we appreciate your help!

**Happy coding! 🚀**
