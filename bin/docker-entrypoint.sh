#!/bin/sh -e

hostname=$(hostname -f)

case "$1" in
    django)
        echo "Run: $CONTAINER_ENVIRONMENT"
        echo "Application: django"
        log_dir="/var/log/django"
        mkdir -p "${log_dir}"
        access_logfile="${log_dir}/django-access.log"
        error_logfile="${log_dir}/django-error.log"
        case "$CONTAINER_ENVIRONMENT" in
            local)
                echo "Skipping collectstatic&migrations"
                python manage.py runserver 0.0.0.0:8000
                ;;
            *)
                echo "Run: collectstatic"
                python manage.py collectstatic --noinput
                echo "Run: migrations"
                python manage.py migrate --noinput --database deploy
                echo "Run: gunicorn"
                gunicorn config.wsgi:application \
                  -c /code/config/gunicorn.py \
                  --log-level=info \
                  --access-logfile "${access_logfile}" \
                  --error-logfile "${error_logfile}" \
            ;;
        esac
        ;;
    dramatiq)
        echo "Application: Dramatiq"
        log_dir="/var/log/dramatiq"
        mkdir -p "${log_dir}"
        exec python manage.py rundramatiq \
            --queues tickets_default tickets_healthcheck \
            --processes 3 \
            --threads 3 \
            --use-gevent \
            -v 2 \
            --log-file=${log_dir}/dramatiq.log
        ;;
    *)
        exec "$@"
        ;;
esac