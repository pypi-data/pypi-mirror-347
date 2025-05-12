# Root Makefile for sheetless project

.PHONY: help venv install test lint format docs clean

VENV_DIR := .venv
ACTIVATE := source $(VENV_DIR)/bin/activate
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Available targets:"
	@echo "  venv       Create virtual environment"
	@echo "  install    Install project in dev mode"
	@echo "  test       Run tests with pytest"
	@echo "  lint       Run flake8 linter"
	@echo "  format     Run black formatter"
	@echo "  docs       Build documentation (via docs/Makefile)"
	@echo "  clean      Remove build, dist, and Python artifacts"

venv:
	virtualenv $(VENV_DIR)
	$(PIP) install --upgrade pip setuptools wheel

install: venv
	$(PIP) install -e .[testing]

test:
	$(VENV_DIR)/bin/pytest

lint:
	$(VENV_DIR)/bin/flake8 src tests

format:
	$(VENV_DIR)/bin/black src tests

docs:
	$(MAKE) -C docs html

clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage .mypy_cache
	find . -type d -name "__pycache__" -exec rm -r {} +

build:
	$(PIP) install -e .[dev]
	$(PYTHON) -m build

precommit:
	$(VENV_DIR)/bin/pre-commit install

version: 
	$(VENV_DIR)/bin/python setup.py --version