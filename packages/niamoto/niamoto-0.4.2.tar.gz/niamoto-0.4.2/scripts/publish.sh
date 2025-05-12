#!/bin/bash
# script publish.sh
# Publishes the package to PyPI using API token authentication

# Get version from pyproject.toml
VERSION=$(grep -o 'version = "[^"]*"' pyproject.toml | cut -d'"' -f2)
echo "Publishing Niamoto version $VERSION"

# Clean and build distribution files
rm -rf dist/
uv build

# Check if PYPI_TOKEN is set in environment
if [ -z "$PYPI_TOKEN" ]; then
  echo "PYPI_TOKEN environment variable not set."
  echo "You can either:"
  echo "1. Set it temporarily: export PYPI_TOKEN=your-token-here"
  echo "2. Continue with manual authentication"
  
  # Standard interactive authentication
  uv publish
else
  echo "Using PyPI token from environment variable"
  # Use token authentication
  UV_PYPI_USER=__token__ UV_PYPI_PASSWORD=$PYPI_TOKEN uv publish
fi
