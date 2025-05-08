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

def get_context() -> KachakaMCPContext:
    """グローバル変数からコンテキストを取得し存在していなければ作成して返す"""
    global current_context
    
    if current_context is None:
        # 設定の読み込み
        config = load_config()
    
        # Kachaka APIクライアントの初期化
        kachaka_client = KachakaApiClient(target=config.kachaka_host)
    
        # コンテキストの作成と提供
        context = KachakaMCPContext(kachaka_client)
        current_context = context  # グローバル変数に保存
         
    return current_context

def _reset_context() -> None:
    """グローバル変数のコンテキストをリセット"""
    global current_context
    current_context = None

@asynccontextmanager
async def kachaka_lifespan(server: FastMCP) -> AsyncIterator[KachakaMCPContext]:
    """Kachaka MCP サーバーのライフスパン管理"""
    try:
        # コンテキストの作成と提供
        yield get_context()
    finally:
        _reset_context()

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
    
    # コンテキストの作成と提供(もう一度)
    global current_context
    kachaka_client = KachakaApiClient(target=config.kachaka_host)
    context = KachakaMCPContext(kachaka_client)
    current_context = context  # グローバル変数に保存
    
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