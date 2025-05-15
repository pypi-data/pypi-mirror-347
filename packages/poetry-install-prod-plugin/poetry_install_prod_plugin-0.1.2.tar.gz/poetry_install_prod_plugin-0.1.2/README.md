# Install Prod

Adds a command `poetry install-prod` which forces local (path) dependencies to be installed in non-editable mode, even when marked as editable. This is particularly useful for monorepo architectures with many cross-dependencies. In a development environment it is desireable to install local (path) dependencies as symbolic links so they are editable, but in a production or CI/CD environment it is necessary to install all dependencies as non-editable.
