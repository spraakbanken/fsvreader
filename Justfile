default: test

INVENV := if env_var_or_default('VIRTUAL_ENV', "") == "" { "rye run" } else { "" }


alias dev := install-dev
# installs the project for development
install-dev:
	rye sync --no-lock

# installs the project for deployment
install:
	rye sync --no-lock --no-dev

# setup CI environment
install-ci: install-dev
	rye sync --no-lock --features=ci


# lint all code
lint *flags="":
	{{INVENV}} ruff {{flags}} app

# format all python files
fmt:
	{{INVENV}} black src tests

# check formatting for all python files
check-fmt:
	{{INVENV}} black --check src tests

# serve sblex-server with reloading
serve-dev:
	{{INVENV}} watchfiles "gunicorn --chdir app --bind 'localhost:8000' app.views:app" app

