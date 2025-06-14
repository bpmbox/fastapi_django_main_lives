#!/usr/bin/env python3
"""
CI/CD Gradio Interface - ルート管理とテスト機能
"""

import gradio as gr
import requests
import json
import sys
import os
from typing import Dict, List, Any
from datetime import datetime
import asyncio
import aiohttp
from urllib.parse import urljoin

# プロジェクトルートをパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')
sys.path.append(project_root)

try:
    from routers.route_api import scanner
    LOCAL_SCANNER = True
except ImportError:
    LOCAL_SCANNER = False

class CICDInterface:
    """CI/CD Gradio インターフェース"""
    
    def __init__(self):
        self.base_url = "http://localhost:7860"  # FastAPI server
        self.scanner = scanner if LOCAL_SCANNER else None
    
    def get_routes_data(self, route_type: str = "active") -> Dict[str, Any]:
        """ルートデータを取得"""
        if self.scanner:
            # ローカルスキャナーを使用
            if route_type == "active":
                return self.scanner.scan_active_routes()
            else:
                return self.scanner.scan_all_routes()
        else:
            # API経由で取得（フォールバック）
            try:
                endpoint = f"/routes/{route_type}"
                response = requests.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"API request failed: {response.status_code}"}
            except Exception as e:
                return {"error": f"API connection failed: {str(e)}"}
    
    def run_tests(self) -> Dict[str, Any]:
        """テストを実行"""
        if self.scanner:
            # ローカルスキャナーでテスト
            try:
                active_routes = self.scanner.scan_active_routes()
                
                test_results = {
                    "timestamp": datetime.now().isoformat(),
                    "total_tests": 0,
                    "passed_tests": 0,
                    "failed_tests": 0,
                    "test_details": []
                }
                
                # FastAPIルートテスト
                for route in active_routes.get("fastapi_routes", []):
                    test_results["total_tests"] += 1
                    test_detail = {
                        "type": "fastapi",
                        "method": route["method"],
                        "path": route["path"],
                        "source": route["source"],
                        "status": "✅ PASS",
                        "message": "Route definition found"
                    }
                    test_results["test_details"].append(test_detail)
                    test_results["passed_tests"] += 1
                
                # Gradioインターフェーステスト
                for interface in active_routes.get("gradio_interfaces", []):
                    test_results["total_tests"] += 1
                    has_functions = len(interface.get("functions", [])) > 0
                    test_detail = {
                        "type": "gradio",
                        "category": interface["category"],
                        "file": interface["file"],
                        "functions": len(interface.get("functions", [])),
                        "status": "✅ PASS" if has_functions else "⚠️ WARN",
                        "message": f"Found {len(interface.get('functions', []))} functions" if has_functions else "No functions found"
                    }
                    test_results["test_details"].append(test_detail)
                    if has_functions:
                        test_results["passed_tests"] += 1
                    else:
                        test_results["failed_tests"] += 1
                
                # Djangoルートテスト
                for url in active_routes.get("django_urls", []):
                    test_results["total_tests"] += 1
                    test_detail = {
                        "type": "django",
                        "method": url["method"],
                        "path": url["path"],
                        "source": url["source"],
                        "status": "✅ PASS",
                        "message": "Django URL pattern found"
                    }
                    test_results["test_details"].append(test_detail)
                    test_results["passed_tests"] += 1
                
                return test_results
                
            except Exception as e:
                return {"error": f"Test execution failed: {str(e)}"}
        else:
            # API経由でテスト（フォールバック）
            try:
                response = requests.get(f"{self.base_url}/routes/test")
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"Test API request failed: {response.status_code}"}
            except Exception as e:
                return {"error": f"Test API connection failed: {str(e)}"}

class GradioAPITester:
    """Gradio API テスト機能"""
    
    def __init__(self, base_url="http://localhost:7860"):
        self.base_url = base_url
        self.gradio_base = f"{base_url}/gradio"
    
    def get_gradio_api_info(self) -> Dict[str, Any]:
        """Gradio API情報を取得"""
        try:
            api_url = f"{self.gradio_base}/?view=api"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                # HTMLレスポンスからAPI情報を抽出
                content = response.text
                
                # API エンドポイントを検索
                import re
                api_patterns = re.findall(r'/api/[^"\'>\s]+', content)
                
                return {
                    "status": "success",
                    "api_url": api_url,
                    "endpoints": list(set(api_patterns)),
                    "total_endpoints": len(set(api_patterns)),
                    "response_status": response.status_code
                }
            else:
                return {
                    "status": "error",
                    "message": f"API info request failed with status {response.status_code}",
                    "api_url": api_url
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get API info: {str(e)}",
                "api_url": api_url if 'api_url' in locals() else None
            }
    
    def test_specific_gradio_function(self, fn_index: int = 0, input_data: List = None) -> Dict[str, Any]:
        """特定のGradio関数をテスト"""
        try:
            if input_data is None:
                input_data = []
            
            predict_url = f"{self.gradio_base}/api/predict"
            
            payload = {
                "fn_index": fn_index,
                "data": input_data,
                "session_hash": "test_session"
            }
            
            response = requests.post(predict_url, json=payload, timeout=15)
            
            result = {
                "fn_index": fn_index,
                "input_data": input_data,
                "status_code": response.status_code,
                "url": predict_url,
                "success": False
            }
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    result.update({
                        "success": True,
                        "response_data": response_data,
                        "has_data": "data" in response_data,
                        "data_length": len(response_data.get("data", [])) if "data" in response_data else 0,
                        "duration": response_data.get("duration"),
                        "error": response_data.get("error")
                    })
                except json.JSONDecodeError:
                    result.update({
                        "success": False,
                        "error": "Invalid JSON response",
                        "response_text": response.text[:200]
                    })
            else:
                result.update({
                    "error": f"HTTP {response.status_code}",
                    "response_text": response.text[:200]
                })
            
            return result
            
        except Exception as e:
            return {
                "fn_index": fn_index,
                "input_data": input_data,
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def discover_and_test_functions(self) -> Dict[str, Any]:
        """Gradio関数を発見してテスト"""
        try:
            # 設定を取得して利用可能な関数を確認
            config_url = f"{self.gradio_base}/config"
            config_response = requests.get(config_url, timeout=10)
            
            result = {
                "config_accessible": config_response.status_code == 200,
                "function_tests": [],
                "total_functions": 0,
                "successful_tests": 0,
                "failed_tests": 0
            }
            
            if config_response.status_code == 200:
                try:
                    config_data = config_response.json()
                    dependencies = config_data.get("dependencies", [])
                    result["total_functions"] = len(dependencies)
                    
                    # 最初の5個の関数をテスト
                    for i, dependency in enumerate(dependencies[:5]):
                        inputs = dependency.get("inputs", [])
                        
                        # 簡単なテストデータを準備
                        test_data = []
                        for input_comp in inputs:
                            component_type = input_comp.get("component", "")
                            if "text" in component_type.lower():
                                test_data.append("test input")
                            elif "number" in component_type.lower():
                                test_data.append(0)
                            elif "checkbox" in component_type.lower():
                                test_data.append(False)
                            else:
                                test_data.append("")
                        
                        # 関数をテスト
                        test_result = self.test_specific_gradio_function(i, test_data)
                        test_result["dependency_info"] = dependency
                        result["function_tests"].append(test_result)
                        
                        if test_result.get("success"):
                            result["successful_tests"] += 1
                        else:
                            result["failed_tests"] += 1
                
                except json.JSONDecodeError:
                    result["config_error"] = "Invalid JSON in config response"
            else:
                result["config_error"] = f"Config request failed with status {config_response.status_code}"
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "error_type": type(e).__name__,
                "config_accessible": False,
                "function_tests": [],
                "total_functions": 0,
                "successful_tests": 0,
                "failed_tests": 0
            }
    
    def test_gradio_connection(self) -> Dict[str, Any]:
        """Gradio接続テスト"""
        try:
            # メインページテスト
            main_response = requests.get(self.gradio_base, timeout=10)
            
            # API情報取得テスト
            api_info = self.get_gradio_api_info()
            
            # 設定API テスト
            config_url = f"{self.gradio_base}/config"
            config_response = requests.get(config_url, timeout=5)
            
            return {
                "gradio_main": {
                    "url": self.gradio_base,
                    "status": main_response.status_code,
                    "accessible": main_response.status_code == 200
                },
                "gradio_config": {
                    "url": config_url,
                    "status": config_response.status_code,
                    "accessible": config_response.status_code == 200
                },
                "api_info": api_info,
                "overall_status": "healthy" if main_response.status_code == 200 else "error"
            }
            
        except Exception as e:
            return {
                "overall_status": "error",
                "error_message": str(e),
                "gradio_main": {"accessible": False},
                "gradio_config": {"accessible": False},
                "api_info": {"status": "error", "message": str(e)}
            }
    
    def test_gradio_api_endpoints(self) -> Dict[str, Any]:
        """Gradio APIエンドポイントをテスト"""
        api_info = self.get_gradio_api_info()
        
        if api_info["status"] != "success":
            return api_info
        
        test_results = []
        response_details = []
        
        for endpoint in api_info["endpoints"][:15]:  # 最初の15個をテスト
            try:
                test_url = f"{self.gradio_base}{endpoint}"
                response = requests.get(test_url, timeout=10)
                
                # レスポンス内容を分析
                content_type = response.headers.get('content-type', 'unknown')
                response_text = ""
                is_json = False
                json_data = None
                
                try:
                    if 'application/json' in content_type:
                        json_data = response.json()
                        is_json = True
                        response_text = json.dumps(json_data, indent=2)[:500]  # 最初の500文字
                    else:
                        response_text = str(response.content[:200], 'utf-8', errors='ignore')
                except:
                    response_text = "Unable to decode response content"
                
                test_result = {
                    "endpoint": endpoint,
                    "url": test_url,
                    "status_code": response.status_code,
                    "accessible": 200 <= response.status_code < 400,
                    "response_size": len(response.content),
                    "content_type": content_type,
                    "is_json": is_json,
                    "response_time": getattr(response, 'elapsed', None),
                    "headers": dict(response.headers),
                    "response_preview": response_text
                }
                
                # 特別なエンドポイントの詳細分析
                if endpoint in ['/api/predict', '/api/predict/', '/config']:
                    if is_json and json_data:
                        if 'fn_index' in str(json_data) or 'dependencies' in str(json_data):
                            test_result["endpoint_type"] = "gradio_api"
                            test_result["analysis"] = "Gradio API endpoint with function definitions"
                        elif 'version' in str(json_data):
                            test_result["endpoint_type"] = "config"
                            test_result["analysis"] = "Configuration endpoint"
                    
                test_results.append(test_result)
                
                # 詳細レスポンス情報を保存
                if is_json and json_data:
                    response_details.append({
                        "endpoint": endpoint,
                        "json_keys": list(json_data.keys()) if isinstance(json_data, dict) else [],
                        "data_type": type(json_data).__name__,
                        "sample_data": json_data
                    })
                
            except Exception as e:
                test_results.append({
                    "endpoint": endpoint,
                    "url": test_url if 'test_url' in locals() else f"{self.gradio_base}{endpoint}",
                    "accessible": False,
                    "error": str(e),
                    "error_type": type(e).__name__
                })
        
        successful_tests = sum(1 for result in test_results if result.get('accessible', False))
        json_endpoints = sum(1 for result in test_results if result.get('is_json', False))
        
        return {
            "total_endpoints_tested": len(test_results),
            "successful_tests": successful_tests,
            "failed_tests": len(test_results) - successful_tests,
            "json_endpoints": json_endpoints,
            "success_rate": f"{(successful_tests/len(test_results)*100):.1f}%" if test_results else "0%",
            "test_results": test_results,
            "response_details": response_details,
            "api_info": api_info
        }

# インターフェースのインスタンス作成
cicd_interface = CICDInterface()
gradio_api_tester = GradioAPITester()

def format_routes_display(route_type: str) -> str:
    """ルート情報を整理して表示"""
    try:
        data = cicd_interface.get_routes_data(route_type)
        
        if "error" in data:
            return f"❌ Error: {data['error']}"
        
        output = []
        output.append(f"🛣️ {route_type.upper()} Routes Summary")
        output.append("=" * 50)
        
        # サマリー
        summary = data.get("summary", {})
        if summary:
            output.append(f"📊 Total Routes: {summary.get('total_routes', 0)}")
            output.append(f"📍 FastAPI: {summary.get('fastapi_routes', 0)}")
            output.append(f"🎨 Gradio: {summary.get('gradio_interfaces', 0)}")
            output.append(f"🐍 Django: {summary.get('django_urls', 0)}")
            output.append("")
        
        # FastAPIルート
        fastapi_routes = data.get("fastapi_routes", [])
        if fastapi_routes:
            output.append("📍 FastAPI Routes:")
            output.append("-" * 30)
            for route in fastapi_routes[:10]:  # 最初の10個のみ表示
                output.append(f"  {route['method']:<6} {route['path']:<30} ({route['source']})")
            if len(fastapi_routes) > 10:
                output.append(f"  ... and {len(fastapi_routes) - 10} more routes")
            output.append("")
        
        # Gradioインターフェース
        gradio_interfaces = data.get("gradio_interfaces", [])
        if gradio_interfaces:
            output.append("🎨 Gradio Interfaces:")
            output.append("-" * 30)
            for interface in gradio_interfaces[:5]:  # 最初の5個のみ表示
                functions = interface.get("functions", [])
                output.append(f"  🎯 {interface['category']}: {interface['file']}")
                output.append(f"     Functions: {', '.join(functions[:3])}")
                if len(functions) > 3:
                    output.append(f"     ... and {len(functions) - 3} more functions")
            if len(gradio_interfaces) > 5:
                output.append(f"  ... and {len(gradio_interfaces) - 5} more interfaces")
            output.append("")
        
        # Djangoルート
        django_urls = data.get("django_urls", [])
        if django_urls:
            output.append("🐍 Django URLs:")
            output.append("-" * 30)
            for url in django_urls[:10]:  # 最初の10個のみ表示
                output.append(f"  {url['method']:<6} {url['path']:<30} ({url['source']})")
            if len(django_urls) > 10:
                output.append(f"  ... and {len(django_urls) - 10} more URLs")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Error formatting routes: {str(e)}"

def run_cicd_tests() -> str:
    """CI/CDテストを実行して結果を表示"""
    try:
        results = cicd_interface.run_tests()
        
        if "error" in results:
            return f"❌ Test Error: {results['error']}"
        
        output = []
        output.append("🧪 CI/CD Test Results")
        output.append("=" * 50)
        output.append(f"⏰ Timestamp: {results.get('timestamp', 'N/A')}")
        output.append(f"📊 Total Tests: {results.get('total_tests', 0)}")
        output.append(f"✅ Passed: {results.get('passed_tests', 0)}")
        output.append(f"❌ Failed: {results.get('failed_tests', 0)}")
        
        # テスト通過率
        total = results.get('total_tests', 0)
        passed = results.get('passed_tests', 0)
        if total > 0:
            pass_rate = (passed / total) * 100
            output.append(f"📈 Pass Rate: {pass_rate:.1f}%")
        
        output.append("")
        output.append("📋 Test Details:")
        output.append("-" * 30)
        
        # テスト詳細
        for detail in results.get('test_details', [])[:20]:  # 最初の20個のみ表示
            test_type = detail.get('type', 'unknown')
            status = detail.get('status', 'unknown')
            message = detail.get('message', 'No message')
            
            if test_type == 'fastapi':
                output.append(f"  {status} FastAPI {detail.get('method', '')} {detail.get('path', '')}")
            elif test_type == 'gradio':
                output.append(f"  {status} Gradio {detail.get('category', '')} ({detail.get('functions', 0)} functions)")
            elif test_type == 'django':
                output.append(f"  {status} Django {detail.get('path', '')}")
            
            output.append(f"       {message}")
        
        if len(results.get('test_details', [])) > 20:
            remaining = len(results.get('test_details', [])) - 20
            output.append(f"  ... and {remaining} more test results")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Error running tests: {str(e)}"

def get_route_comparison() -> str:
    """全ルートとアクティブルートの比較"""
    try:
        all_routes = cicd_interface.get_routes_data("all")
        active_routes = cicd_interface.get_routes_data("active")
        
        if "error" in all_routes or "error" in active_routes:
            return "❌ Error getting route data for comparison"
        
        output = []
        output.append("🔍 Route Comparison (All vs Active)")
        output.append("=" * 50)
        
        all_summary = all_routes.get("summary", {})
        active_summary = active_routes.get("summary", {})
        
        output.append("📊 Summary Comparison:")
        output.append(f"  FastAPI Routes: {all_summary.get('fastapi_routes', 0)} total → {active_summary.get('fastapi_routes', 0)} active")
        output.append(f"  Gradio Interfaces: {all_summary.get('gradio_interfaces', 0)} total → {active_summary.get('gradio_interfaces', 0)} active")
        output.append(f"  Django URLs: {all_summary.get('django_urls', 0)} total → {active_summary.get('django_urls', 0)} active")
        
        total_all = all_summary.get('total_routes', 0)
        total_active = active_summary.get('total_routes', 0)
        
        if total_all > 0:
            active_ratio = (total_active / total_all) * 100
            output.append(f"\n🎯 Active Ratio: {active_ratio:.1f}% ({total_active}/{total_all})")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Error in route comparison: {str(e)}"

# テスト関数群
def test_gradio_api_connection() -> str:
    """Gradio API接続とエンドポイントをテスト"""
    try:
        # 接続テスト
        connection_result = gradio_api_tester.test_gradio_connection()
        
        output = []
        output.append("🔌 Gradio Connection Test")
        output.append("=" * 50)
        
        # メイン接続状況
        main_status = connection_result.get("gradio_main", {})
        main_accessible = main_status.get("accessible", False)
        main_status_icon = "✅" if main_accessible else "❌"
        output.append(f"{main_status_icon} Main Gradio: {main_status.get('url', 'N/A')} (Status: {main_status.get('status', 'N/A')})")
        
        # 設定API状況
        config_status = connection_result.get("gradio_config", {})
        config_accessible = config_status.get("accessible", False)
        config_status_icon = "✅" if config_accessible else "❌"
        output.append(f"{config_status_icon} Config API: {config_status.get('url', 'N/A')} (Status: {config_status.get('status', 'N/A')})")
        
        # API情報
        api_info = connection_result.get("api_info", {})
        if api_info.get("status") == "success":
            output.append(f"📡 API Endpoints Found: {api_info.get('total_endpoints', 0)}")
            output.append(f"🔗 API Info URL: {api_info.get('api_url', 'N/A')}")
        else:
            output.append(f"❌ API Info Error: {api_info.get('message', 'Unknown error')}")
        
        # 全体的なステータス
        overall = connection_result.get("overall_status", "unknown")
        overall_icon = "✅" if overall == "healthy" else "❌"
        output.append(f"\n{overall_icon} Overall Status: {overall.upper()}")
        
        if connection_result.get("error_message"):
            output.append(f"❌ Error Details: {connection_result['error_message']}")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Gradio API test failed: {str(e)}"

# Gradioインターフェースの作成
def create_cicd_interface():
    """CI/CD Gradio インターフェースを作成"""
    
    with gr.Blocks(title="🚀 CI/CD Route Management", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🚀 CI/CD Route Management & Testing")
        gr.Markdown("Laravel風アーキテクチャのルート管理とテスト機能")
        
        with gr.Tabs():
            # ルート一覧タブ
            with gr.Tab("📍 Route List"):
                gr.Markdown("## ルート一覧")
                
                with gr.Row():
                    route_type_radio = gr.Radio(
                        choices=["active", "all"],
                        value="active",
                        label="Route Type",
                        info="アクティブルートのみ or 全ルート"
                    )
                    refresh_btn = gr.Button("🔄 Refresh", variant="secondary")
                
                route_display = gr.Textbox(
                    label="Route Information",
                    lines=20,
                    max_lines=30,
                    interactive=False
                )
                
                refresh_btn.click(
                    fn=format_routes_display,
                    inputs=[route_type_radio],
                    outputs=[route_display]
                )
                
                route_type_radio.change(
                    fn=format_routes_display,
                    inputs=[route_type_radio],
                    outputs=[route_display]
                )
            
            # テスト実行タブ
            with gr.Tab("🧪 Testing"):
                gr.Markdown("## CI/CD テスト実行")
                
                with gr.Row():
                    test_btn = gr.Button("🧪 Run Tests", variant="primary")
                    comparison_btn = gr.Button("🔍 Compare Routes", variant="secondary")
                
                with gr.Row():
                    gradio_connection_btn = gr.Button("🔌 Test Gradio Connection", variant="secondary")
                    gradio_api_btn = gr.Button("📡 Test Gradio APIs", variant="secondary")
                
                with gr.Row():
                    gradio_functions_btn = gr.Button("🎯 Test Gradio Functions", variant="secondary")
                    gradio_detailed_btn = gr.Button("🔍 Detailed API Analysis", variant="secondary")
                
                test_results = gr.Textbox(
                    label="Test Results",
                    lines=25,
                    max_lines=35,
                    interactive=False
                )
                
                test_btn.click(
                    fn=run_cicd_tests,
                    outputs=[test_results]
                )
                
                comparison_btn.click(
                    fn=get_route_comparison,
                    outputs=[test_results]
                )
                
                gradio_connection_btn.click(
                    fn=test_gradio_api_connection,
                    outputs=[test_results]
                )
                
                gradio_api_btn.click(
                    fn=test_gradio_api_endpoints,
                    outputs=[test_results]
                )
                
                gradio_functions_btn.click(
                    fn=test_gradio_functions,
                    outputs=[test_results]
                )
                
                gradio_detailed_btn.click(
                    fn=lambda: test_gradio_connection() + "\n\n" + test_gradio_api_endpoints() + "\n\n" + test_gradio_functions(),
                    outputs=[test_results]
                )
            
            # API情報タブ
            with gr.Tab("📡 API Info"):
                gr.Markdown("## Route API Endpoints")
                
                with gr.Row():
                    api_list_btn = gr.Button("📋 Get Gradio API List", variant="primary")
                    api_test_btn = gr.Button("🧪 Test API Endpoints", variant="secondary")
                
                api_info_display = gr.Textbox(
                    label="API Information",
                    lines=20,
                    max_lines=30,
                    interactive=False
                )
                
                api_list_btn.click(
                    fn=get_gradio_api_list,
                    outputs=[api_info_display]
                )
                
                api_test_btn.click(
                    fn=test_gradio_api_endpoints,
                    outputs=[api_info_display]
                )
                
                gr.Markdown("""
                ### 利用可能なAPI:
                - `GET /api/v1/routes/all` - 全ルート取得
                - `GET /api/v1/routes/active` - アクティブルート取得
                - `GET /api/v1/routes/summary` - サマリー情報
                - `GET /api/v1/routes/test` - テスト実行
                - `GET /api/v1/routes/health` - ヘルスチェック
                
                ### Gradio API:
                - `GET /gradio/?view=api` - Gradio API ドキュメント
                - `/gradio/config` - Gradio設定
                - `/gradio/api/*` - Gradio API エンドポイント
                
                ### Artisan Commands:
                - `python artisan route:list` - 全ルート表示
                - `python artisan route:active` - アクティブルート表示
                - `python artisan cicd test` - CI/CDテスト
                """)
        
        # 初期データロード
        interface.load(
            fn=lambda: format_routes_display("active"),
            outputs=[route_display]
        )
    
# Gradioインターフェースのインスタンス
gradio_interface = create_cicd_interface()

def test_gradio_api_endpoints() -> str:
    """Gradio APIエンドポイントの詳細テスト"""
    try:
        # エンドポイントテスト実行
        test_result = gradio_api_tester.test_gradio_api_endpoints()
        
        output = []
        output.append("🧪 Gradio API Endpoints Test")
        output.append("=" * 50)
        
        if "error" in test_result or test_result.get("api_info", {}).get("status") == "error":
            error_msg = test_result.get("error_message") or test_result.get("api_info", {}).get("message", "Unknown error")
            output.append(f"❌ Test Error: {error_msg}")
            return "\n".join(output)
        
        # テスト統計
        total_tested = test_result.get("total_endpoints_tested", 0)
        successful = test_result.get("successful_tests", 0)
        failed = test_result.get("failed_tests", 0)
        json_endpoints = test_result.get("json_endpoints", 0)
        success_rate = test_result.get("success_rate", "0%")
        
        output.append(f"📊 Test Statistics:")
        output.append(f"   Total Endpoints Tested: {total_tested}")
        output.append(f"   ✅ Successful: {successful}")
        output.append(f"   ❌ Failed: {failed}")
        output.append(f"   � JSON Responses: {json_endpoints}")
        output.append(f"   �📈 Success Rate: {success_rate}")
        output.append("")
        
        # API情報
        api_info = test_result.get("api_info", {})
        if api_info.get("status") == "success":
            output.append(f"🔗 Total Available Endpoints: {api_info.get('total_endpoints', 0)}")
            output.append(f"📡 API Documentation: {api_info.get('api_url', 'N/A')}")
            output.append("")
        
        # 個別テスト結果
        test_results = test_result.get("test_results", [])
        if test_results:
            output.append("📋 Endpoint Test Details:")
            output.append("-" * 30)
            
            for i, result in enumerate(test_results[:12], 1):  # 最初の12個のみ表示
                endpoint = result.get("endpoint", "unknown")
                accessible = result.get("accessible", False)
                status_code = result.get("status_code", "N/A")
                
                status_icon = "✅" if accessible else "❌"
                output.append(f"{i:2d}. {status_icon} {endpoint}")
                
                if accessible:
                    content_type = result.get("content_type", "unknown")
                    response_size = result.get("response_size", 0)
                    is_json = result.get("is_json", False)
                    json_icon = "📋" if is_json else "📄"
                    
                    output.append(f"      Status: {status_code}, {json_icon} Type: {content_type}, Size: {response_size} bytes")
                    
                    # 特別なエンドポイントの分析結果
                    if result.get("endpoint_type"):
                        endpoint_type = result.get("endpoint_type")
                        analysis = result.get("analysis", "")
                        output.append(f"      🔍 Type: {endpoint_type} - {analysis}")
                    
                    # レスポンスプレビュー（JSONの場合）
                    if is_json and result.get("response_preview"):
                        preview = result.get("response_preview", "")[:100]
                        if len(preview) >= 100:
                            preview += "..."
                        output.append(f"      📝 Preview: {preview}")
                        
                else:
                    error = result.get("error", f"HTTP {status_code}")
                    error_type = result.get("error_type", "Unknown")
                    output.append(f"      ❌ Error ({error_type}): {error}")
            
            if len(test_results) > 12:
                output.append(f"   ... and {len(test_results) - 12} more endpoints")
        
        # レスポンス詳細分析
        response_details = test_result.get("response_details", [])
        if response_details:
            output.append("")
            output.append("🔍 JSON Response Analysis:")
            output.append("-" * 30)
            
            for detail in response_details[:5]:  # 最初の5個の詳細
                endpoint = detail.get("endpoint", "unknown")
                data_type = detail.get("data_type", "unknown")
                json_keys = detail.get("json_keys", [])
                
                output.append(f"📊 {endpoint}")
                output.append(f"    Data Type: {data_type}")
                if json_keys:
                    keys_str = ", ".join(json_keys[:5])
                    if len(json_keys) > 5:
                        keys_str += f"... (+{len(json_keys)-5} more)"
                    output.append(f"    Keys: {keys_str}")
                
                # 特定のキーワードを含む場合は特別に表示
                sample_data = detail.get("sample_data", {})
                if isinstance(sample_data, dict):
                    if "fn_index" in sample_data or "dependencies" in sample_data:
                        output.append("    🎯 Contains Gradio function definitions")
                    elif "version" in sample_data:
                        output.append("    ⚙️ Contains configuration information")
                    elif "components" in sample_data:
                        output.append("    🧩 Contains component definitions")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Gradio API endpoints test failed: {str(e)}"

def test_gradio_functions() -> str:
    """Gradio関数の機能テスト"""
    try:
        # 関数発見とテスト実行
        test_result = gradio_api_tester.discover_and_test_functions()
        
        output = []
        output.append("🎯 Gradio Functions Test")
        output.append("=" * 50)
        
        if "error" in test_result:
            error_msg = test_result.get("error", "Unknown error")
            error_type = test_result.get("error_type", "Unknown")
            output.append(f"❌ Test Error ({error_type}): {error_msg}")
            return "\n".join(output)
        
        # 設定アクセス状況
        config_accessible = test_result.get("config_accessible", False)
        config_icon = "✅" if config_accessible else "❌"
        output.append(f"{config_icon} Gradio Config Access: {'Available' if config_accessible else 'Failed'}")
        
        if test_result.get("config_error"):
            output.append(f"⚠️ Config Error: {test_result['config_error']}")
        
        # 関数テスト統計
        total_functions = test_result.get("total_functions", 0)
        successful_tests = test_result.get("successful_tests", 0)
        failed_tests = test_result.get("failed_tests", 0)
        
        output.append(f"\n📊 Function Test Statistics:")
        output.append(f"   Total Functions Found: {total_functions}")
        output.append(f"   ✅ Successful Tests: {successful_tests}")
        output.append(f"   ❌ Failed Tests: {failed_tests}")
        
        if total_functions > 0:
            success_rate = (successful_tests / min(5, total_functions)) * 100  # 最大5個をテスト
            output.append(f"   📈 Success Rate: {success_rate:.1f}%")
        
        # 個別関数テスト結果
        function_tests = test_result.get("function_tests", [])
        if function_tests:
            output.append("\n🔍 Function Test Details:")
            output.append("-" * 30)
            
            for i, test in enumerate(function_tests, 1):
                fn_index = test.get("fn_index", "unknown")
                success = test.get("success", False)
                status_icon = "✅" if success else "❌"
                
                output.append(f"{i}. {status_icon} Function {fn_index}")
                
                # 入力データ
                input_data = test.get("input_data", [])
                if input_data:
                    input_preview = str(input_data)[:50]
                    if len(str(input_data)) > 50:
                        input_preview += "..."
                    output.append(f"   📥 Input: {input_preview}")
                
                if success:
                    # 成功時の詳細
                    has_data = test.get("has_data", False)
                    data_length = test.get("data_length", 0)
                    duration = test.get("duration")
                    
                    output.append(f"   📤 Response: {data_length} items" if has_data else "   📤 Response: No data")
                    if duration:
                        output.append(f"   ⏱️ Duration: {duration}s")
                    
                    # エラーがある場合
                    if test.get("error"):
                        output.append(f"   ⚠️ Function Error: {test['error']}")
                        
                else:
                    # 失敗時の詳細
                    error = test.get("error", "Unknown error")
                    error_type = test.get("error_type", "Unknown")
                    output.append(f"   ❌ Error ({error_type}): {error}")
                    
                    if test.get("response_text"):
                        response_preview = test["response_text"][:100]
                        output.append(f"   📄 Response: {response_preview}")
                
                # 依存関係情報
                dependency_info = test.get("dependency_info", {})
                if dependency_info:
                    inputs = dependency_info.get("inputs", [])
                    outputs = dependency_info.get("outputs", [])
                    output.append(f"   🔗 I/O: {len(inputs)} inputs, {len(outputs)} outputs")
                
                output.append("")
        
        # テスト済み関数が全体の一部の場合
        if total_functions > len(function_tests):
            remaining = total_functions - len(function_tests)
            output.append(f"📝 Note: {remaining} additional functions not tested")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Gradio functions test failed: {str(e)}"

def get_gradio_api_list() -> str:
    """Gradio API一覧を取得して表示"""
    try:
        api_info = gradio_api_tester.get_gradio_api_info()
        
        output = []
        output.append("📡 Gradio API Endpoints List")
        output.append("=" * 50)
        
        if api_info.get("status") != "success":
            error_msg = api_info.get("message", "Unknown error")
            output.append(f"❌ Error: {error_msg}")
            return "\n".join(output)
        
        endpoints = api_info.get("endpoints", [])
        total_endpoints = len(endpoints)
        
        output.append(f"🔗 API Documentation URL: {api_info.get('api_url', 'N/A')}")
        output.append(f"📊 Total Endpoints: {total_endpoints}")
        output.append("")
        
        if endpoints:
            output.append("📋 Available API Endpoints:")
            output.append("-" * 30)
            
            # エンドポイントをカテゴリ別に分類
            api_endpoints = [ep for ep in endpoints if ep.startswith('/api/')]
            other_endpoints = [ep for ep in endpoints if not ep.startswith('/api/')]
            
            if api_endpoints:
                output.append("🔧 API Endpoints:")
                for i, endpoint in enumerate(api_endpoints[:15], 1):
                    output.append(f"  {i:2d}. {endpoint}")
                if len(api_endpoints) > 15:
                    output.append(f"      ... and {len(api_endpoints) - 15} more API endpoints")
                output.append("")
            
            if other_endpoints:
                output.append("🌐 Other Endpoints:")
                for i, endpoint in enumerate(other_endpoints[:10], 1):
                    output.append(f"  {i:2d}. {endpoint}")
                if len(other_endpoints) > 10:
                    output.append(f"      ... and {len(other_endpoints) - 10} more endpoints")
        else:
            output.append("⚠️ No API endpoints found")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Failed to get Gradio API list: {str(e)}"

# ...existing code...
    """Gradio関数の機能テスト"""
    try:
        # 関数発見とテスト実行
        test_result = gradio_api_tester.discover_and_test_functions()
        
        output = []
        output.append("🎯 Gradio Functions Test")
        output.append("=" * 50)
        
        if "error" in test_result:
            error_msg = test_result.get("error", "Unknown error")
            error_type = test_result.get("error_type", "Unknown")
            output.append(f"❌ Test Error ({error_type}): {error_msg}")
            return "\n".join(output)
        
        # 設定アクセス状況
        config_accessible = test_result.get("config_accessible", False)
        config_icon = "✅" if config_accessible else "❌"
        output.append(f"{config_icon} Gradio Config Access: {'Available' if config_accessible else 'Failed'}")
        
        if test_result.get("config_error"):
            output.append(f"⚠️ Config Error: {test_result['config_error']}")
        
        # 関数テスト統計
        total_functions = test_result.get("total_functions", 0)
        successful_tests = test_result.get("successful_tests", 0)
        failed_tests = test_result.get("failed_tests", 0)
        
        output.append(f"\n📊 Function Test Statistics:")
        output.append(f"   Total Functions Found: {total_functions}")
        output.append(f"   ✅ Successful Tests: {successful_tests}")
        output.append(f"   ❌ Failed Tests: {failed_tests}")
        
        if total_functions > 0:
            success_rate = (successful_tests / min(5, total_functions)) * 100  # 最大5個をテスト
            output.append(f"   📈 Success Rate: {success_rate:.1f}%")
        
        # 個別関数テスト結果
        function_tests = test_result.get("function_tests", [])
        if function_tests:
            output.append("\n🔍 Function Test Details:")
            output.append("-" * 30)
            
            for i, test in enumerate(function_tests, 1):
                fn_index = test.get("fn_index", "unknown")
                success = test.get("success", False)
                status_icon = "✅" if success else "❌"
                
                output.append(f"{i}. {status_icon} Function {fn_index}")
                
                # 入力データ
                input_data = test.get("input_data", [])
                if input_data:
                    input_preview = str(input_data)[:50]
                    if len(str(input_data)) > 50:
                        input_preview += "..."
                    output.append(f"   📥 Input: {input_preview}")
                
                if success:
                    # 成功時の詳細
                    has_data = test.get("has_data", False)
                    data_length = test.get("data_length", 0)
                    duration = test.get("duration")
                    
                    output.append(f"   📤 Response: {data_length} items" if has_data else "   📤 Response: No data")
                    if duration:
                        output.append(f"   ⏱️ Duration: {duration}s")
                    
                    # エラーがある場合
                    if test.get("error"):
                        output.append(f"   ⚠️ Function Error: {test['error']}")
                        
                else:
                    # 失敗時の詳細
                    error = test.get("error", "Unknown error")
                    error_type = test.get("error_type", "Unknown")
                    output.append(f"   ❌ Error ({error_type}): {error}")
                    
                    if test.get("response_text"):
                        response_preview = test["response_text"][:100]
                        output.append(f"   📄 Response: {response_preview}")
                
                # 依存関係情報
                dependency_info = test.get("dependency_info", {})
                if dependency_info:
                    inputs = dependency_info.get("inputs", [])
                    outputs = dependency_info.get("outputs", [])
                    output.append(f"   🔗 I/O: {len(inputs)} inputs, {len(outputs)} outputs")
                
                output.append("")
        
        # テスト済み関数が全体の一部の場合
        if total_functions > len(function_tests):
            remaining = total_functions - len(function_tests)
            output.append(f"📝 Note: {remaining} additional functions not tested")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Gradio functions test failed: {str(e)}"
    """Gradio API一覧を取得して表示"""
    try:
        api_info = gradio_api_tester.get_gradio_api_info()
        
        output = []
        output.append("📡 Gradio API Endpoints List")
        output.append("=" * 50)
        
        if api_info.get("status") != "success":
            error_msg = api_info.get("message", "Unknown error")
            output.append(f"❌ Error: {error_msg}")
            return "\n".join(output)
        
        endpoints = api_info.get("endpoints", [])
        total_endpoints = len(endpoints)
        
        output.append(f"🔗 API Documentation URL: {api_info.get('api_url', 'N/A')}")
        output.append(f"📊 Total Endpoints: {total_endpoints}")
        output.append("")
        
        if endpoints:
            output.append("📋 Available API Endpoints:")
            output.append("-" * 30)
            
            # エンドポイントをカテゴリ別に分類
            api_endpoints = [ep for ep in endpoints if ep.startswith('/api/')]
            other_endpoints = [ep for ep in endpoints if not ep.startswith('/api/')]
            
            if api_endpoints:
                output.append("🔧 API Endpoints:")
                for i, endpoint in enumerate(api_endpoints[:15], 1):
                    output.append(f"  {i:2d}. {endpoint}")
                if len(api_endpoints) > 15:
                    output.append(f"      ... and {len(api_endpoints) - 15} more API endpoints")
                output.append("")
            
            if other_endpoints:
                output.append("🌐 Other Endpoints:")
                for i, endpoint in enumerate(other_endpoints[:10], 1):
                    output.append(f"  {i:2d}. {endpoint}")
                if len(other_endpoints) > 10:
                    output.append(f"      ... and {len(other_endpoints) - 10} more endpoints")
        else:
            output.append("⚠️ No API endpoints found")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Failed to get Gradio API list: {str(e)}"

# ...existing code...
