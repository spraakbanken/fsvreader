default: test

INVENV := if env_var_or_default('VIRTUAL_ENV', "") == "" { "uv run" } else { "" }


alias dev := install-dev
# installs the project for development
install-dev:
	uv sync --dev

# installs the project for deployment
install:
	uv sync --no-dev

# lint all code
lint *flags="":
	{{INVENV}} ruff {{flags}} app

# format all python files
fmt:
	{{INVENV}} ruff format fsvreader tests

# check formatting for all python files
check-fmt:
	{{INVENV}} ruff format --check fsvreader tests

# serve sblex-server with reloading
serve-dev:
	{{INVENV}} watchfiles "gunicorn --chdir fsvreader --bind 'localhost:8000' fsvreader.views:app" fsvreader
