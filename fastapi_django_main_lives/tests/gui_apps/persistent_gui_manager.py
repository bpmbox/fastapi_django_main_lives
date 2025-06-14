#!/usr/bin/env python3
"""
Persistent AI GUI Container Manager
Manages Docker-based persistent GUI environment for AI Copilot
"""

import subprocess
import time
import json
import requests
import logging
from pathlib import Path
from typing import Dict, Optional, Any
import sqlite3
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PersistentGUIManager:
    """Manages the persistent Docker GUI environment for AI operations"""
    
    def __init__(self):
        self.container_name = "copilot-ai-desktop"
        self.compose_file = Path(__file__).parent / "docker-gui-setup" / "docker-compose.gui.yml"
        self.gui_port = 6080
        self.vnc_port = 5901
        self.memory_db = "/ai-memory/gui_operations.db"
        
    def initialize_volumes(self) -> bool:
        """Create Docker volumes if they don't exist"""
        volumes = [
            "copilot-ai-memory",
            "copilot-gui-data", 
            "copilot-browser-data"
        ]
        
        for volume in volumes:
            try:
                result = subprocess.run([
                    "docker", "volume", "create", volume
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"✅ Volume {volume} ready")
                else:
                    logger.info(f"📁 Volume {volume} already exists")
                    
            except Exception as e:
                logger.error(f"❌ Failed to create volume {volume}: {e}")
                return False
                
        return True
    
    def start_gui_container(self) -> bool:
        """Start the persistent GUI container"""
        try:
            logger.info("🚀 Starting persistent AI GUI environment...")
            
            # Initialize volumes first
            if not self.initialize_volumes():
                logger.error("❌ Failed to initialize volumes")
                return False
            
            # Start container using docker-compose
            result = subprocess.run([
                "docker-compose", 
                "-f", str(self.compose_file),
                "up", "-d"
            ], capture_output=True, text=True, cwd="/workspaces/fastapi_django_main_live")
            
            if result.returncode != 0:
                logger.error(f"❌ Failed to start GUI container: {result.stderr}")
                return False
            
            logger.info("🚀 GUI container started successfully")
            
            # Wait for services to be ready
            return self.wait_for_services()
            
        except Exception as e:
            logger.error(f"❌ Error starting GUI container: {e}")
            return False
    
    def wait_for_services(self, timeout: int = 60) -> bool:
        """Wait for GUI services to be ready"""
        logger.info("⏳ Waiting for GUI services to be ready...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Check if noVNC web interface is accessible
                response = requests.get(f"http://localhost:{self.gui_port}", timeout=5)
                if response.status_code == 200:
                    logger.info("✅ noVNC web interface is ready")
                    
                    # Log successful startup
                    self.log_gui_operation("gui_startup", {
                        "status": "success",
                        "port": self.gui_port,
                        "vnc_port": self.vnc_port,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    return True
                    
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(2)
            
        logger.error("❌ GUI services failed to start within timeout")
        return False
    
    def stop_gui_container(self) -> bool:
        """Stop the GUI container"""
        try:
            logger.info("🛑 Stopping GUI container...")
            
            result = subprocess.run([
                "docker-compose",
                "-f", str(self.compose_file),
                "down"
            ], capture_output=True, text=True, cwd="/workspaces/fastapi_django_main_live")
            
            if result.returncode == 0:
                logger.info("✅ GUI container stopped")
                return True
            else:
                logger.error(f"❌ Failed to stop GUI container: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error stopping GUI container: {e}")
            return False
    
    def restart_gui_container(self) -> bool:
        """Restart the GUI container"""
        logger.info("🔄 Restarting GUI container...")
        return self.stop_gui_container() and self.start_gui_container()
    
    def get_container_status(self) -> Dict[str, Any]:
        """Get current status of GUI container"""
        try:
            result = subprocess.run([
                "docker", "ps", "--filter", f"name={self.container_name}",
                "--format", "json"
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                container_info = json.loads(result.stdout.strip())
                return {
                    "status": "running",
                    "container_id": container_info.get("ID", ""),
                    "image": container_info.get("Image", ""),
                    "ports": container_info.get("Ports", ""),
                    "created": container_info.get("CreatedAt", "")
                }
            else:
                return {"status": "stopped"}
                
        except Exception as e:
            logger.error(f"❌ Error getting container status: {e}")
            return {"status": "error", "error": str(e)}
    
    def execute_in_container(self, command: str) -> Optional[str]:
        """Execute command in the GUI container"""
        try:
            result = subprocess.run([
                "docker", "exec", "-it", self.container_name,
                "bash", "-c", command
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout
            else:
                logger.error(f"❌ Command failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error executing command: {e}")
            return None
    
    def install_gui_software(self) -> bool:
        """Install additional software in the GUI environment"""
        software_packages = [
            "firefox",
            "chromium-browser", 
            "gimp",
            "libreoffice",
            "gedit",
            "python3-pip",
            "python3-tk",
            "scrot",  # Screenshot tool
            "xdotool"  # GUI automation tool
        ]
        
        logger.info("📦 Installing GUI software packages...")
        
        # Update package list
        if not self.execute_in_container("apt-get update"):
            return False
        
        # Install packages
        for package in software_packages:
            logger.info(f"📦 Installing {package}...")
            result = self.execute_in_container(f"apt-get install -y {package}")
            if result is None:
                logger.warning(f"⚠️ Failed to install {package}")
        
        # Install Python packages for AI automation
        python_packages = [
            "selenium",
            "beautifulsoup4", 
            "pillow",
            "opencv-python-headless",
            "pyautogui",
            "pynput"
        ]
        
        for package in python_packages:
            logger.info(f"🐍 Installing Python package: {package}")
            self.execute_in_container(f"pip3 install {package}")
        
        logger.info("✅ GUI software installation complete")
        return True
    
    def log_gui_operation(self, operation: str, data: Dict[str, Any]):
        """Log GUI operations to memory database"""
        try:
            # Ensure memory directory exists
            Path("/ai-memory").mkdir(exist_ok=True)
            
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gui_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    operation TEXT,
                    data TEXT
                )
            """)
            
            # Insert operation log
            cursor.execute(
                "INSERT INTO gui_operations (timestamp, operation, data) VALUES (?, ?, ?)",
                (datetime.now().isoformat(), operation, json.dumps(data))
            )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Failed to log GUI operation: {e}")
    
    def get_gui_url(self) -> str:
        """Get the noVNC GUI URL"""
        return f"http://localhost:{self.gui_port}"
    
    def get_vnc_connection_info(self) -> Dict[str, Any]:
        """Get VNC connection information"""
        return {
            "web_interface": f"http://localhost:{self.gui_port}",
            "vnc_server": f"localhost:{self.vnc_port}",
            "password": "copilot",
            "resolution": "1920x1080"
        }

def main():
    """Main function for CLI usage"""
    import sys
    
    gui_manager = PersistentGUIManager()
    
    if len(sys.argv) < 2:
        print("Usage: python3 persistent_gui_manager.py [start|stop|restart|status|install|info]")
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        success = gui_manager.start_gui_container()
        if success:
            print("🚀 Persistent AI GUI environment started!")
            print(f"🌐 Access GUI at: {gui_manager.get_gui_url()}")
            print("🔐 Password: copilot")
        else:
            print("❌ Failed to start GUI environment")
            
    elif command == "stop":
        success = gui_manager.stop_gui_container()
        if success:
            print("🛑 GUI environment stopped")
        else:
            print("❌ Failed to stop GUI environment")
            
    elif command == "restart":
        success = gui_manager.restart_gui_container()
        if success:
            print("🔄 GUI environment restarted")
        else:
            print("❌ Failed to restart GUI environment")
            
    elif command == "status":
        status = gui_manager.get_container_status()
        print(f"📊 Container Status: {json.dumps(status, indent=2)}")
        
    elif command == "install":
        if gui_manager.get_container_status()["status"] == "running":
            gui_manager.install_gui_software()
        else:
            print("❌ Container must be running to install software")
            
    elif command == "info":
        info = gui_manager.get_vnc_connection_info()
        print(f"🔗 Connection Info: {json.dumps(info, indent=2)}")
        
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
