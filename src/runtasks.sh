#!/usr/bin/env bash

exec celery -qA tasks.send_email worker
