#!/bin/bash

# Kachaka MCP サーバーのインストールスクリプト

# 現在のディレクトリを取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 仮想環境の作成と有効化
echo "Creating virtual environment..."
python -m venv "$PROJECT_DIR/.venv"
source "$PROJECT_DIR/.venv/bin/activate"

# 依存関係のインストール
echo "Installing dependencies..."
pip install --upgrade pip
pip install -e "$PROJECT_DIR"

echo "Installation complete!"
echo "To activate the virtual environment, run:"
echo "source $PROJECT_DIR/.venv/bin/activate"
echo ""
echo "To run the server, run:"
echo "kachaka-mcp"
echo "or"
echo "python -m kachaka_mcp.server"