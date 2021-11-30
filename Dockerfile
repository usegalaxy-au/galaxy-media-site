FROM ubuntu:20.04

# Validate before starting build
WORKDIR /srv/sites/webapp
COPY . .
RUN bash docker/validate.sh

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3.8 \
        python3-pip \
        postgresql-client \
        nginx \
        certbot python3-certbot-nginx \
    && rm -rf /var/lib/apt/lists/*

RUN python3.8 -m pip install --no-cache-dir --upgrade pip && \
    python3.8 -m pip install --no-cache-dir -r requirements.txt

RUN bash docker/setup.sh

EXPOSE 80
EXPOSE 443
