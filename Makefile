CUR_DIR := ${CURDIR}
OS := $(shell uname)
.PHONY: clean
clean:
	@echo "cleaning up..."
	@rm -rf ${CUR_DIR}/data/input
	poetry env remove --all
	@rm -rf ${CUR_DIR}/.venv ${CUR_DIR}/build ${CUR_DIR}/.pytest_cache


.PHONY: setup
setup:
	@echo "setting up..."
ifeq ($(OS),Darwin)
	@echo "Mac"
else
	@echo "Linux"
endif
	@poetry config virtualenvs.in-project true
	@poetry install --only main -vvv

.PHONY: setup_all
setup_all:
	@echo "setting up..."
	@poetry config virtualenvs.in-project true
	@poetry install --only main --only jupyter --only test --only lint -vvv
	@poetry run poetry run jupyter contrib nbextension install --user
	@poetry run jupyter nbextension enable --py codeium --user
	@poetry run jupyter serverextension enable --py codeium --user

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

.PHONY: run_notebook
run_notebook:
	@echo "running notebook..."
	@poetry config virtualenvs.in-project true
	@poetry install --only main --only jupyter -vvv
	@poetry run poetry run jupyter contrib nbextension install --user
	@poetry run jupyter nbextension enable --py codeium --user
	@poetry run jupyter serverextension enable --py codeium --user
	@poetry run jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser
