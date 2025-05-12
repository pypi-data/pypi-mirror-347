# Ciphers

A Python tool for ciphering messages using various algorithms.

## Installation

### Using uv (recommended)

```bash
# Install uv if you don't have it
pip install uv

# Create and activate a virtual environment with uv
uv venv
source .venv/bin/activate  # On Linux/macOS
# or
# .venv\Scripts\activate  # On Windows

# Install the package in development mode
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

## Usage

```bash
# Encrypt a message using Caesar cipher with a shift of 3
cipher encrypt --algorithm caesar --key 3 "Hello, World!"

# Decrypt a message using Caesar cipher with a shift of 3
cipher decrypt --algorithm caesar --key 3 "Khoor, Zruog!"
```

## Development

### Installing Development Dependencies

With uv:

```bash
# Install development dependencies
uv pip install -e ".[dev]"
```

With pip:

```bash
# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run tests with pytest
pytest

# Run tests with coverage
pytest --cov=ciphers
```

### Code Formatting and Linting

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint with ruff
ruff check .

# Format with ruff
ruff format .

# Type checking with mypy
mypy ciphers tests
```

### Building and Publishing

Building the package with uv:

```bash
# Build both wheel and sdist
uv build .

# Or build specific formats
uv build --wheel .  # Only wheel
uv build --sdist .  # Only source distribution
```

Publishing to PyPI with uv:

```bash
# Upload to TestPyPI first to verify everything works
uv publish --index testpypi dist/*

# Upload to PyPI
uv publish dist/*
```

You can also use twine if you prefer:

```bash
# Install twine
uv pip install twine

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

## Supported Algorithms

- Caesar Cipher: A simple substitution cipher where each letter is shifted by a fixed number of positions.
