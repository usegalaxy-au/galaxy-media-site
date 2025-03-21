#!/usr/bin/env bash

HOSTNAME=dev-site.gvl.org.au

export ACT_RUNNER=ubuntu-latest

gh act workflow_dispatch \
    -W .github/workflows/deploy-dev.yml \
    -s ANSIBLE_VAULT_PASS="$ANSIBLE_VAULT_PASS" \
    -s SSH_PRIVATE_KEY="$(cat ~/.ssh/github)" \
    -s SSH_KNOWN_HOSTS="$(ssh-keyscan $HOSTNAME)" \
    -s SSH_USER="ubuntu" \
    --container-architecture linux/amd64
