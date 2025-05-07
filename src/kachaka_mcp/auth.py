"""
Authentication provider for Kachaka MCP Server.
"""

from typing import Dict, List, Optional, Set

# MCP SDKのバージョンによって認証関連のクラスが異なる可能性があるため、
# 簡易的な認証プロバイダーを実装
class KachakaAuthProvider:
    """Kachaka MCP サーバーの認証プロバイダー（簡易版）"""
    
    def __init__(self):
        """初期化"""
        from .utils.config import load_config
        self.config = load_config()
        self.api_keys: Set[str] = set(self.config.api_keys)
        self.clients: Dict[str, Dict] = {}
    
    async def validate_client_credentials(self, client_id: str, client_secret: str) -> bool:
        """クライアント認証情報の検証
        
        Args:
            client_id: クライアントID
            client_secret: クライアントシークレット（APIキー）
            
        Returns:
            認証情報が有効かどうか
        """
        # APIキーが設定されていない場合は認証を無効化
        if not self.api_keys:
            return True
        
        return client_secret in self.api_keys