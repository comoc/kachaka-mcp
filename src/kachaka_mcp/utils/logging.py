"""
Logging utilities for Kachaka MCP Server.
"""

import sys
from pathlib import Path

from loguru import logger

from .config import load_config


def setup_logging():
    """ロギングの設定"""
    # 設定の読み込み
    config = load_config()
    
    # ログレベルの設定
    log_level = config.log_level
    
    # ログファイルのパス
    log_dir = Path.home() / ".kachaka-mcp" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "kachaka-mcp.log"
    
    # ロガーの設定
    logger.remove()  # デフォルトのハンドラを削除
    
    # 標準出力へのログ
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    
    # ファイルへのログ
    logger.add(
        log_file,
        rotation="10 MB",  # 10MBごとにローテーション
        retention="1 week",  # 1週間分のログを保持
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )
    
    logger.info(f"Logging initialized with level: {log_level}")
    
    return logger