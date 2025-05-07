@echo off
REM Kachaka MCP サーバーの実行スクリプト（Windows用）

REM 現在のディレクトリを取得
set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..

REM 仮想環境の有効化
if exist "%PROJECT_DIR%\.venv" (
    call "%PROJECT_DIR%\.venv\Scripts\activate.bat"
)

REM 環境変数の設定
if exist "%PROJECT_DIR%\.env" (
    echo Loading environment variables from .env file...
    for /f "tokens=*" %%a in (%PROJECT_DIR%\.env) do (
        set %%a
    )
)

REM コマンドライン引数の解析
set MODE=run
set KACHAKA_HOST=

:parse_args
if "%~1"=="" goto end_parse_args
if "%~1"=="--dev" (
    set MODE=dev
    shift
    goto parse_args
)
if "%~1"=="--install" (
    set MODE=install
    shift
    goto parse_args
)
if "%~1"=="--host" (
    set KACHAKA_HOST=%~2
    shift
    shift
    goto parse_args
)
echo Unknown option: %~1
exit /b 1

:end_parse_args

REM Kachakaホストの設定
if not "%KACHAKA_HOST%"=="" (
    set KACHAKA_HOST=%KACHAKA_HOST%
)

REM サーバーの実行
if "%MODE%"=="run" (
    echo Running Kachaka MCP server...
    python -m kachaka_mcp.server
) else if "%MODE%"=="dev" (
    echo Running Kachaka MCP server in development mode...
    mcp dev kachaka_mcp.server
) else if "%MODE%"=="install" (
    echo Installing Kachaka MCP server to Claude Desktop...
    mcp install kachaka_mcp.server --name "Kachaka Robot"
) else (
    echo Unknown mode: %MODE%
    exit /b 1
)