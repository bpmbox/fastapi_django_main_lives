#!/usr/bin/env python3
"""
データベース修正スクリプト
"""
import sqlite3
import os

def fix_database():
    db_path = "/workspaces/fastapi_django_main_live/prompts.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 既存のテーブル構造を確認
        cursor.execute("PRAGMA table_info(prompts)")
        columns = cursor.fetchall()
        print("現在のテーブル構造:")
        for col in columns:
            print(f"  {col}")
        
        # categoryカラムが存在するかチェック
        column_names = [col[1] for col in columns]
        
        if 'category' not in column_names:
            print("\ncategoryカラムが見つかりません。追加します...")
            cursor.execute('ALTER TABLE prompts ADD COLUMN category TEXT DEFAULT "general"')
            conn.commit()
            print("categoryカラムを追加しました！")
            
            # 更新後の構造を確認
            cursor.execute("PRAGMA table_info(prompts)")
            new_columns = cursor.fetchall()
            print("\n更新後のテーブル構造:")
            for col in new_columns:
                print(f"  {col}")
        else:
            print("\ncategoryカラムは既に存在します。")
        
        # テストレコード数を確認
        cursor.execute("SELECT COUNT(*) FROM prompts")
        count = cursor.fetchone()[0]
        print(f"\n現在のプロンプト数: {count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"エラー: {e}")
        return False

if __name__ == "__main__":
    fix_database()
