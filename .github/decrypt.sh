#!/bin/sh

ls

gpg --quiet --batch --yes --decrypt --passphrase="$PASSPHRASE" \
--output app/secret_key.txt .github/secret_key.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$PASSPHRASE" \
--output app/client_secret.json .github/client_secret.gpg
