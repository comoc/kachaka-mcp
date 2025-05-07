"""
Kachaka MCP Server

Main server implementation for Kachaka MCP.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from kachaka_api.aio import KachakaApiClient
from mcp.server.fastmcp import Context, FastMCP

from .resources import register_resources
from .tools import register_tools
from .prompts import register_prompts
from .auth import KachakaAuthProvider
from .utils.config import load_config


# グローバル変数としてコンテキストを保存
current_context = None

class KachakaMCPContext:
    """Kachaka MCP サーバーのコンテキスト"""
    def __init__(self, kachaka_client: KachakaApiClient):
        self.kachaka_client = kachaka_client


@asynccontextmanager
async def kachaka_lifespan(server: FastMCP) -> AsyncIterator[KachakaMCPContext]:
    """Kachaka MCP サーバーのライフスパン管理"""
    global current_context
    
    # 設定の読み込み
    config = load_config()
    
    # Kachaka APIクライアントの初期化
    kachaka_client = KachakaApiClient(target=config.kachaka_host)
    
    try:
        # コンテキストの作成と提供
        context = KachakaMCPContext(kachaka_client)
        current_context = context  # グローバル変数に保存
        yield context
    finally:
        # クリーンアップ処理
        current_context = None


def create_server(server_name: str = None) -> FastMCP:
    """Kachaka MCP サーバーを作成"""
    # 設定の読み込み
    config = load_config()
    
    # サーバー名の設定
    if server_name is None:
        server_name = config.server_name
    
    # MCPサーバーの作成
    try:
        # 認証プロバイダーを使用する場合
        if config.auth_enabled:
            mcp = FastMCP(
                server_name,
                lifespan=kachaka_lifespan,
                auth_provider=KachakaAuthProvider(),
            )
        else:
            # 認証なしの場合
            mcp = FastMCP(
                server_name,
                lifespan=kachaka_lifespan,
            )
    except Exception as e:
        # エラーが発生した場合は、認証なしで再試行
        print(f"認証プロバイダーの初期化に失敗しました: {e}")
        print("認証なしでサーバーを起動します。")
        mcp = FastMCP(
            server_name,
            lifespan=kachaka_lifespan,
        )
    
    # リソース、ツール、プロンプトの登録
    register_resources(mcp)
    register_tools(mcp)
    register_prompts(mcp)
    
    return mcp


def main():
    """メイン関数"""
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()