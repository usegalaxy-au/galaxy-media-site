#!/usr/bin/env bash

HOSTNAME=site.usegalaxy.org.au

export ACT_RUNNER=ubuntu-latest

source "$(dirname $0)/../../venv/bin/activate"

gh act workflow_dispatch \
    -W .github/workflows/deploy.yml \
    -s ANSIBLE_VAULT_PASS_BASE64="$ANSIBLE_VAULT_PASS_BASE64" \
    -s SSH_PRIVATE_KEY="$(cat ~/.ssh/github)" \
    -s SSH_USER="ubuntu" \
    --container-architecture linux/amd64
