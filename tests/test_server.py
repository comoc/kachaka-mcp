"""
Tests for Kachaka MCP Server.
"""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from kachaka_mcp.server import create_server, KachakaMCPContext


class TestKachakaMCPServer(unittest.TestCase):
    """Kachaka MCP サーバーのテスト"""
    
    def test_create_server(self):
        """サーバー作成のテスト"""
        with patch('kachaka_mcp.server.register_resources') as mock_register_resources, \
             patch('kachaka_mcp.server.register_tools') as mock_register_tools, \
             patch('kachaka_mcp.server.register_prompts') as mock_register_prompts, \
             patch('kachaka_mcp.server.KachakaAuthProvider') as mock_auth_provider, \
             patch('kachaka_mcp.server.load_config') as mock_load_config:
            
            # 設定のモック
            mock_config = MagicMock()
            mock_config.server_name = "Test Server"
            mock_config.auth_enabled = False
            mock_load_config.return_value = mock_config
            
            # サーバーの作成
            server = create_server()
            
            # 各関数が呼ばれたことを確認
            mock_register_resources.assert_called_once()
            mock_register_tools.assert_called_once()
            mock_register_prompts.assert_called_once()
            
            # 認証が無効の場合、認証プロバイダーが作成されないことを確認
            mock_auth_provider.assert_not_called()
            
            # サーバー名が設定されていることを確認
            self.assertEqual(server.name, "Test Server")


if __name__ == '__main__':
    unittest.main()