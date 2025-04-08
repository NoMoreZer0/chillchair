#!/bin/sh -e

case "$CONTAINER_ENVIRONMENT" in
    prod|test|local)
        # we are healthy if we respond on 8000 or if dramatiq is running
        for i in {1..3}; do
            if curl --fail -L http://localhost:8000/status.html || pgrep dramatiq ; then
                sleep 3
            else
                echo "Healthcheck failed"
                exit 1
            fi
        done
        ;;
esac