#!/usr/bin/env bash
set -e

REPO="https://github.com/Jdrc6000/Fossil.git"
MODEL="gpt-oss:20b-cloud"
DEST="/tmp/fossil-$$"

# install ollama if not present
if ! command -v ollama &> /dev/null; then
    echo "installing ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# start if not started already
if ! pgrep -x "ollama" > /dev/null; then
    echo "starting ollama service..."
    ollama serve &> /tmp/ollama.log &
    sleep 3
fi

# pull model if not installed
if ! ollama list 2>/dev/null | grep -q "$MODEL"; then
    echo "pulling $MODEL (this might take a while)..."
    ollama pull "$MODEL"
fi

# clone repo
echo "cloning repo..."
git clone --depth=1 "$REPO" "$DEST"
cd "$DEST"

# install python lib
pip install ollama textual --quiet

echo "starting fossil..."
python3 main_tui.py