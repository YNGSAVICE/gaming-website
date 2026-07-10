# Contributing to Gaming Website

Thank you for your interest in contributing! Here's how you can help:

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure as needed
6. Run the app: `python backend/run.py`

## Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Write or update tests
4. Commit with clear messages: `git commit -am 'Add new feature'`
5. Push to your fork: `git push origin feature/your-feature`
6. Create a Pull Request

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions
- Write tests for new functionality

## Running Tests

```bash
pytest tests/ -v --cov=backend
```

## Reporting Issues

Create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment details

## Questions?

Open a discussion or contact the maintainers.
