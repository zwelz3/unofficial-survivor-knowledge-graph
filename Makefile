.PHONY: all install generate expand test validate clean docs

PYTHON ?= python3
PIP ?= pip

# ── primary targets ──────────────────────────────────────────────────

all: install generate expand test validate

install:
	$(PIP) install -e ".[dev]" --break-system-packages

generate:
	$(PYTHON) scripts/generate_data.py

expand:
	$(PYTHON) scripts/expand_to_rdf.py

test:
	$(PYTHON) -m pytest tests/ -v

validate:
	$(PYTHON) scripts/validate_shacl.py

# ── research pipeline (per-season) ──────────────────────────────────

research-season-%:
	$(PYTHON) scripts/research_episode.py --season $*

extract-season-%:
	$(PYTHON) scripts/extract_entities.py --season $*

# ── documentation ────────────────────────────────────────────────────

docs:
	cd docs && mkdocs build

docs-serve:
	cd docs && mkdocs serve

# ── cleanup ──────────────────────────────────────────────────────────

clean:
	rm -rf output/
	rm -rf data/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

clean-research:
	rm -rf research/raw/*
	rm -rf research/provenance/*

# ── stats ────────────────────────────────────────────────────────────

stats:
	@echo "=== Data Stats ==="
	@echo "Season dirs: $$(ls -d data/season-* 2>/dev/null | wc -l)"
	@echo "Episode files: $$(find data/ -name 'e*.json' 2>/dev/null | wc -l)"
	@echo "Season files: $$(find data/ -name 'season.json' 2>/dev/null | wc -l)"
	@echo "Research docs: $$(find research/raw/ -name '*.md' 2>/dev/null | wc -l)"
	@echo "Provenance docs: $$(find research/provenance/ -name '*.jsonld' 2>/dev/null | wc -l)"
	@test -f output/survivor.trig && echo "RDF triples: $$(wc -l < output/survivor.nq)" || echo "RDF: not yet generated"
