

.default: help

ifeq (${VIRTUAL_ENV},)
  INVENV = poetry run
else
  INVENV =
endif

.PHONY: help
help:
	@echo "USAGE"
	@echo "====="
	@echo ""
	@echo "install-dev (alias: dev)"
	@echo "		installs the project for development"

	@echo "install"
	@echo "		installs the project for deployment"

	@echo "install-ci"
	@echo "		installs the project for CI"

	@echo "lint"
	@echo "		lint all code"

	@echo "fmt"
	@echo "		format all python files"

	@echo "check-fmt"
	@echo "		check formatting for all python files"

	@echo "serve-dev"
	@echo "		serve sblex-server with reloading"

dev: install-dev
install-dev:
	poetry install

install:
	poetry install --only main --sync

# setup CI environment
install-ci: install-dev
	poetry install --only ci

.PHONY: lint
lint:
	${INVENV} ruff app

fmt:
	${INVENV} black app

.PHONY: check-fmt
check-fmt:
	${INVENV} black --check app

# type-check the code
.PHONY: type-check
type-check:
	${INVENV} mypy --config-file mypy.ini app

# build the project
build:
	poetry build

serve-dev:
	${INVENV} watchfiles "uvicorn --bind localhost:8000 app.views:app" app

