# Kachaka MCP サーバーの実行スクリプト（PowerShell用）

# 現在のディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

# パラメータの定義
param(
    [switch]$Dev,
    [switch]$Install,
    [string]$Host
)

# 仮想環境の有効化
if (Test-Path "$ProjectDir\.venv") {
    & "$ProjectDir\.venv\Scripts\Activate.ps1"
}

# 環境変数の設定
if (Test-Path "$ProjectDir\.env") {
    Write-Host "Loading environment variables from .env file..."
    Get-Content "$ProjectDir\.env" | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value)
        }
    }
}

# モードの設定
$Mode = "run"
if ($Dev) {
    $Mode = "dev"
}
if ($Install) {
    $Mode = "install"
}

# Kachakaホストの設定
if ($Host) {
    $env:KACHAKA_HOST = $Host
}

# サーバーの実行
switch ($Mode) {
    "run" {
        Write-Host "Running Kachaka MCP server..."
        python -m kachaka_mcp.server
    }
    "dev" {
        Write-Host "Running Kachaka MCP server in development mode..."
        mcp dev kachaka_mcp.server
    }
    "install" {
        Write-Host "Installing Kachaka MCP server to Claude Desktop..."
        mcp install kachaka_mcp.server --name "Kachaka Robot"
    }
    default {
        Write-Host "Unknown mode: $Mode"
        exit 1
    }
}