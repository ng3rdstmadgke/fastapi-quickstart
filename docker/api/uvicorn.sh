#!/bin/bash

# オプション: https://www.uvicorn.org/settings/
uvicorn main:app \
  --log-config "log_config.yml" \
  --workers 2 