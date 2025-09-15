# Contributing to DDT Application

Thank you for your interest in contributing to DDT Application! 🎉

## How to Contribute

### 1. Fork the Repository
- Click the "Fork" button on the GitHub page
- Clone your fork locally

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes
- Write clean, readable code
- Follow the existing code style
- Add tests for new features
- Update documentation if needed

### 4. Test Your Changes
```bash
# Run tests
python manage.py test

# Check code style
flake8 .

# Test the application
python manage.py runserver
```

### 5. Commit Changes
```bash
git add .
git commit -m "Add: your feature description"
```

### 6. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## Code Style Guidelines

### Python
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions small and focused

### Django
- Use Django best practices
- Follow the existing model structure
- Use proper form validation
- Add appropriate error handling

### HTML/CSS
- Use semantic HTML
- Follow Bootstrap conventions
- Keep CSS organized and commented
- Use responsive design principles

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment

### Setup Steps
```bash
# Clone repository
git clone https://github.com/PatrikBaldon/DDT-Application.git
cd DDT-Application

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test ddt_app.tests.test_models

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests
- Write tests for new features
- Test edge cases and error conditions
- Use descriptive test names
- Keep tests independent and isolated

## Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Descriptive commit messages

### PR Description
- Clear description of changes
- Reference related issues
- Include screenshots if UI changes
- List any breaking changes

## Issue Guidelines

### Bug Reports
- Use the bug report template
- Include steps to reproduce
- Provide system information
- Add screenshots if applicable

### Feature Requests
- Use the feature request template
- Describe the problem clearly
- Explain the proposed solution
- Consider alternatives

## Release Process

### Version Numbering
- **Major** (1.0.0): Breaking changes
- **Minor** (1.1.0): New features
- **Patch** (1.0.1): Bug fixes

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] Changelog updated
- [ ] Release notes prepared

## Community Guidelines

### Be Respectful
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully

### Be Collaborative
- Help others when possible
- Share knowledge and experience
- Ask questions when needed

### Be Professional
- Keep discussions focused
- Use appropriate language
- Follow the code of conduct

## Getting Help

- **Documentation**: Check the README and code comments
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact us at support@ddt-app.com

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to DDT Application! 🌱