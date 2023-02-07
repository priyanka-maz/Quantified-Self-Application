#!/usr/bin/sh

MailHog &
celery -A main.celery worker -l INFO &
celery -A main.celery beat --max-interval 1 -l INFO &
python main.py

pkill celery
pkill MailHog
