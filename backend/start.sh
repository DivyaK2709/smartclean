#!/usr/bin/env bash
set -e

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Starting server..."
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
