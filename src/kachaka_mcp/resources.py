"""
Resources for Kachaka MCP Server.

This module defines the resources that are exposed by the Kachaka MCP Server.
"""

import json
from typing import Dict, Any, List

from mcp.server.fastmcp import FastMCP, Context, Image
from PIL import Image as PILImage
import io

from loguru import logger


def register_resources(mcp: FastMCP) -> None:
    """リソースの登録
    
    Args:
        mcp: MCPサーバーインスタンス
    """
    # ロボット情報リソース
    register_robot_resources(mcp)
    
    # マップリソース
    register_map_resources(mcp)
    
    # センサーリソース
    register_sensor_resources(mcp)


def register_robot_resources(mcp: FastMCP) -> None:
    """ロボット情報リソースの登録
    
    Args:
        mcp: MCPサーバーインスタンス
    """
    @mcp.resource("robot://status")
    async def get_robot_status() -> str:
        """ロボットの現在の状態を取得"""
        logger.debug("Getting robot status")
        # コンテキストを取得する方法が変わった可能性があるため、
        # 現在のMCP SDKのバージョンに合わせて修正
        try:
            from mcp.server.fastmcp import get_context
            ctx = get_context()
        except ImportError:
            # 古いバージョンのSDKを使用している場合は、ctxを直接取得
            ctx = mcp.get_context()
            
        """ロボットの現在の状態を取得"""
        logger.debug("Getting robot status")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # 各種情報の取得 
            pose = await kachaka_client.get_robot_pose()
            battery_info = await kachaka_client.get_battery_info()
            command_state, command = await kachaka_client.get_command_state()
            
            # JSONとして返す
            status = {
                "pose": {
                    "x": pose.x,
                    "y": pose.y,
                    "yaw": pose.yaw
                },
                "battery": {
                    "percentage": battery_info[0],
                    "status": str(battery_info[1])
                },
                "command_state": str(command_state),
                "command": {
                    "type": command.WhichOneof("command") if command else None,
                    "id": command_state.command_id if command_state.command_id else ""
                }
            }
            
            return json.dumps(status, indent=2)
        except Exception as e:
            logger.error(f"Error getting robot status: {e}")
            return json.dumps({"error": str(e)})
    
    @mcp.resource("robot://version")
    async def get_robot_version() -> str:
        """ロボットのバージョン情報を取得"""
        logger.debug("Getting robot version")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            version = await kachaka_client.get_robot_version()
            return version
        except Exception as e:
            logger.error(f"Error getting robot version: {e}")
            return json.dumps({"error": str(e)})
    
    @mcp.resource("robot://serial")
    async def get_robot_serial() -> str:
        """ロボットのシリアル番号を取得"""
        logger.debug("Getting robot serial number")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            serial = await kachaka_client.get_robot_serial_number()
            return serial
        except Exception as e:
            logger.error(f"Error getting robot serial number: {e}")
            return json.dumps({"error": str(e)})
    
    @mcp.resource("robot://command")
    async def get_robot_command() -> str:
        """現在実行中のコマンド情報を取得"""
        logger.debug("Getting robot command")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            command_state, command = await kachaka_client.get_command_state()
            
            command_info = {
                "state": str(command_state),
                "command": {
                    "type": command.WhichOneof("command") if command else None,
                    "id": command_state.command_id if command_state.command_id else ""
                }
            }
            
            return json.dumps(command_info, indent=2)
        except Exception as e:
            logger.error(f"Error getting robot command: {e}")
            return json.dumps({"error": str(e)})


def register_map_resources(mcp: FastMCP) -> None:
    """マップリソースの登録
    
    Args:
        mcp: MCPサーバーインスタンス
    """
    @mcp.resource("map://current")
    async def get_current_map() -> Image:
        """現在のマップ画像を取得"""
        logger.debug("Getting current map")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # マップの取得
            map_data = await kachaka_client.get_png_map()
            
            # 画像として返す
            return Image(data=map_data.data, format="png")
        except Exception as e:
            logger.error(f"Error getting current map: {e}")
            # エラー画像を返す
            error_img = PILImage.new('RGB', (400, 100), color=(255, 0, 0))
            img_bytes = io.BytesIO()
            error_img.save(img_bytes, format='PNG')
            return Image(data=img_bytes.getvalue(), format="png")
    
    @mcp.resource("map://locations/{location_id}")
    async def get_locations(location_id: str = None) -> str:
        """登録された場所の情報を取得"""
        logger.debug(f"Getting locations, location_id={location_id}")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # 場所の取得
            locations = await kachaka_client.get_locations()
            
            # 特定の場所が指定されている場合
            if location_id:
                for location in locations:
                    if location.id == location_id or location.name == location_id:
                        return json.dumps({
                            "id": location.id,
                            "name": location.name,
                            "pose": {
                                "x": location.pose.x,
                                "y": location.pose.y,
                                "yaw": location.pose.yaw
                            },
                            "type": str(location.type)
                        }, indent=2)
                
                return json.dumps({"error": f"Location {location_id} not found"})
            
            # すべての場所を返す
            result = []
            for location in locations:
                result.append({
                    "id": location.id,
                    "name": location.name,
                    "pose": {
                        "x": location.pose.x,
                        "y": location.pose.y,
                        "yaw": location.pose.yaw
                    },
                    "type": str(location.type)
                })
            
            return json.dumps(result, indent=2)
        except Exception as e:
            logger.error(f"Error getting locations: {e}")
            return json.dumps({"error": str(e)})
    
    @mcp.resource("map://shelves/{shelf_id}")
    async def get_shelves(shelf_id: str = None) -> str:
        """棚の情報と位置を取得"""
        logger.debug(f"Getting shelves, shelf_id={shelf_id}")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # 棚の取得
            shelves = await kachaka_client.get_shelves()
            
            # 特定の棚が指定されている場合
            if shelf_id:
                for shelf in shelves:
                    if shelf.id == shelf_id or shelf.name == shelf_id:
                        return json.dumps({
                            "id": shelf.id,
                            "name": shelf.name,
                            "pose": {
                                "x": shelf.pose.x,
                                "y": shelf.pose.y,
                                "yaw": shelf.pose.yaw
                            },
                            "home_location_id": shelf.home_location_id
                        }, indent=2)
                
                return json.dumps({"error": f"Shelf {shelf_id} not found"})
            
            # すべての棚を返す
            result = []
            for shelf in shelves:
                result.append({
                    "id": shelf.id,
                    "name": shelf.name,
                    "pose": {
                        "x": shelf.pose.x,
                        "y": shelf.pose.y,
                        "yaw": shelf.pose.yaw
                    },
                    "home_location_id": shelf.home_location_id
                })
            
            return json.dumps(result, indent=2)
        except Exception as e:
            logger.error(f"Error getting shelves: {e}")
            return json.dumps({"error": str(e)})
    
    @mcp.resource("map://list")
    async def get_map_list() -> str:
        """利用可能なマップのリストを取得"""
        logger.debug("Getting map list")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # マップリストの取得
            maps = await kachaka_client.get_map_list()
            
            # マップ情報を整形
            result = []
            for map_info in maps:
                result.append({
                    "id": map_info.id,
                    "name": map_info.name,
                    "created_at": map_info.created_at,
                    "is_current": map_info.id == await kachaka_client.get_current_map_id()
                })
            
            return json.dumps(result, indent=2)
        except Exception as e:
            logger.error(f"Error getting map list: {e}")
            return json.dumps({"error": str(e)})


def register_sensor_resources(mcp: FastMCP) -> None:
    """センサーリソースの登録
    
    Args:
        mcp: MCPサーバーインスタンス
    """
    @mcp.resource("sensors://camera/front")
    async def get_front_camera() -> Image:
        """前面カメラ画像を取得"""
        logger.debug("Getting front camera image")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # カメラ画像の取得
            image = await kachaka_client.get_front_camera_ros_compressed_image()
            
            # 画像として返す
            return Image(data=image.data, format="jpeg")
        except Exception as e:
            logger.error(f"Error getting front camera image: {e}")
            # エラー画像を返す
            error_img = PILImage.new('RGB', (400, 100), color=(255, 0, 0))
            img_bytes = io.BytesIO()
            error_img.save(img_bytes, format='PNG')
            return Image(data=img_bytes.getvalue(), format="png")
    
    @mcp.resource("sensors://camera/back")
    async def get_back_camera() -> Image:
        """背面カメラ画像を取得"""
        logger.debug("Getting back camera image")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # カメラ画像の取得
            image = await kachaka_client.get_back_camera_ros_compressed_image()
            
            # 画像として返す
            return Image(data=image.data, format="jpeg")
        except Exception as e:
            logger.error(f"Error getting back camera image: {e}")
            # エラー画像を返す
            error_img = PILImage.new('RGB', (400, 100), color=(255, 0, 0))
            img_bytes = io.BytesIO()
            error_img.save(img_bytes, format='PNG')
            return Image(data=img_bytes.getvalue(), format="png")
    
    @mcp.resource("sensors://camera/tof")
    async def get_tof_camera() -> Image:
        """ToFカメラ画像を取得"""
        logger.debug("Getting ToF camera image")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # カメラ画像の取得
            image = await kachaka_client.get_tof_camera_ros_compressed_image()
            
            # 画像として返す
            return Image(data=image.data, format="jpeg")
        except Exception as e:
            logger.error(f"Error getting ToF camera image: {e}")
            # エラー画像を返す
            error_img = PILImage.new('RGB', (400, 100), color=(255, 0, 0))
            img_bytes = io.BytesIO()
            error_img.save(img_bytes, format='PNG')
            return Image(data=img_bytes.getvalue(), format="png")
    
    @mcp.resource("sensors://laser")
    async def get_laser_scan() -> str:
        """レーザースキャンデータを取得"""
        logger.debug("Getting laser scan data")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # レーザースキャンの取得
            scan = await kachaka_client.get_ros_laser_scan()
            
            # データを整形
            scan_data = {
                "angle_min": scan.angle_min,
                "angle_max": scan.angle_max,
                "angle_increment": scan.angle_increment,
                "time_increment": scan.time_increment,
                "scan_time": scan.scan_time,
                "range_min": scan.range_min,
                "range_max": scan.range_max,
                "ranges": list(scan.ranges),
                "intensities": list(scan.intensities)
            }
            
            return json.dumps(scan_data)
        except Exception as e:
            logger.error(f"Error getting laser scan data: {e}")
            return json.dumps({"error": str(e)})
    
    @mcp.resource("sensors://imu")
    async def get_imu_data() -> str:
        """IMUデータを取得"""
        logger.debug("Getting IMU data")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # IMUデータの取得
            imu = await kachaka_client.get_ros_imu()
            
            # データを整形
            imu_data = {
                "orientation": {
                    "x": imu.orientation.x,
                    "y": imu.orientation.y,
                    "z": imu.orientation.z,
                    "w": imu.orientation.w
                },
                "angular_velocity": {
                    "x": imu.angular_velocity.x,
                    "y": imu.angular_velocity.y,
                    "z": imu.angular_velocity.z
                },
                "linear_acceleration": {
                    "x": imu.linear_acceleration.x,
                    "y": imu.linear_acceleration.y,
                    "z": imu.linear_acceleration.z
                }
            }
            
            return json.dumps(imu_data)
        except Exception as e:
            logger.error(f"Error getting IMU data: {e}")
            return json.dumps({"error": str(e)})
    
    @mcp.resource("sensors://odometry")
    async def get_odometry_data() -> str:
        """オドメトリデータを取得"""
        logger.debug("Getting odometry data")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # オドメトリデータの取得
            odom = await kachaka_client.get_ros_odometry()
            
            # データを整形
            odom_data = {
                "pose": {
                    "position": {
                        "x": odom.pose.pose.position.x,
                        "y": odom.pose.pose.position.y,
                        "z": odom.pose.pose.position.z
                    },
                    "orientation": {
                        "x": odom.pose.pose.orientation.x,
                        "y": odom.pose.pose.orientation.y,
                        "z": odom.pose.pose.orientation.z,
                        "w": odom.pose.pose.orientation.w
                    }
                },
                "twist": {
                    "linear": {
                        "x": odom.twist.twist.linear.x,
                        "y": odom.twist.twist.linear.y,
                        "z": odom.twist.twist.linear.z
                    },
                    "angular": {
                        "x": odom.twist.twist.angular.x,
                        "y": odom.twist.twist.angular.y,
                        "z": odom.twist.twist.angular.z
                    }
                }
            }
            
            return json.dumps(odom_data)
        except Exception as e:
            logger.error(f"Error getting odometry data: {e}")
            return json.dumps({"error": str(e)})
    
    @mcp.resource("sensors://object_detection")
    async def get_object_detection() -> str:
        """物体検出結果を取得"""
        logger.debug("Getting object detection results")
        from kachaka_mcp.server import get_context
        kachaka_client = get_context().kachaka_client 
        
        try:
            # 物体検出結果の取得
            header, objects = await kachaka_client.get_object_detection()
            
            # データを整形
            result = []
            for obj in objects:
                result.append({
                    "id": obj.id,
                    "label": obj.label,
                    "score": obj.score,
                    "bbox": {
                        "x": obj.bbox.x,
                        "y": obj.bbox.y,
                        "width": obj.bbox.width,
                        "height": obj.bbox.height
                    }
                })
            
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error getting object detection results: {e}")
            return json.dumps({"error": str(e)})