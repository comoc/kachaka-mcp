#!/bin/bash

# Kachaka MCP サーバーの実行スクリプト

# 現在のディレクトリを取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 仮想環境の有効化
if [ -d "$PROJECT_DIR/.venv" ]; then
    source "$PROJECT_DIR/.venv/bin/activate"
fi

# 環境変数の設定
if [ -f "$PROJECT_DIR/.env" ]; then
    echo "Loading environment variables from .env file..."
    set -a
    source "$PROJECT_DIR/.env"
    set +a
fi

# コマンドライン引数の解析
MODE="run"
KACHAKA_HOST=""

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --dev)
            MODE="dev"
            shift
            ;;
        --install)
            MODE="install"
            shift
            ;;
        --host)
            KACHAKA_HOST="$2"
            shift
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Kachakaホストの設定
if [ -n "$KACHAKA_HOST" ]; then
    export KACHAKA_HOST="$KACHAKA_HOST"
fi

# サーバーの実行
case $MODE in
    run)
        echo "Running Kachaka MCP server..."
        python -m kachaka_mcp.server
        ;;
    dev)
        echo "Running Kachaka MCP server in development mode..."
        mcp dev kachaka_mcp.server
        ;;
    install)
        echo "Installing Kachaka MCP server to Claude Desktop..."
        mcp install kachaka_mcp.server --name "Kachaka Robot"
        ;;
    *)
        echo "Unknown mode: $MODE"
        exit 1
        ;;
esac