VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest

.PHONY: help venv install install-dev test test-v lint clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

venv: ## Create virtual environment
	python3 -m venv $(VENV)

install: venv ## Install production dependencies
	$(PIP) install -r requirements.txt

install-dev: install ## Install dev dependencies (includes pytest)
	$(PIP) install -r requirements-dev.txt

test: install-dev ## Run all tests
	$(PYTEST) tests/

test-v: install-dev ## Run all tests with verbose output
	$(PYTEST) tests/ -v

test-k: install-dev ## Run tests matching pattern: make test-k K=<pattern>
	$(PYTEST) tests/ -v -k "$(K)"

clean: ## Remove venv and caches
	rm -rf $(VENV) __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null; true
