"""
システム自動化モジュール
GPT-ENGINEERで生成されたシステムをGitHubにアップし、
Controller/Routerを自動認識する機能
"""

import os
import subprocess
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
import tempfile
import shutil

class SystemAutomation:
    """システム自動化クラス"""
    
    def __init__(self, github_token: str, base_workspace: str = "/workspaces/fastapi_django_main_live"):
        self.github_token = github_token
        self.base_workspace = Path(base_workspace)
        self.controllers_dir = self.base_workspace / "controllers"
        self.routers_dir = self.base_workspace / "routers"
        
    def create_github_repository(self, repo_name: str, description: str = "") -> Dict:
        """GitHubリポジトリを作成"""
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            data = {
                'name': repo_name,
                'description': description,
                'private': False,
                'auto_init': True
            }
            
            response = requests.post(
                'https://api.github.com/user/repos',
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                repo_data = response.json()
                return {
                    'success': True,
                    'url': repo_data['html_url'],
                    'clone_url': repo_data['clone_url'],
                    'ssh_url': repo_data['ssh_url']
                }
            else:
                return {
                    'success': False,
                    'error': f"GitHub API エラー: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"リポジトリ作成エラー: {str(e)}"
            }
    
    def push_to_github(self, local_path: str, repo_url: str, commit_message: str = "Initial commit") -> Dict:
        """ローカルのコードをGitHubにプッシュ"""
        try:
            local_path = Path(local_path)
            
            if not local_path.exists():
                return {'success': False, 'error': 'ローカルパスが存在しません'}
            
            # Git リポジトリを初期化
            subprocess.run(['git', 'init'], cwd=local_path, check=True)
            subprocess.run(['git', 'add', '.'], cwd=local_path, check=True)
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=local_path, check=True)
            subprocess.run(['git', 'branch', '-M', 'main'], cwd=local_path, check=True)
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url], cwd=local_path, check=True)
            subprocess.run(['git', 'push', '-u', 'origin', 'main'], cwd=local_path, check=True)
            
            return {
                'success': True,
                'message': 'GitHubプッシュ完了'
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'error': f"Git操作エラー: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"プッシュエラー: {str(e)}"
            }
    
    def scan_for_controllers(self, generated_path: str) -> List[Dict]:
        """生成されたコードからController/Routerを検索"""
        controllers = []
        generated_path = Path(generated_path)
        
        if not generated_path.exists():
            return controllers
        
        # Pythonファイルをスキャン
        for file_path in generated_path.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # FastAPI router検索
                if 'APIRouter' in content or 'router' in content.lower():
                    controllers.append({
                        'type': 'fastapi_router',
                        'file': str(file_path),
                        'name': file_path.stem,
                        'content_preview': content[:200] + '...' if len(content) > 200 else content
                    })
                
                # Gradio interface検索
                if 'gradio_interface' in content or 'gr.Blocks' in content:
                    controllers.append({
                        'type': 'gradio_interface',
                        'file': str(file_path),
                        'name': file_path.stem,
                        'content_preview': content[:200] + '...' if len(content) > 200 else content
                    })
                
                # Django views検索
                if 'django' in content.lower() and ('def ' in content or 'class ' in content):
                    controllers.append({
                        'type': 'django_view',
                        'file': str(file_path),
                        'name': file_path.stem,
                        'content_preview': content[:200] + '...' if len(content) > 200 else content
                    })
                    
            except Exception as e:
                print(f"ファイル読み込みエラー {file_path}: {e}")
        
        return controllers
    
    def auto_integrate_controllers(self, controllers: List[Dict]) -> Dict:
        """Controller/Routerを自動統合"""
        results = {
            'integrated': [],
            'errors': []
        }
        
        for controller in controllers:
            try:
                source_file = Path(controller['file'])
                controller_type = controller['type']
                
                if controller_type == 'fastapi_router':
                    # FastAPI routerを統合
                    dest_dir = self.routers_dir
                    dest_file = dest_dir / f"auto_{controller['name']}.py"
                    
                elif controller_type == 'gradio_interface':
                    # Gradio interfaceを統合
                    dest_dir = self.controllers_dir / "gradio_auto"
                    dest_dir.mkdir(exist_ok=True)
                    dest_file = dest_dir / f"{controller['name']}.py"
                    
                elif controller_type == 'django_view':
                    # Django viewを統合
                    dest_dir = self.controllers_dir / "django_auto"
                    dest_dir.mkdir(exist_ok=True)
                    dest_file = dest_dir / f"{controller['name']}.py"
                
                else:
                    continue
                
                # ファイルをコピー
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, dest_file)
                
                results['integrated'].append({
                    'type': controller_type,
                    'source': str(source_file),
                    'destination': str(dest_file),
                    'name': controller['name']
                })
                
            except Exception as e:
                results['errors'].append({
                    'controller': controller['name'],
                    'error': str(e)
                })
        
        return results
    
    def full_automation_pipeline(self, 
                                generated_folder: str, 
                                repo_name: str, 
                                description: str = "",
                                commit_message: str = "Generated system") -> Dict:
        """完全自動化パイプライン"""
        pipeline_results = {
            'github_repo': None,
            'github_push': None,
            'controllers_found': [],
            'integration_results': None,
            'success': False
        }
        
        try:
            # 1. GitHubリポジトリ作成
            print(f"🚀 GitHubリポジトリ作成: {repo_name}")
            repo_result = self.create_github_repository(repo_name, description)
            pipeline_results['github_repo'] = repo_result
            
            if not repo_result['success']:
                return pipeline_results
            
            # 2. GitHubにプッシュ
            print(f"📤 GitHubにプッシュ中...")
            push_result = self.push_to_github(
                generated_folder,
                repo_result['clone_url'],
                commit_message
            )
            pipeline_results['github_push'] = push_result
            
            # 3. Controller/Router検索
            print(f"🔍 Controller/Router検索中...")
            controllers = self.scan_for_controllers(generated_folder)
            pipeline_results['controllers_found'] = controllers
            
            # 4. 自動統合
            if controllers:
                print(f"🔧 Controller/Router自動統合中...")
                integration_result = self.auto_integrate_controllers(controllers)
                pipeline_results['integration_results'] = integration_result
            
            pipeline_results['success'] = True
            return pipeline_results
            
        except Exception as e:
            pipeline_results['error'] = str(e)
            return pipeline_results


def create_system_automation_interface():
    """システム自動化のGradio インターフェース"""
    import gradio as gr
    
    def run_automation_pipeline(github_token, repo_name, generated_folder, description):
        if not github_token or not repo_name or not generated_folder:
            return "❌ 必須項目を入力してください", ""
        
        automation = SystemAutomation(github_token)
        result = automation.full_automation_pipeline(
            generated_folder, 
            repo_name, 
            description
        )
        
        if result['success']:
            summary = f"""✅ 自動化パイプライン完了！

🔗 GitHub リポジトリ: {result['github_repo']['url']}
📤 プッシュ: {'成功' if result['github_push']['success'] else '失敗'}
🔍 検出されたController: {len(result['controllers_found'])}件
🔧 統合結果: {len(result['integration_results']['integrated']) if result['integration_results'] else 0}件統合済み
"""
            
            details = json.dumps(result, indent=2, ensure_ascii=False)
            return summary, details
        else:
            return f"❌ エラー: {result.get('error', '不明なエラー')}", json.dumps(result, indent=2, ensure_ascii=False)
    
    with gr.Blocks(title="🚀 システム自動化") as interface:
        gr.Markdown("# 🚀 システム自動化パイプライン")
        gr.Markdown("生成されたシステムを自動でGitHubにアップし、Controller/Routerを統合します")
        
        with gr.Row():
            with gr.Column():
                github_token_input = gr.Textbox(
                    label="GitHub Token",
                    type="password",
                    placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
                )
                repo_name_input = gr.Textbox(
                    label="リポジトリ名",
                    placeholder="my-generated-system"
                )
                generated_folder_input = gr.Textbox(
                    label="生成されたフォルダパス",
                    placeholder="/path/to/generated/system"
                )
                description_input = gr.Textbox(
                    label="リポジトリ説明",
                    placeholder="GPT-ENGINEERで生成されたシステム"
                )
                
                run_button = gr.Button("🚀 自動化実行", variant="primary")
            
            with gr.Column():
                result_summary = gr.Textbox(
                    label="実行結果サマリー",
                    lines=10,
                    interactive=False
                )
                result_details = gr.Textbox(
                    label="詳細結果 (JSON)",
                    lines=15,
                    interactive=False
                )
        
        run_button.click(
            fn=run_automation_pipeline,
            inputs=[github_token_input, repo_name_input, generated_folder_input, description_input],
            outputs=[result_summary, result_details]
        )
    
    return interface

# システム自動化インターフェースを作成
system_automation_interface = create_system_automation_interface()
