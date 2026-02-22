VENV := .venv
PYTHON := $(VENV)/bin/python

.PHONY: install crawl agents run help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Create venv & install deps
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
	$(VENV)/bin/playwright install chromium

crawl: ## Crawl only — save screenshots + data, no AI
	$(PYTHON) run.py --crawl-only

agents: ## Run agents on saved crawl data (skip crawl)
	$(PYTHON) run.py --agents-only

run: ## Full run: crawl + agents + council + report
	$(PYTHON) run.py

clean: ## Remove reports and crawl data
	rm -rf reports/
