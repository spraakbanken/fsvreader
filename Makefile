

.default: help

ifeq (${VIRTUAL_ENV},)
  INVENV = rye run
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
	rye sync --no-lock

install:
	rye sync --no-dev --no-lock

# setup CI environment
install-ci: install-dev
	rye sync --no-lock --features=ci

.PHONY: lint
lint:
	${INVENV} ruff app

fmt:
	${INVENV} ruff format app

.PHONY: check-fmt
check-fmt:
	${INVENV} ruff format --check app

# type-check the code
.PHONY: type-check
type-check:
	${INVENV} mypy --config-file mypy.ini app

# build the project
build:
	rye build

serve-dev:
	${INVENV} watchfiles "gunicorn --chdir app --bind 'localhost:8000' app.views:app" app
