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
	@poetry run black .
	@poetry run pre-commit run --all-files
