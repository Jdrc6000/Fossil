#!/usr/bin/env bash
set -e

REPO="https://github.com/Jdrc6000/Fossil.git"
MODEL="gpt-oss:20b-cloud"
DEST="/tmp/fossil-$$"

cleanup() { rm -rf "$DEST"; }
trap cleanup EXIT

# python check
if ! python3 -c "import sys; assert sys.version_info >= (3,10)" 2>/dev/null; then
    echo "error: Python 3.10+ required"
    exit 1
fi

# ollama install
if ! command -v ollama &>/dev/null; then
    echo "installing ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# start ollama and wait until it's actually responding
if ! pgrep -x ollama &>/dev/null; then
    echo "starting ollama service..."
    ollama serve &>/tmp/ollama.log &
    echo "waiting for ollama..."
    for i in $(seq 1 15); do
        ollama list &>/dev/null && break
        sleep 1
    done
fi

# pull model
if ! ollama list 2>/dev/null | grep -q "$MODEL"; then
    echo "pulling $MODEL (this might take a while)..."
    ollama pull "$MODEL"
fi

echo "cloning repo..."
git clone --depth=1 "$REPO" "$DEST"
cd "$DEST"

pip install ollama textual --break-system-packages --quiet

echo "starting fossil..."
python3 main_tui.py </dev/tty