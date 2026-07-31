SHELL := /bin/bash

TREE_SITTER_DIR ?= ../tree-sitter-moonbit
GRAMMAR_COMMIT ?= 5435c307c6cf2ef0d508a99047b06f35a4308444
NODE_TYPES := $(TREE_SITTER_DIR)/src/node-types.json

ifeq ($(OS),Windows_NT)
	PYTHON := python
else
	PYTHON := python3
endif

.PHONY: help default grammar-setup clean-grammar grammar-check validate-queries test-syntax zed-log-path zed-log dev watch watch-log

default: help

help:
	@echo "Available targets:"
	@echo "  make help             Show this help message"
	@echo "  make grammar-setup    Clone/update the MoonBit grammar locally"
	@echo "  make clean-grammar    Remove the local MoonBit grammar checkout"
	@echo "  make grammar-check    Check that the pinned grammar exists"
	@echo "  make validate-queries Run all query validation checks"
	@echo "  make test-syntax      Parse MoonBit syntax fixtures"
	@echo "  make zed-log-path     Print the expected Zed log path"
	@echo "  make zed-log          Tail Zed.log"
	@echo "  make dev              Validate queries and open the project in Zed"
	@echo "  make watch            Watch files and re-validate on changes"
	@echo "  make watch-log        Watch + tail Zed log"

grammar-setup:
	@if [ ! -d "$(TREE_SITTER_DIR)" ]; then \
		git clone https://github.com/moonbitlang/tree-sitter-moonbit "$(TREE_SITTER_DIR)"; \
	fi
	@cd "$(TREE_SITTER_DIR)" && git fetch --all --tags --prune && git checkout "$(GRAMMAR_COMMIT)"

grammar-check:
	@if [ ! -f "$(NODE_TYPES)" ]; then \
		echo "Missing $(NODE_TYPES)"; \
		echo "Run: make grammar-setup"; \
		exit 1; \
	fi
	@echo "Grammar node-types found: $(NODE_TYPES)"

clean-grammar:
	@if [ -d "$(TREE_SITTER_DIR)" ]; then \
		echo "Removing Tree-sitter MoonBit grammar at $(TREE_SITTER_DIR)"; \
		rm -rf "$(TREE_SITTER_DIR)"; \
	else \
		echo "No grammar directory found at $(TREE_SITTER_DIR)"; \
	fi

validate-queries: grammar-check
	@$(PYTHON) scripts/validate_queries.py "$(NODE_TYPES)" \
		languages/moonbit/highlights.scm \
		languages/moonbit/outline.scm \
		languages/moonbit/indents.scm \
		languages/moonbit/brackets.scm \
		languages/moonbit/injections.scm

test-syntax: grammar-check
	@TREE_SITTER_DIR="$(TREE_SITTER_DIR)" $(PYTHON) scripts/test_queries.py

zed-log-path:
	@$(PYTHON) scripts/zed_log.py --print-path

zed-log:
	@$(PYTHON) scripts/zed_log.py --tail

dev:
	@$(PYTHON) scripts/dev.py

watch:
	@$(PYTHON) scripts/watch.py --open-zed

watch-log:
	@$(PYTHON) scripts/watch.py --open-zed --log
