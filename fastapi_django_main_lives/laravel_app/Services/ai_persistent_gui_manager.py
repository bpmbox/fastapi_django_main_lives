#!/usr/bin/env python3
"""
AI Persistent GUI Manager
永続化されたDocker GUI環境の管理システム
30年来の夢の実現 - 人とAIが共に創造する基盤
"""
import os
import subprocess
import time
import json
import docker
import requests
from pathlib import Path
from typing import Dict, Optional, List
import logging

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIPersistentGUIManager:
    """永続化されたAI GUI環境の管理クラス"""
    
    def __init__(self):
        self.container_name = "ai-gui-desktop-persistent"
        self.compose_file = "docker-compose-persistent-gui.yml"
        self.workspace_path = "/workspaces/fastapi_django_main_live"
        self.docker_client = docker.from_env()
        self.gui_url = "http://localhost:6081"
        self.vnc_port = 5902
        
    def check_docker_compose(self) -> bool:
        """Docker Composeが利用可能かチェック"""
        try:
            result = subprocess.run(['docker-compose', '--version'], 
                                  capture_output=True, text=True)
            logger.info(f"Docker Compose available: {result.stdout.strip()}")
            return True
        except FileNotFoundError:
            logger.error("Docker Compose not found")
            return False
    
    def start_persistent_gui(self) -> bool:
        """永続化GUI環境を起動"""
        try:
            logger.info("🚀 Starting AI Persistent GUI Desktop...")
            
            # コンテナが既に動いているかチェック
            if self.is_container_running():
                logger.info("✅ AI GUI Desktop is already running")
                return True
            
            # Docker Composeで起動
            compose_cmd = [
                'docker-compose', 
                '-f', self.compose_file,
                'up', '-d'
            ]
            
            result = subprocess.run(compose_cmd, cwd=self.workspace_path, 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ AI Persistent GUI Desktop started successfully")
                # 起動待機
                self.wait_for_gui_ready()
                return True
            else:
                logger.error(f"❌ Failed to start GUI: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error starting GUI: {e}")
            return False
    
    def is_container_running(self) -> bool:
        """コンテナが動いているかチェック"""
        try:
            container = self.docker_client.containers.get(self.container_name)
            return container.status == 'running'
        except docker.errors.NotFound:
            return False
        except Exception as e:
            logger.error(f"Error checking container: {e}")
            return False
    
    def wait_for_gui_ready(self, timeout: int = 60) -> bool:
        """GUIが準備完了するまで待機"""
        logger.info("⏳ Waiting for GUI to be ready...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(self.gui_url, timeout=5)
                if response.status_code == 200:
                    logger.info("✅ GUI is ready!")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(5)
            logger.info("⏳ Still waiting for GUI...")
        
        logger.warning("⚠️ GUI startup timeout")
        return False
    
    def stop_gui(self) -> bool:
        """GUI環境を停止"""
        try:
            logger.info("🛑 Stopping AI Persistent GUI Desktop...")
            
            compose_cmd = [
                'docker-compose', 
                '-f', self.compose_file,
                'down'
            ]
            
            result = subprocess.run(compose_cmd, cwd=self.workspace_path, 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ AI GUI Desktop stopped successfully")
                return True
            else:
                logger.error(f"❌ Failed to stop GUI: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error stopping GUI: {e}")
            return False
    
    def restart_gui(self) -> bool:
        """GUI環境を再起動"""
        logger.info("🔄 Restarting AI Persistent GUI Desktop...")
        if self.stop_gui():
            time.sleep(5)
            return self.start_gui()
        return False
    
    def get_status(self) -> Dict:
        """GUI環境の状態を取得"""
        status = {
            'container_running': self.is_container_running(),
            'gui_accessible': False,
            'vnc_port': self.vnc_port,
            'gui_url': self.gui_url,
            'volumes_info': self.get_volumes_info()
        }
        
        # GUI アクセス可能性チェック
        try:
            response = requests.get(self.gui_url, timeout=5)
            status['gui_accessible'] = response.status_code == 200
        except:
            pass
        
        return status
    
    def get_volumes_info(self) -> Dict:
        """永続化ボリュームの情報を取得"""
        volumes_info = {}
        volume_names = [
            'copilot-ai-memory',
            'copilot-gui-data', 
            'copilot-browser-data',
            'copilot-desktop-config'
        ]
        
        for volume_name in volume_names:
            try:
                volume = self.docker_client.volumes.get(volume_name)
                volumes_info[volume_name] = {
                    'exists': True,
                    'mountpoint': volume.attrs.get('Mountpoint', ''),
                    'created': volume.attrs.get('CreatedAt', '')
                }
            except docker.errors.NotFound:
                volumes_info[volume_name] = {'exists': False}
            except Exception as e:
                volumes_info[volume_name] = {'error': str(e)}
        
        return volumes_info
    
    def execute_in_container(self, command: str) -> Optional[str]:
        """コンテナ内でコマンドを実行"""
        try:
            container = self.docker_client.containers.get(self.container_name)
            if container.status != 'running':
                logger.error("Container is not running")
                return None
            
            result = container.exec_run(command, user='aiuser')
            return result.output.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error executing command in container: {e}")
            return None
    
    def install_browser_in_container(self) -> bool:
        """コンテナ内にブラウザをインストール"""
        logger.info("🌐 Installing browsers in GUI container...")
        
        commands = [
            "apt-get update",
            "apt-get install -y firefox chromium-browser",
            "apt-get install -y python3 python3-pip",
            "pip3 install playwright selenium",
            "playwright install"
        ]
        
        for cmd in commands:
            result = self.execute_in_container(f"sudo {cmd}")
            if result is None:
                logger.error(f"Failed to execute: {cmd}")
                return False
            logger.info(f"✅ Executed: {cmd}")
        
        return True
    
    def create_ai_memory_structure(self) -> bool:
        """AI Memory構造をコンテナ内に作成"""
        logger.info("🧠 Creating AI Memory structure in container...")
        
        directories = [
            "/ai-memory/screenshots",
            "/ai-memory/operations", 
            "/ai-memory/browser_data",
            "/ai-memory/logs",
            "/ai-memory/temp"
        ]
        
        for directory in directories:
            result = self.execute_in_container(f"mkdir -p {directory}")
            if result is None:
                logger.error(f"Failed to create directory: {directory}")
                return False
        
        # 権限設定
        self.execute_in_container("chown -R aiuser:aiuser /ai-memory")
        self.execute_in_container("chmod -R 755 /ai-memory")
        
        logger.info("✅ AI Memory structure created")
        return True


def main():
    """メイン関数"""
    print("🚀 AI Persistent GUI Manager - 30年来の夢の実現")
    print("=" * 50)
    
    manager = AIPersistentGUIManager()
    
    # Docker Composeチェック
    if not manager.check_docker_compose():
        print("❌ Docker Compose is required")
        return
    
    # GUI環境起動
    if manager.start_persistent_gui():
        print("\n✅ AI Persistent GUI Desktop is ready!")
        print(f"🌐 Access GUI at: {manager.gui_url}")
        print(f"🖥️ VNC Direct Access: localhost:{manager.vnc_port}")
        print("🔐 Password: copilot")
        
        # ブラウザとAI Memory構造のセットアップ
        time.sleep(10)  # コンテナが完全に起動するまで待機
        manager.install_browser_in_container()
        manager.create_ai_memory_structure()
        
        # 状態表示
        status = manager.get_status()
        print(f"\n📊 System Status:")
        print(f"  • Container Running: {'✅' if status['container_running'] else '❌'}")
        print(f"  • GUI Accessible: {'✅' if status['gui_accessible'] else '❌'}")
        print(f"  • Volumes: {len([v for v in status['volumes_info'].values() if v.get('exists', False)])}/4 ready")
        
    else:
        print("❌ Failed to start AI GUI Desktop")


if __name__ == "__main__":
    main()
