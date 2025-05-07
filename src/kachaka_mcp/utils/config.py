"""
Configuration management for Kachaka MCP Server.
"""

import os
import json
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field


class KachakaMCPConfig(BaseModel):
    """Kachaka MCP サーバーの設定"""
    kachaka_host: str = Field(
        default="100.94.1.1:26400",
        description="Kachakaロボットのホスト（IPアドレス:ポート）"
    )
    server_name: str = Field(
        default="Kachaka Robot",
        description="MCPサーバーの名前"
    )
    log_level: str = Field(
        default="INFO",
        description="ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）"
    )
    auth_enabled: bool = Field(
        default=False,
        description="認証を有効にするかどうか"
    )
    api_keys: List[str] = Field(
        default_factory=list,
        description="APIキーのリスト"
    )


def load_config() -> KachakaMCPConfig:
    """設定を読み込む"""
    # 環境変数から設定ファイルのパスを取得
    config_path = os.environ.get("KACHAKA_MCP_CONFIG")
    
    # 環境変数が設定されていない場合はデフォルトのパスを使用
    if not config_path:
        config_path = "~/.kachaka-mcp/config.json"
    
    # パスを展開
    config_path = Path(config_path).expanduser()
    
    # デフォルト設定
    config = KachakaMCPConfig()
    
    # 設定ファイルが存在する場合は読み込む
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config_data = json.load(f)
                config = KachakaMCPConfig(**config_data)
        except Exception as e:
            print(f"設定ファイルの読み込みに失敗しました: {e}")
    
    # 環境変数で上書き
    if os.environ.get("KACHAKA_HOST"):
        config.kachaka_host = os.environ.get("KACHAKA_HOST")
    
    if os.environ.get("KACHAKA_MCP_SERVER_NAME"):
        config.server_name = os.environ.get("KACHAKA_MCP_SERVER_NAME")
    
    if os.environ.get("KACHAKA_MCP_LOG_LEVEL"):
        config.log_level = os.environ.get("KACHAKA_MCP_LOG_LEVEL")
    
    if os.environ.get("KACHAKA_MCP_AUTH_ENABLED"):
        config.auth_enabled = os.environ.get("KACHAKA_MCP_AUTH_ENABLED").lower() in ("true", "1", "yes")
    
    if os.environ.get("KACHAKA_MCP_API_KEYS"):
        config.api_keys = os.environ.get("KACHAKA_MCP_API_KEYS").split(",")
    
    return config


def save_config(config: KachakaMCPConfig, config_path: Optional[str] = None) -> None:
    """設定を保存する"""
    # 環境変数から設定ファイルのパスを取得
    if not config_path:
        config_path = os.environ.get("KACHAKA_MCP_CONFIG", "~/.kachaka-mcp/config.json")
    
    # パスを展開
    config_path = Path(config_path).expanduser()
    
    # ディレクトリが存在しない場合は作成
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 設定を保存
    with open(config_path, "w") as f:
        json.dump(config.model_dump(), f, indent=2)