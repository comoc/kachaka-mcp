# Kachaka MCP サーバーのインストールスクリプト（PowerShell用）

# 現在のディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

# 仮想環境の作成と有効化
Write-Host "Creating virtual environment..."
python -m venv "$ProjectDir\.venv"
& "$ProjectDir\.venv\Scripts\Activate.ps1"

# 依存関係のインストール
Write-Host "Installing dependencies..."
pip install --upgrade pip
pip install -e "$ProjectDir"

Write-Host "Installation complete!"
Write-Host "To activate the virtual environment, run:"
Write-Host "& '$ProjectDir\.venv\Scripts\Activate.ps1'"
Write-Host ""
Write-Host "To run the server, run:"
Write-Host "kachaka-mcp"
Write-Host "or"
Write-Host "python -m kachaka_mcp.server"