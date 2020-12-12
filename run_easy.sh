#!/bin/bash

# Loads and exports the .env variables so that they can be accessed by 
# child processes.
(export $(cat .env | xargs) && \
venv/bin/gunicorn \
--bind unix:/run/${SITENAME}.socket superlists.wsgi:application)
