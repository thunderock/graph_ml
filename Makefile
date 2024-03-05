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
	# python3 -m keyring --disable
endif
	@poetry config virtualenvs.in-project true
	@poetry install

.PHONY: format
format:
	@echo "formatting..."
	@poetry run black .