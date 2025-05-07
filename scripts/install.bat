@echo off
REM Kachaka MCP サーバーのインストールスクリプト（Windows用）

REM 現在のディレクトリを取得
set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..

REM 仮想環境の作成と有効化
echo Creating virtual environment...
python -m venv "%PROJECT_DIR%\.venv"
call "%PROJECT_DIR%\.venv\Scripts\activate.bat"

REM 依存関係のインストール
echo Installing dependencies...
pip install --upgrade pip
pip install -e "%PROJECT_DIR%"

echo Installation complete!
echo To activate the virtual environment, run:
echo call "%PROJECT_DIR%\.venv\Scripts\activate.bat"
echo.
echo To run the server, run:
echo kachaka-mcp
echo or
echo python -m kachaka_mcp.server