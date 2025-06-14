#!/usr/bin/env python3
"""
Hugging Face リポジトリ内容取得クライアント
"""
import os
import requests
from huggingface_hub import HfApi, Repository, list_repo_files
from huggingface_hub import hf_hub_download, snapshot_download
from typing import List, Dict, Optional
import json
from datetime import datetime

class HuggingFaceRepoClient:
    """Hugging Face リポジトリの内容を取得するクライアント"""
    
    def __init__(self, token: Optional[str] = None):
        """
        初期化
        
        Args:
            token: Hugging Face API トークン（環境変数 HF_TOKEN から取得）
        """
        self.token = token or os.environ.get("HF_TOKEN")
        self.api = HfApi(token=self.token)
        
    def get_repo_info(self, repo_id: str, repo_type: str = "space") -> Dict:
        """
        リポジトリの基本情報を取得
        
        Args:
            repo_id: リポジトリID (例: "kenken999/fastapi_django_main_live")
            repo_type: リポジトリタイプ ("space", "model", "dataset")
            
        Returns:
            リポジトリ情報の辞書
        """
        try:
            if repo_type == "space":
                repo_info = self.api.space_info(repo_id)
            elif repo_type == "model":
                repo_info = self.api.model_info(repo_id)
            elif repo_type == "dataset":
                repo_info = self.api.dataset_info(repo_id)
            else:
                raise ValueError("repo_type must be 'space', 'model', or 'dataset'")
                
            return {
                "id": repo_info.id,
                "author": repo_info.author,
                "sha": getattr(repo_info, 'sha', 'N/A'),
                "created_at": str(repo_info.created_at) if hasattr(repo_info, 'created_at') else 'N/A',
                "last_modified": str(repo_info.last_modified) if hasattr(repo_info, 'last_modified') else 'N/A',
                "private": getattr(repo_info, 'private', False),
                "tags": getattr(repo_info, 'tags', []),
                "siblings": [f.rfilename for f in getattr(repo_info, 'siblings', [])],
                "downloads": getattr(repo_info, 'downloads', 0),
                "likes": getattr(repo_info, 'likes', 0),
            }
        except Exception as e:
            return {"error": str(e)}
    
    def list_files(self, repo_id: str, repo_type: str = "space") -> List[str]:
        """
        リポジトリ内のファイル一覧を取得
        
        Args:
            repo_id: リポジトリID
            repo_type: リポジトリタイプ
            
        Returns:
            ファイルパスのリスト
        """
        try:
            files = list_repo_files(repo_id, repo_type=repo_type, token=self.token)
            return list(files)
        except Exception as e:
            print(f"ファイル一覧取得エラー: {e}")
            return []
    
    def download_file(self, repo_id: str, filename: str, repo_type: str = "space") -> Optional[str]:
        """
        リポジトリから特定のファイルをダウンロード
        
        Args:
            repo_id: リポジトリID
            filename: ダウンロードするファイル名
            repo_type: リポジトリタイプ
            
        Returns:
            ダウンロードしたファイルのローカルパス
        """
        try:
            file_path = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                repo_type=repo_type,
                token=self.token
            )
            return file_path
        except Exception as e:
            print(f"ファイルダウンロードエラー: {e}")
            return None
    
    def read_file_content(self, repo_id: str, filename: str, repo_type: str = "space") -> Optional[str]:
        """
        リポジトリから特定のファイルの内容を読み取り
        
        Args:
            repo_id: リポジトリID
            filename: 読み取るファイル名
            repo_type: リポジトリタイプ
            
        Returns:
            ファイルの内容（テキスト）
        """
        try:
            # ファイルをダウンロード
            file_path = self.download_file(repo_id, filename, repo_type)
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return None
        except Exception as e:
            print(f"ファイル内容読み取りエラー: {e}")
            return None
    
    def clone_repo(self, repo_id: str, local_dir: str, repo_type: str = "space") -> bool:
        """
        リポジトリ全体をローカルにクローン
        
        Args:
            repo_id: リポジトリID
            local_dir: ローカルディレクトリパス
            repo_type: リポジトリタイプ
            
        Returns:
            成功したかどうか
        """
        try:
            snapshot_download(
                repo_id=repo_id,
                local_dir=local_dir,
                repo_type=repo_type,
                token=self.token
            )
            return True
        except Exception as e:
            print(f"リポジトリクローンエラー: {e}")
            return False
    
    def get_commit_history(self, repo_id: str, repo_type: str = "space") -> List[Dict]:
        """
        リポジトリのコミット履歴を取得
        
        Args:
            repo_id: リポジトリID
            repo_type: リポジトリタイプ
            
        Returns:
            コミット履歴のリスト
        """
        try:
            commits = self.api.list_repo_commits(repo_id, repo_type=repo_type)
            return [
                {
                    "commit_id": commit.commit_id,
                    "title": commit.title,
                    "message": getattr(commit, 'message', ''),
                    "date": str(commit.date) if hasattr(commit, 'date') else 'N/A',
                    "author": getattr(commit, 'author', 'Unknown'),
                }
                for commit in commits[:10]  # 最新10件
            ]
        except Exception as e:
            print(f"コミット履歴取得エラー: {e}")
            return []

def main():
    """メイン関数 - 使用例"""
    
    # 現在のHugging Face Spacesリポジトリの情報を取得
    client = HuggingFaceRepoClient()
    repo_id = "kenken999/fastapi_django_main_live"
    
    print("🚀 Hugging Face リポジトリ情報取得開始")
    print(f"📂 対象リポジトリ: {repo_id}")
    print("-" * 50)
    
    # 1. リポジトリ基本情報
    print("📋 基本情報:")
    repo_info = client.get_repo_info(repo_id, "space")
    if "error" not in repo_info:
        for key, value in repo_info.items():
            print(f"  {key}: {value}")
    else:
        print(f"  エラー: {repo_info['error']}")
    
    print("\n" + "-" * 50)
    
    # 2. ファイル一覧
    print("📁 ファイル一覧:")
    files = client.list_files(repo_id, "space")
    if files:
        for i, file in enumerate(files[:10]):  # 最初の10ファイル
            print(f"  {i+1:2d}. {file}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more files")
    else:
        print("  ファイルが見つかりません")
    
    print("\n" + "-" * 50)
    
    # 3. 特定ファイルの内容読み取り
    print("📄 README.md の内容:")
    readme_content = client.read_file_content(repo_id, "README.md", "space")
    if readme_content:
        # 最初の500文字を表示
        print(readme_content[:500] + "..." if len(readme_content) > 500 else readme_content)
    else:
        print("  README.md が見つかりません")
    
    print("\n" + "-" * 50)
    
    # 4. コミット履歴
    print("📜 最新コミット履歴:")
    commits = client.get_commit_history(repo_id, "space")
    if commits:
        for i, commit in enumerate(commits[:5]):  # 最新5件
            print(f"  {i+1}. {commit['title']} ({commit['date'][:10]})")
    else:
        print("  コミット履歴が取得できません")
    
    print("\n" + "=" * 50)
    print("✅ 取得完了")

if __name__ == "__main__":
    main()
