VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest

.PHONY: help venv install install-dev test test-v test-k build validate serve dev clean

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

build: ## Generate pyscript.toml with file mappings
	@echo '[files]' > pyscript.toml
	@find src -name '*.py' ! -path '*__pycache__*' | sort | while read f; do \
		echo "\"./$$f\" = \"./$$f\""; \
	done >> pyscript.toml
	@echo "[build] pyscript.toml updated"
	@$(MAKE) --no-print-directory validate

validate: ## Validate pyscript.toml for TOML syntax errors (duplicate keys, etc.)
	@python3 -c "import tomllib, sys; tomllib.load(open('pyscript.toml','rb')); print('[validate] pyscript.toml OK')" \
		|| (echo '[validate] pyscript.toml INVALID'; exit 1)

serve: build ## Build and serve the app at http://localhost:8000
	python3 -m http.server 8000

dev: install-dev build ## Serve with auto-rebuild on src/ changes (reload browser manually)
	$(VENV)/bin/watchmedo shell-command \
		--patterns="*.py" \
		--recursive \
		--command='$(MAKE) build' \
		src/ &
	python3 -m http.server 8000

clean: ## Remove venv, caches, and build artifacts
	rm -rf $(VENV) __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null; true
