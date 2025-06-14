#!/usr/bin/env python3
"""
承認システム手動テスト
承認待ちキューに手動でエントリを追加し、承認フローをテストします
"""

import sqlite3
import sys
import os
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.append('/workspaces/fastapi_django_main_live')

class ApprovalTestDemo:
    """承認システムテストデモ"""
    
    def __init__(self):
        self.db_path = "/workspaces/fastapi_django_main_live/prompts.db"
    
    def add_test_approval_item(self, title, description, priority=5):
        """テスト用の承認待ちアイテムを追加"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO approval_queue (
                    github_issue_number, github_repo, issue_title, issue_body,
                    requester, approval_status, priority, estimated_time,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                999,  # ダミーのISSUE番号
                "miyataken999/fastapi_django_main_live",
                title,
                description,
                "manual_test_user",
                "pending_review",
                priority,
                "30-60分"
            ))
            
            new_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ 承認待ちアイテム追加: ID {new_id} - {title}")
            return new_id
            
        except Exception as e:
            print(f"❌ 承認待ちアイテム追加エラー: {e}")
            return None
    
    def show_approval_queue(self):
        """承認待ちキューを表示"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, issue_title, approval_status, priority, 
                       requester, estimated_time, created_at
                FROM approval_queue 
                ORDER BY priority DESC, created_at ASC
            ''')
            
            items = cursor.fetchall()
            conn.close()
            
            print("\n📋 承認待ちキュー:")
            print("=" * 80)
            
            if not items:
                print("  承認待ちの項目はありません")
                return []
            
            for item in items:
                id, title, status, priority, requester, est_time, created = item
                created_time = created[:16] if created else 'Unknown'
                
                status_icon = {
                    'pending_review': '⏳',
                    'approved': '✅',
                    'rejected': '❌',
                    'in_progress': '🔄',
                    'completed': '🎉',
                    'failed': '💥'
                }.get(status, '❓')
                
                priority_str = f"P{priority}"
                
                print(f"{status_icon} ID:{id:2d} | {priority_str} | {title[:40]:40s} | {requester:15s} | {created_time}")
                print(f"     ステータス: {status} | 見積: {est_time}")
                print("-" * 80)
            
            print(f"合計: {len(items)}件")
            return items
            
        except Exception as e:
            print(f"❌ 承認待ちキュー取得エラー: {e}")
            return []
    
    def approve_item(self, approval_id, reviewer_name="manual_reviewer"):
        """承認待ちアイテムを承認"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # アイテムの存在確認
            cursor.execute('SELECT issue_title, approval_status FROM approval_queue WHERE id = ?', (approval_id,))
            result = cursor.fetchone()
            
            if not result:
                print(f"❌ ID {approval_id} のアイテムが見つかりません")
                conn.close()
                return False
            
            title, current_status = result
            
            if current_status != 'pending_review':
                print(f"⚠️ ID {approval_id} は既に {current_status} 状態です")
                conn.close()
                return False
            
            # 承認実行
            cursor.execute('''
                UPDATE approval_queue 
                SET approval_status = ?, approved_by = ?, approved_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', ('approved', reviewer_name, approval_id))
            
            conn.commit()
            conn.close()
            
            print(f"✅ ID {approval_id} を承認しました: {title}")
            print(f"   承認者: {reviewer_name}")
            print(f"   承認日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True
            
        except Exception as e:
            print(f"❌ 承認エラー: {e}")
            return False
    
    def reject_item(self, approval_id, reason="テスト拒否", reviewer_name="manual_reviewer"):
        """承認待ちアイテムを拒否"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE approval_queue 
                SET approval_status = ?, approved_by = ?, reviewer_notes = ?,
                    approved_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', ('rejected', reviewer_name, reason, approval_id))
            
            if cursor.rowcount == 0:
                print(f"❌ ID {approval_id} のアイテムが見つかりません")
                conn.close()
                return False
            
            conn.commit()
            conn.close()
            
            print(f"❌ ID {approval_id} を拒否しました")
            print(f"   理由: {reason}")
            print(f"   拒否者: {reviewer_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ 拒否エラー: {e}")
            return False
    
    def create_sample_approval_items(self):
        """サンプル承認待ちアイテムを作成"""
        sample_items = [
            {
                "title": "🧪 テスト: 簡単な計算機システム",
                "description": """Webベースの計算機アプリケーション作成要求

要件:
- HTML/CSS/JavaScript
- 四則演算機能
- レスポンシブデザイン
- ローカルで動作

優先度: 高""",
                "priority": 8
            },
            {
                "title": "🧪 テスト: ToDoリスト管理システム",
                "description": """タスク管理システムの作成要求

要件:
- React.js または Vue.js
- CRUD操作
- ローカルストレージ
- モダンUI

優先度: 中""",
                "priority": 5
            },
            {
                "title": "🧪 テスト: API バックエンドシステム",
                "description": """RESTful APIの作成要求

要件:
- FastAPI フレームワーク
- データベース連携
- 認証機能
- Swagger UI

優先度: 高""",
                "priority": 7
            }
        ]
        
        print("\n🚀 サンプル承認待ちアイテムを追加します...")
        
        added_ids = []
        for item in sample_items:
            item_id = self.add_test_approval_item(
                item["title"],
                item["description"],
                item["priority"]
            )
            if item_id:
                added_ids.append(item_id)
        
        print(f"\n✅ {len(added_ids)}個の承認待ちアイテムを追加しました")
        return added_ids

def main():
    """メイン実行"""
    print("🔄 承認システム手動テストデモ")
    print("=" * 60)
    
    demo = ApprovalTestDemo()
    
    while True:
        # 現在の承認待ちキューを表示
        items = demo.show_approval_queue()
        
        print("\n📝 実行したい操作を選択してください:")
        print("1. サンプル承認待ちアイテムを追加")
        print("2. 承認待ちアイテムを承認する")
        print("3. 承認待ちアイテムを拒否する")
        print("4. 承認待ちキューのみ表示")
        print("5. 終了")
        
        choice = input("\n選択 (1-5): ").strip()
        
        if choice == "1":
            added_ids = demo.create_sample_approval_items()
            if added_ids:
                print(f"\n💡 追加されたアイテムのID: {added_ids}")
                print("   これらのIDを使って承認テストができます")
        
        elif choice == "2":
            if not items:
                print("❌ 承認待ちのアイテムがありません")
                continue
                
            item_id = input("承認するアイテムのID: ").strip()
            try:
                item_id = int(item_id)
                demo.approve_item(item_id)
            except ValueError:
                print("❌ 無効なID形式です")
        
        elif choice == "3":
            if not items:
                print("❌ 承認待ちのアイテムがありません")
                continue
                
            item_id = input("拒否するアイテムのID: ").strip()
            reason = input("拒否理由（省略可）: ").strip() or "手動テスト拒否"
            try:
                item_id = int(item_id)
                demo.reject_item(item_id, reason)
            except ValueError:
                print("❌ 無効なID形式です")
        
        elif choice == "4":
            # 承認待ちキューの表示のみ（既に上で実行済み）
            pass
        
        elif choice == "5":
            print("👋 承認システムテストを終了します")
            break
        
        else:
            print("❌ 無効な選択です")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    main()
