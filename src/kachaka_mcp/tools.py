"""
Tools for Kachaka MCP Server.

This module defines the tools that are exposed by the Kachaka MCP Server.
"""

from typing import Dict, Any, List, Optional

from mcp.server.fastmcp import FastMCP, Context
from loguru import logger


def register_tools(mcp: FastMCP) -> None:
    """ツールの登録
    
    Args:
        mcp: MCPサーバーインスタンス
    """
    # 移動ツール
    register_movement_tools(mcp)
    
    # 棚操作ツール
    register_shelf_tools(mcp)
    
    # システム操作ツール
    register_system_tools(mcp)
    
    # マップ操作ツール
    register_map_tools(mcp)


def register_movement_tools(mcp: FastMCP) -> None:
    """移動ツールの登録
    
    Args:
        mcp: MCPサーバーインスタンス
    """
    @mcp.tool()
    async def move_to_location(location_name: str) -> str:
        """指定した場所にロボットを移動させる
        
        Args:
            location_name: 移動先の場所の名前またはID
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Moving to location: {location_name}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 進捗報告の設定
            ctx.info(f"Moving to location: {location_name}")
            
            # 移動コマンドの実行
            result = await kachaka_client.move_to_location(
                location_name,
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return f"Successfully moved to {location_name}"
            else:
                return f"Failed to move to {location_name}: {result.message}"
        except Exception as e:
            logger.error(f"Error moving to location: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def move_to_pose(x: float, y: float, yaw: float) -> str:
        """指定した座標に移動
        
        Args:
            x: X座標
            y: Y座標
            yaw: 向き（ラジアン）
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Moving to pose: x={x}, y={y}, yaw={yaw}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 進捗報告の設定
            ctx.info(f"Moving to pose: x={x}, y={y}, yaw={yaw}")
            
            # 移動コマンドの実行
            result = await kachaka_client.move_to_pose(
                x, y, yaw,
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return f"Successfully moved to pose: x={x}, y={y}, yaw={yaw}"
            else:
                return f"Failed to move to pose: {result.message}"
        except Exception as e:
            logger.error(f"Error moving to pose: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def return_home() -> str:
        """ホームに戻る
        
        Returns:
            実行結果のメッセージ
        """
        logger.info("Returning home")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 進捗報告の設定
            ctx.info("Returning home")
            
            # ホームに戻るコマンドの実行
            result = await kachaka_client.return_home(
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return "Successfully returned home"
            else:
                return f"Failed to return home: {result.message}"
        except Exception as e:
            logger.error(f"Error returning home: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def move_forward(distance_meter: float, speed: float = 0.0) -> str:
        """指定した距離前進
        
        Args:
            distance_meter: 前進する距離（メートル）
            speed: 速度（メートル/秒）、0.0の場合はデフォルト速度
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Moving forward: distance={distance_meter}m, speed={speed}m/s")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 進捗報告の設定
            ctx.info(f"Moving forward: distance={distance_meter}m, speed={speed}m/s")
            
            # 前進コマンドの実行
            result = await kachaka_client.move_forward(
                distance_meter,
                speed=speed,
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return f"Successfully moved forward {distance_meter}m"
            else:
                return f"Failed to move forward: {result.message}"
        except Exception as e:
            logger.error(f"Error moving forward: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def rotate_in_place(angle_radian: float) -> str:
        """その場で回転
        
        Args:
            angle_radian: 回転角度（ラジアン）
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Rotating in place: angle={angle_radian}rad")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 進捗報告の設定
            ctx.info(f"Rotating in place: angle={angle_radian}rad")
            
            # 回転コマンドの実行
            result = await kachaka_client.rotate_in_place(
                angle_radian,
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return f"Successfully rotated {angle_radian}rad"
            else:
                return f"Failed to rotate: {result.message}"
        except Exception as e:
            logger.error(f"Error rotating in place: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def set_robot_velocity(linear: float, angular: float) -> str:
        """ロボットの速度を設定
        
        Args:
            linear: 直進速度（メートル/秒）
            angular: 回転速度（ラジアン/秒）
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Setting robot velocity: linear={linear}m/s, angular={angular}rad/s")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 速度設定コマンドの実行
            result = await kachaka_client.set_robot_velocity(linear, angular)
            
            # 結果の返却
            if result.success:
                return f"Successfully set robot velocity: linear={linear}m/s, angular={angular}rad/s"
            else:
                return f"Failed to set robot velocity: {result.message}"
        except Exception as e:
            logger.error(f"Error setting robot velocity: {e}")
            return f"Error: {str(e)}"


def register_shelf_tools(mcp: FastMCP) -> None:
    """棚操作ツールの登録
    
    Args:
        mcp: MCPサーバーインスタンス
    """
    @mcp.tool()
    async def move_shelf(shelf_name: str, location_name: str) -> str:
        """棚を指定した場所に移動
        
        Args:
            shelf_name: 移動する棚の名前またはID
            location_name: 移動先の場所の名前またはID
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Moving shelf {shelf_name} to location {location_name}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 進捗報告の設定
            ctx.info(f"Moving shelf {shelf_name} to location {location_name}")
            
            # 棚移動コマンドの実行
            result = await kachaka_client.move_shelf(
                shelf_name,
                location_name,
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return f"Successfully moved shelf {shelf_name} to location {location_name}"
            else:
                return f"Failed to move shelf: {result.message}"
        except Exception as e:
            logger.error(f"Error moving shelf: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def return_shelf(shelf_name: str = "") -> str:
        """棚を元の場所に戻す
        
        Args:
            shelf_name: 戻す棚の名前またはID（空文字列の場合は現在持っている棚）
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Returning shelf {shelf_name if shelf_name else '(current)'}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 進捗報告の設定
            ctx.info(f"Returning shelf {shelf_name if shelf_name else '(current)'}")
            
            # 棚を戻すコマンドの実行
            result = await kachaka_client.return_shelf(
                shelf_name,
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return f"Successfully returned shelf {shelf_name if shelf_name else '(current)'}"
            else:
                return f"Failed to return shelf: {result.message}"
        except Exception as e:
            logger.error(f"Error returning shelf: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def dock_shelf() -> str:
        """棚にドッキング
        
        Returns:
            実行結果のメッセージ
        """
        logger.info("Docking shelf")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 進捗報告の設定
            ctx.info("Docking shelf")
            
            # ドッキングコマンドの実行
            result = await kachaka_client.dock_shelf(
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return "Successfully docked shelf"
            else:
                return f"Failed to dock shelf: {result.message}"
        except Exception as e:
            logger.error(f"Error docking shelf: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def undock_shelf() -> str:
        """棚からアンドック
        
        Returns:
            実行結果のメッセージ
        """
        logger.info("Undocking shelf")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 進捗報告の設定
            ctx.info("Undocking shelf")
            
            # アンドックコマンドの実行
            result = await kachaka_client.undock_shelf(
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return "Successfully undocked shelf"
            else:
                return f"Failed to undock shelf: {result.message}"
        except Exception as e:
            logger.error(f"Error undocking shelf: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def dock_any_shelf_with_registration(location_name: str, dock_forward: bool = False) -> str:
        """任意の棚にドッキングして登録
        
        Args:
            location_name: ドッキングする場所の名前またはID
            dock_forward: 前方からドッキングするかどうか
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Docking any shelf at location {location_name}, dock_forward={dock_forward}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 進捗報告の設定
            ctx.info(f"Docking any shelf at location {location_name}, dock_forward={dock_forward}")
            
            # ドッキングコマンドの実行
            result = await kachaka_client.dock_any_shelf_with_registration(
                location_name,
                dock_forward,
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return f"Successfully docked shelf at location {location_name}"
            else:
                return f"Failed to dock shelf: {result.message}"
        except Exception as e:
            logger.error(f"Error docking shelf: {e}")
            return f"Error: {str(e)}"


def register_system_tools(mcp: FastMCP) -> None:
    """システム操作ツールの登録
    
    Args:
        mcp: MCPサーバーインスタンス
    """
    @mcp.tool()
    async def speak(text: str) -> str:
        """テキストを音声で発話
        
        Args:
            text: 発話するテキスト
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Speaking: {text}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 発話コマンドの実行
            result = await kachaka_client.speak(
                text,
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return f"Successfully spoke: {text}"
            else:
                return f"Failed to speak: {result.message}"
        except Exception as e:
            logger.error(f"Error speaking: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def cancel_command() -> str:
        """実行中のコマンドをキャンセル
        
        Returns:
            実行結果のメッセージ
        """
        logger.info("Canceling command")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # コマンドのキャンセル
            result, command = await kachaka_client.cancel_command()
            
            # 結果の返却
            if result.success:
                return "Successfully canceled command"
            else:
                return f"Failed to cancel command: {result.message}"
        except Exception as e:
            logger.error(f"Error canceling command: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def proceed() -> str:
        """次のステップに進む
        
        Returns:
            実行結果のメッセージ
        """
        logger.info("Proceeding to next step")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 次のステップに進む
            result = await kachaka_client.proceed()
            
            # 結果の返却
            if result.success:
                return "Successfully proceeded to next step"
            else:
                return f"Failed to proceed: {result.message}"
        except Exception as e:
            logger.error(f"Error proceeding: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def lock(duration_sec: float) -> str:
        """指定した時間ロックする
        
        Args:
            duration_sec: ロックする時間（秒）
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Locking for {duration_sec} seconds")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # ロックコマンドの実行
            result = await kachaka_client.lock(
                duration_sec,
                wait_for_completion=True
            )
            
            # 結果の返却
            if result.success:
                return f"Successfully locked for {duration_sec} seconds"
            else:
                return f"Failed to lock: {result.message}"
        except Exception as e:
            logger.error(f"Error locking: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def set_auto_homing_enabled(enable: bool) -> str:
        """自動ホーミングの有効/無効を設定
        
        Args:
            enable: 有効にするかどうか
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Setting auto homing enabled: {enable}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 自動ホーミングの設定
            result = await kachaka_client.set_auto_homing_enabled(enable)
            
            # 結果の返却
            if result.success:
                return f"Successfully set auto homing enabled: {enable}"
            else:
                return f"Failed to set auto homing: {result.message}"
        except Exception as e:
            logger.error(f"Error setting auto homing: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def set_manual_control_enabled(enable: bool) -> str:
        """手動制御の有効/無効を設定
        
        Args:
            enable: 有効にするかどうか
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Setting manual control enabled: {enable}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 手動制御の設定
            result = await kachaka_client.set_manual_control_enabled(enable)
            
            # 結果の返却
            if result.success:
                return f"Successfully set manual control enabled: {enable}"
            else:
                return f"Failed to set manual control: {result.message}"
        except Exception as e:
            logger.error(f"Error setting manual control: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def set_speaker_volume(volume: int) -> str:
        """スピーカーの音量を設定
        
        Args:
            volume: 音量（0-100）
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Setting speaker volume: {volume}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 音量の設定
            result = await kachaka_client.set_speaker_volume(volume)
            
            # 結果の返却
            if result.success:
                return f"Successfully set speaker volume: {volume}"
            else:
                return f"Failed to set speaker volume: {result.message}"
        except Exception as e:
            logger.error(f"Error setting speaker volume: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def restart_robot() -> str:
        """ロボットを再起動
        
        Returns:
            実行結果のメッセージ
        """
        logger.info("Restarting robot")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # 再起動コマンドの実行
            result = await kachaka_client.restart_robot()
            
            # 結果の返却
            if result.success:
                return "Successfully restarted robot"
            else:
                return f"Failed to restart robot: {result.message}"
        except Exception as e:
            logger.error(f"Error restarting robot: {e}")
            return f"Error: {str(e)}"


def register_map_tools(mcp: FastMCP) -> None:
    """マップ操作ツールの登録
    
    Args:
        mcp: MCPサーバーインスタンス
    """
    @mcp.tool()
    async def switch_map(map_id: str) -> str:
        """マップを切り替える
        
        Args:
            map_id: 切り替えるマップのID
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Switching to map: {map_id}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # マップの切り替え
            result = await kachaka_client.switch_map(map_id)
            
            # 結果の返却
            if result.success:
                return f"Successfully switched to map: {map_id}"
            else:
                return f"Failed to switch map: {result.message}"
        except Exception as e:
            logger.error(f"Error switching map: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def export_map(map_id: str, output_file_path: str) -> str:
        """マップをエクスポート
        
        Args:
            map_id: エクスポートするマップのID
            output_file_path: 出力ファイルパス
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Exporting map {map_id} to {output_file_path}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # マップのエクスポート
            result = await kachaka_client.export_map(map_id, output_file_path)
            
            # 結果の返却
            if result.success:
                return f"Successfully exported map {map_id} to {output_file_path}"
            else:
                return f"Failed to export map: {result.message}"
        except Exception as e:
            logger.error(f"Error exporting map: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def import_map(target_file_path: str) -> str:
        """マップをインポート
        
        Args:
            target_file_path: インポートするファイルパス
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Importing map from {target_file_path}")
        from kachaka_mcp.server import current_context
        kachaka_client = current_context.kachaka_client
        
        try:
            # マップのインポート
            result = await kachaka_client.import_map(target_file_path)
            
            # 結果の返却
            if result.success:
                return f"Successfully imported map from {target_file_path}"
            else:
                return f"Failed to import map: {result.message}"
        except Exception as e:
            logger.error(f"Error importing map: {e}")
            return f"Error: {str(e)}"
    
    @mcp.tool()
    async def set_robot_pose(x: float, y: float, yaw: float, ctx: Context) -> str:
        """ロボットの位置を設定
        
        Args:
            x: X座標
            y: Y座標
            yaw: 向き（ラジアン）
            ctx: MCPコンテキスト
            
        Returns:
            実行結果のメッセージ
        """
        logger.info(f"Setting robot pose: x={x}, y={y}, yaw={yaw}")
        kachaka_client = ctx.request_context.lifespan_context.kachaka_client
        
        try:
            # ロボットの位置を設定
            pose = {"x": x, "y": y, "yaw": yaw}
            result = await kachaka_client.set_robot_pose(pose)
            
            # 結果の返却
            if result.success:
                return f"Successfully set robot pose: x={x}, y={y}, yaw={yaw}"
            else:
                return f"Failed to set robot pose: {result.message}"
        except Exception as e:
            logger.error(f"Error setting robot pose: {e}")
            return f"Error: {str(e)}"