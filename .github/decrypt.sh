#!/bin/sh

gpg --quiet --batch --yes --decrypt --passphrase="$PASSPHRASE" \
--output ../app/secret_key.txt secret_key.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$PASSPHRASE" \
--output ../app/client_secret.json client_secret.gpg
