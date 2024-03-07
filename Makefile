CUR_DIR := ${CURDIR}
OS := $(shell uname)
.PHONY: clean
clean:
	@echo "cleaning up..."
	@rm -rf ${CUR_DIR}/data/input
	poetry env remove --all
	@rm -rf ${CUR_DIR}/.venv


.PHONY: setup
setup: clean
	@echo "setting up..."
ifeq ($(OS),Darwin)
	@echo "Mac"
else
	@echo "Linux"
endif
	@poetry config virtualenvs.in-project true
	@poetry install --only main -vvv

.PHONY: setup_all
setup_all: clean
	@echo "setting up..."
	@poetry config virtualenvs.in-project true
	@poetry install -vvv

.PHONY: format
format:
	@echo "formatting..."
	@poetry install --only lint
	@poetry run black .
	# ruff fix
	@poetry run pre-commit run --all-files --config .pre-commit-config.yaml

.PHONY: run_tests
run_tests:
	@echo "running tests..."
	@poetry install --only main --only test -vvv
	@poetry run pytest -q tests
