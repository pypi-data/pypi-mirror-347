UV ?= uv
PYTHON ?= python3
SRC := ./minigist
TESTS := ./tests

VERSION := $(shell git describe --tags --long | sed -E 's/^v?([0-9.]+)-([0-9]+)-g([0-9a-f]+)/\1.post\2+\3/')

.PHONY: default
default: check

.PHONY: install
install:
	$(UV) sync --all-extras --dev

.PHONY: format
format:
	$(UV) run isort $(SRC) $(TESTS)
	$(UV) run ruff --fix $(SRC) $(TESTS)

.PHONY: check
check:
	$(UV) run ruff format --check $(SRC) $(TESTS)
	$(UV) run ruff check $(SRC) $(TESTS)
	$(UV) run isort --check $(SRC) $(TESTS)
	$(UV) run mypy $(SRC) $(TESTS)
	$(UV) run pytest $(TESTS)

.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info

.PHONY: build-image
build-image:
	podman build \
		--build-arg VERSION=$(VERSION) \
		-t local/minigist .

.PHONY: run-local
run-local:
	podman run \
		--rm \
		--replace \
		--name=minigist \
		-v $(PWD)/config.yaml:/etc/config.yaml:Z \
		local/minigist -- run
