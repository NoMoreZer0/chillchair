# Build from python image.
FROM python:3.10

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    openssh-client \
    build-essential \
    gettext \
    libpq-dev \
    wkhtmltopdf  \
    curl \
    procps \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


ARG SSHKEY
ARG KNOWN_HOSTS
ENV PYTHONUNBUFFERED 1

RUN : "---------- install uv --------------" \
    && pip install --upgrade pip \
    && pip install uv==0.5.18

# Set python requirements
WORKDIR /code

# Install python dependencies
COPY ./requirements.txt /code
RUN uv pip sync requirements.txt --system

# Set volume for database and static files.
RUN mkdir -p /static /media

# Copy source code
COPY . /code

# Collect static
#RUN python manage.py collectstatic --noinput

#RUN #pwd

ENTRYPOINT ["./bin/docker-entrypoint.sh"]
#
HEALTHCHECK \
    --start-period=15s \
    --timeout=14s \
    --retries=1 \
    --interval=20s \
    CMD ./bin/healthcheck.sh