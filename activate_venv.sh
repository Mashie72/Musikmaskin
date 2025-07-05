#!/bin/bash

VENV_DIR=".venv"
ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"

if [ -f "$ACTIVATE_SCRIPT" ]; then
    echo "✅ Hittade venv, försöker aktivera..."
    source "$ACTIVATE_SCRIPT"
    echo "🧪 Venv aktiv? Python: $(which python)"
    echo "🐍 Version: $(python --version)"
else
    echo "❌ Venv hittades inte i $VENV_DIR"
fi
