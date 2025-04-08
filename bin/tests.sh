#!/bin/sh
set -e

export CONTAINER_ENVIRONMENT=ci

echo "Checking migrations"
python manage.py makemigrations --check --dry-run --noinput
echo "Migrations are OK"

# Run coverage
coverage erase

# Check formatting
echo "Checking formatting"
ruff format --check .

ruff check app/

pytest --cov=app --cov-branch --cov-fail-under=90 --cov-report xml --cov-report term-missing:skip-covered

# Send coverage to codecov if configured.
if [ "$CODECOV_TOKEN" ]; then
    if [ "$GITHUB_PR" ]; then
        codecov_args=" --pr $GITHUB_PR "
    fi
    curl https://keybase.io/codecovsecurity/pgp_keys.asc | gpg --no-default-keyring --keyring trustedkeys.gpg --import
    curl -Os https://uploader.codecov.io/latest/linux/codecov
    curl -Os https://uploader.codecov.io/latest/linux/codecov.SHA256SUM
    curl -Os https://uploader.codecov.io/latest/linux/codecov.SHA256SUM.sig
    gpgv codecov.SHA256SUM.sig codecov.SHA256SUM
    shasum -a 256 -c codecov.SHA256SUM
    chmod +x codecov
    ./codecov -t ${CODECOV_TOKEN} $codecov_args
fi