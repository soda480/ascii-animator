SHELL := /bin/bash
VENV ?= .venv
PKG  ?= ascii_animator

# Cross-platform venv bin paths
ifeq ($(OS),Windows_NT)
  BIN := $(VENV)/Scripts
else
  BIN := $(VENV)/bin
endif

PY  := $(BIN)/python3
PIP := $(BIN)/pip

# ANSI color codes
YELLOW := \033[1;33m
RESET := \033[0m

.PHONY: dev venv lint test coverage cc bandit build clean scrub

help:
	@printf "$(YELLOW)Available commands:$(RESET)\n"
	@printf "  make venv           - Create a virtual environment with project dependencies\n"
	@printf "  make lint           - Lint source code\n"
	@printf "  make test           - Run unit tests\n"
	@printf "  make coverage       - Measure test code coverage\n"
	@printf "  make cc             - Compute cyclomatic complexity\n"
	@printf "  make bandit         - Run bandit security scan\n"
	@printf "  make build          - Build source and wheel distributions\n"
	@printf "  make dist           - Validate built distributions\n"
	@printf "  make publish        - Upload package to PyPI\n"
	@printf "  make clean          - Remove build and test artifacts\n"
	@printf "  make scrub          - Remove virtual environment\n"
	@printf "  make dev            - Execute development pipeline (venv lint test coverage cc bandit build)\n"

dev: venv lint cc test bandit coverage build
	@printf "$(YELLOW)Development pipeline complete.$(RESET)\n"

# Rebuild the venv only when pyproject.toml changes
venv: $(VENV)/.stamp

$(VENV)/.stamp: pyproject.toml
	@printf "$(YELLOW)Ensuring virtual environment exists at $(VENV)...$(RESET)\n"
	@python3 -m venv $(VENV)
	@printf "$(YELLOW)Upgrading pip...$(RESET)\n"
	@$(PIP) install --upgrade pip
	@printf "$(YELLOW)Installing project in editable mode with dev extras... $(RESET)\n"
	@$(PIP) install -e .[dev]
	@# Touch the stamp file to record the last successful build time
	@touch $@

lint: venv
	@printf "$(YELLOW)Linting source code...$(RESET)\n"
	$(PY) -m flake8 -v $(PKG)/ --max-line-length 100 --ignore=E302,E305,W503,F405,F403,E501,E722

test: venv
	@printf "$(YELLOW)Running unit tests...$(RESET)\n"
	$(PY) -m unittest discover tests/ -v

coverage: venv
	@printf "$(YELLOW)Running test code coverage report...$(RESET)\n"
	$(PY) -m coverage run -m unittest discover tests/
	$(PY) -m coverage report -m
	mkdir -p docs/badges
	$(PY) -m coverage xml -o coverage.xml
	$(BIN)/genbadge coverage -i coverage.xml -o docs/badges/coverage.svg

cc: venv
	@printf "$(YELLOW)Determining cyclomatic complecity...$(RESET)\n"
	$(PY) -m radon cc -s $(PKG)/

bandit: venv
	@printf "$(YELLOW)Executing bandit security scan...$(RESET)\n"
	$(PY) -m bandit -r $(PKG)/ --skip B606,B311,B110

build: venv
	@printf "$(YELLOW)Building source and wheel distributions...$(RESET)\n"
	$(PY) -m build

dist: build
	@printf "$(YELLOW)Checking built distributions...$(RESET)\n"
	$(BIN)/twine check dist/*

publish: dist
	@printf "$(YELLOW)Uploading to PyPI...$(RESET)\n"
	$(BIN)/twine upload \
		--non-interactive --skip-existing \
		--repository pypi \
		--verbose \
		dist/*

clean:
	@printf "$(YELLOW)Cleaning up build and test artifacts...$(RESET)\n"
	rm -rf .pytest_cache .coverage coverage.xml htmlcov build dist *.egg-info docs/badges/coverage.svg
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

scrub: clean
	@printf "$(YELLOW)Removing virtual environment...$(RESET)\n"
	rm -rf $(VENV)