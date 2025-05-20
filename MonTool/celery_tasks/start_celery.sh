#!/bin/bash

celery -A celery_tasks.celery worker -l INFO