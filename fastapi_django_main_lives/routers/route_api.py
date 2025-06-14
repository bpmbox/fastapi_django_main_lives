#!/usr/bin/env python3
"""
Route API - ルート一覧とテスト機能のAPIエンドポイント
CI/CDパイプライン用のAPI
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
import os
import sys
import re
import importlib
from pathlib import Path

router = APIRouter()

class RouteScanner:
    """ルートスキャナー - artisan.pyのロジックを再利用"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
    
    def scan_all_routes(self) -> Dict[str, Any]:
        """全ルートをスキャン"""
        return {
            "fastapi_routes": self._scan_fastapi_routes(),
            "gradio_interfaces": self._scan_gradio_interfaces(),
            "django_urls": self._scan_django_urls(),
            "summary": self._get_summary()
        }
    
    def scan_active_routes(self) -> Dict[str, Any]:
        """アクティブなルートのみスキャン"""
        return {
            "fastapi_routes": self._scan_active_fastapi_routes(),
            "gradio_interfaces": self._scan_active_gradio_interfaces(),
            "django_urls": self._scan_active_django_urls(),
            "summary": self._get_active_summary()
        }
    
    def _scan_fastapi_routes(self) -> List[Dict[str, str]]:
        """FastAPIルートをスキャン"""
        routes = []
        
        # メインファイル
        main_files = ["mysite/asgi.py", "app.py", "main.py"]
        for main_file in main_files:
            main_path = self.project_root / main_file
            if main_path.exists():
                routes.extend(self._extract_routes_from_file(main_path, main_file))
        
        # routersディレクトリ
        routers_dir = self.project_root / "routers"
        if routers_dir.exists():
            for py_file in routers_dir.glob("**/*.py"):
                if py_file.name != "__init__.py":
                    relative_path = str(py_file.relative_to(self.project_root))
                    routes.extend(self._extract_routes_from_file(py_file, relative_path))
        
        return routes
    
    def _scan_active_fastapi_routes(self) -> List[Dict[str, str]]:
        """アクティブなFastAPIルートのみスキャン"""
        routes = []
        
        # メインファイル
        main_files = ["mysite/asgi.py", "app.py", "main.py"]
        for main_file in main_files:
            main_path = self.project_root / main_file
            if main_path.exists():
                routes.extend(self._extract_routes_from_file(main_path, main_file))
        
        # アクティブなroutersのみ
        routers_dir = self.project_root / "routers"
        if routers_dir.exists():
            # 直接のPythonファイル
            for py_file in routers_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    relative_path = str(py_file.relative_to(self.project_root))
                    routes.extend(self._extract_routes_from_file(py_file, relative_path))
            
            # gra_*サブディレクトリ
            for subdir in routers_dir.iterdir():
                if subdir.is_dir() and subdir.name.startswith('gra_'):
                    for py_file in subdir.glob("*.py"):
                        if py_file.name != "__init__.py":
                            relative_path = str(py_file.relative_to(self.project_root))
                            routes.extend(self._extract_gradio_functions_as_routes(py_file, relative_path))
        
        return routes
    
    def _scan_gradio_interfaces(self) -> List[Dict[str, Any]]:
        """Gradioインターフェースをスキャン"""
        interfaces = []
        controllers_dir = self.project_root / "controllers"
        
        if controllers_dir.exists():
            for subdir in controllers_dir.iterdir():
                if subdir.is_dir() and subdir.name.startswith('gra_'):
                    py_files = [f for f in subdir.glob("*.py") if f.name != "__init__.py"]
                    for py_file in py_files:
                        interface_info = self._analyze_gradio_interface(py_file, subdir.name)
                        if interface_info:
                            interfaces.append(interface_info)
        
        return interfaces
    
    def _scan_active_gradio_interfaces(self) -> List[Dict[str, Any]]:
        """アクティブなGradioインターフェースのみスキャン"""
        return self._scan_gradio_interfaces()  # すべてアクティブ
    
    def _scan_django_urls(self) -> List[Dict[str, str]]:
        """DjangoURLをスキャン"""
        urls = []
        
        # 全体をスキャン
        for urls_file in self.project_root.rglob("urls.py"):
            if "workspace" not in str(urls_file):  # workspaceは除外
                relative_path = str(urls_file.relative_to(self.project_root))
                urls.extend(self._extract_django_patterns(urls_file, relative_path))
        
        return urls
    
    def _scan_active_django_urls(self) -> List[Dict[str, str]]:
        """アクティブなDjangoURLのみスキャン"""
        urls = []
        
        # アクティブなファイルのみ
        active_files = ["mysite/urls.py", "polls/urls.py"]
        for django_file in active_files:
            urls_path = self.project_root / django_file
            if urls_path.exists():
                urls.extend(self._extract_django_patterns(urls_path, django_file))
        
        return urls
    
    def _extract_routes_from_file(self, file_path: Path, source: str) -> List[Dict[str, str]]:
        """ファイルからルートを抽出"""
        routes = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # FastAPI デコレータルート
            route_patterns = [
                r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
                r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']'
            ]
            
            for pattern in route_patterns:
                matches = re.findall(pattern, content)
                for method, path in matches:
                    routes.append({
                        "method": method.upper(),
                        "path": path,
                        "source": source,
                        "type": "fastapi"
                    })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return routes
    
    def _extract_gradio_functions_as_routes(self, file_path: Path, source: str) -> List[Dict[str, str]]:
        """Gradioファイルから関数をルートとして抽出"""
        routes = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 関数定義を検索
            function_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            functions = re.findall(function_pattern, content)
            
            # __で始まる内部関数を除外
            user_functions = [f for f in functions if not f.startswith('_')]
            
            for func in user_functions:
                routes.append({
                    "method": "GRADIO",
                    "path": f"/gradio/{source.replace('/', '_')}#{func}",
                    "source": source,
                    "type": "gradio_function",
                    "function": func
                })
        except Exception as e:
            print(f"Error reading gradio file: {e}")
        
        return routes
    
    def _analyze_gradio_interface(self, file_path: Path, category: str) -> Dict[str, Any]:
        """Gradioインターフェースを解析"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Gradioタイプを検出
            gradio_types = re.findall(r'gr\.(Interface|Blocks|TabbedInterface|ChatInterface)', content)
            
            # 関数定義を検出
            functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', content)
            user_functions = [f for f in functions if not f.startswith('_')]
            
            return {
                "category": category,
                "file": file_path.name,
                "path": str(file_path.relative_to(self.project_root)),
                "gradio_types": list(set(gradio_types)),
                "functions": user_functions,
                "type": "gradio_interface"
            }
        except Exception as e:
            print(f"Error analyzing gradio interface: {e}")
            return None
    
    def _extract_django_patterns(self, file_path: Path, source: str) -> List[Dict[str, str]]:
        """DjangoのURLパターンを抽出"""
        patterns = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Django URL パターンを検索
            url_patterns = [
                r'path\(["\']([^"\']*)["\']',
                r'url\(["\']([^"\']*)["\']'
            ]
            
            for pattern in url_patterns:
                matches = re.findall(pattern, content)
                for url in matches:
                    patterns.append({
                        "method": "PATH",
                        "path": url or "/",
                        "source": source,
                        "type": "django"
                    })
        except Exception as e:
            print(f"Error reading Django URLs: {e}")
        
        return patterns
    
    def _get_summary(self) -> Dict[str, int]:
        """ルートの統計情報"""
        fastapi = len(self._scan_fastapi_routes())
        gradio = len(self._scan_gradio_interfaces())
        django = len(self._scan_django_urls())
        
        return {
            "total_routes": fastapi + gradio + django,
            "fastapi_routes": fastapi,
            "gradio_interfaces": gradio,
            "django_urls": django
        }
    
    def _get_active_summary(self) -> Dict[str, int]:
        """アクティブルートの統計情報"""
        fastapi = len(self._scan_active_fastapi_routes())
        gradio = len(self._scan_active_gradio_interfaces())
        django = len(self._scan_active_django_urls())
        
        return {
            "total_active_routes": fastapi + gradio + django,
            "active_fastapi_routes": fastapi,
            "active_gradio_interfaces": gradio,
            "active_django_urls": django
        }

# ルートスキャナーのインスタンス
scanner = RouteScanner()

@router.get("/routes/all")
async def get_all_routes():
    """全ルート一覧を取得"""
    try:
        return scanner.scan_all_routes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Route scanning failed: {str(e)}")

@router.get("/routes/active")
async def get_active_routes():
    """アクティブなルートのみ取得"""
    try:
        return scanner.scan_active_routes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Active route scanning failed: {str(e)}")

@router.get("/routes/summary")
async def get_routes_summary():
    """ルートのサマリー情報を取得"""
    try:
        return {
            "all_routes_summary": scanner._get_summary(),
            "active_routes_summary": scanner._get_active_summary()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")

@router.get("/routes/test")
async def test_routes():
    """ルートの基本テスト"""
    try:
        active_routes = scanner.scan_active_routes()
        
        # 基本的なテスト
        test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": []
        }
        
        # FastAPIルートテスト
        for route in active_routes["fastapi_routes"]:
            test_results["total_tests"] += 1
            test_detail = {
                "type": "fastapi",
                "method": route["method"],
                "path": route["path"],
                "source": route["source"],
                "status": "passed",  # 基本的にはルートが存在すればOK
                "message": "Route definition found"
            }
            test_results["test_details"].append(test_detail)
            test_results["passed_tests"] += 1
        
        # Gradioインターフェーステスト
        for interface in active_routes["gradio_interfaces"]:
            test_results["total_tests"] += 1
            test_detail = {
                "type": "gradio",
                "category": interface["category"],
                "file": interface["file"],
                "functions": len(interface["functions"]),
                "status": "passed" if interface["functions"] else "warning",
                "message": f"Found {len(interface['functions'])} functions" if interface["functions"] else "No functions found"
            }
            test_results["test_details"].append(test_detail)
            if interface["functions"]:
                test_results["passed_tests"] += 1
            else:
                test_results["failed_tests"] += 1
        
        # Djangoルートテスト
        for url in active_routes["django_urls"]:
            test_results["total_tests"] += 1
            test_detail = {
                "type": "django",
                "method": url["method"],
                "path": url["path"],
                "source": url["source"],
                "status": "passed",
                "message": "Django URL pattern found"
            }
            test_results["test_details"].append(test_detail)
            test_results["passed_tests"] += 1
        
        return test_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Route testing failed: {str(e)}")

@router.get("/health")
async def route_api_health():
    """Route API ヘルスチェック"""
    return {
        "status": "healthy",
        "service": "route_api",
        "scanner": "ready"
    }
