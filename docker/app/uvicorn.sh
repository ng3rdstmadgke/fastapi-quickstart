#!/bin/bash

# オプション: https://www.uvicorn.org/settings/
uvicorn main:app \
  --workers 2 