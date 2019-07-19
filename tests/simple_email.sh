#!/usr/bin/env bash

exec curl -d @'simple_email.json' -H 'Content-Type: application/json' \
          -X POST 'http://localhost:8000'
