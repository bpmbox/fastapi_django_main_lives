#!/usr/bin/env python3
"""
RPA + AI画像解析デバッグシステム (DI統合版)
================================

RPAでキャプチャした画像をAIが解析してエラーを特定・解決策を提案
依存性注入パターンでデータベース処理を抽象化
"""

import gradio as gr
import asyncio
import base64
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# RPAモジュールのインポート
sys.path.append('/workspaces/fastapi_django_main_live')
try:
    from contbk.gra_12_rpa.rpa_automation import RPAManager
    RPA_AVAILABLE = True
except ImportError:
    RPA_AVAILABLE = False
    print("⚠️ RPA機能が利用できません")

# DIレイヤーのインポート
try:
    from controllers.gra_03_programfromdocs.database_di_layer import (
        RepositoryFactory, 
        DebugHistoryService,
        DebugRecord
    )
    DI_AVAILABLE = True
except ImportError:
    DI_AVAILABLE = False
    print("⚠️ DI機能が利用できません")

class RPADebugSystem:
    """RPA + AI デバッグシステム (DI統合版)"""
    
    def __init__(self, history_service: DebugHistoryService = None, repository_type: str = "sqlite"):
        """
        依存性注入でデータベースサービスを設定
        
        Args:
            history_service: 履歴管理サービス（DIパターン）
            repository_type: リポジトリタイプ ("sqlite" または "json")
        """
        # RPA Manager初期化
        if RPA_AVAILABLE:
            self.rpa_manager = RPAManager()
        else:
            self.rpa_manager = None
        
        # DI: 履歴管理サービス注入
        if history_service:
            self.history_service = history_service
            self.debug_history = []  # レガシー互換性
        elif DI_AVAILABLE:
            self.history_service = RepositoryFactory.create_service(repository_type)
            self.debug_history = []  # レガシー互換性
        else:
            # フォールバック: レガシー実装
            self.debug_history = []
            self.history_service = None
        
        # キャプチャディレクトリ設定
        self.capture_dir = Path("/workspaces/fastapi_django_main_live/docs/images/debug_captures")
        self.capture_dir.mkdir(parents=True, exist_ok=True)
    
    async def capture_and_analyze(self, url: str, description: str = "", selector: str = None) -> tuple:
        """
        RPAでキャプチャして画像解析を実行（DI統合版）
        
        Args:
            url: 対象URL
            description: 問題の説明
            selector: CSS セレクター（オプション）
            
        Returns:
            (PIL.Image, 解析結果テキスト, キャプチャファイルパス, record_id)
        """
        if not self.rpa_manager:
            return None, "❌ RPA機能が利用できません", "", None
        
        try:
            # 🤖 RPAでスクリーンショット取得
            img, capture_message = await self.rpa_manager.capture_screenshot(
                url=url,
                selector=selector,
                wait_time=5  # エラー画面の読み込みを待つため少し長めに
            )
            
            if not img:
                return None, f"❌ キャプチャ失敗: {capture_message}", "", None
            
            # 💾 キャプチャ画像を保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            selector_suffix = f"_selector" if selector else "_fullpage"
            filename = f"debug_capture_{timestamp}{selector_suffix}.png"
            capture_path = self.capture_dir / filename
            img.save(capture_path)
            
            # 🧠 AI解析用のプロンプトを生成
            analysis_prompt = self._generate_analysis_prompt(description, selector)
            
            # 📊 DI: 履歴管理サービス経由で保存
            record_id = None
            if self.history_service:
                try:
                    record_id = await self.history_service.save_debug_session(
                        url=url,
                        description=description,
                        selector=selector,
                        capture_path=str(capture_path),
                        analysis_prompt=analysis_prompt
                    )
                    print(f"✅ DI: デバッグ記録保存 (ID: {record_id})")
                except Exception as e:
                    print(f"⚠️ DI保存エラー: {e}")
            else:
                # フォールバック: レガシー実装
                debug_record = {
                    "timestamp": datetime.now().isoformat(),
                    "url": url,
                    "description": description,
                    "selector": selector,
                    "capture_path": str(capture_path),
                    "analysis_prompt": analysis_prompt
                }
                self.debug_history.append(debug_record)
                print("⚠️ レガシー履歴モードで保存")
            
            return img, analysis_prompt, str(capture_path), record_id
            
        except Exception as e:
            error_msg = f"❌ キャプチャ・解析エラー: {str(e)}"
            return None, error_msg, "", None
    
    async def update_analysis_result(self, record_id: int, analysis_result: str) -> bool:
        """
        AI解析結果を記録に反映（DI統合）
        
        Args:
            record_id: 記録ID
            analysis_result: AI解析結果
            
        Returns:
            更新成功フラグ
        """
        if self.history_service and record_id:
            try:
                success = await self.history_service.complete_analysis(record_id, analysis_result)
                if success:
                    print(f"✅ DI: 解析結果更新完了 (ID: {record_id})")
                return success
            except Exception as e:
                print(f"⚠️ DI更新エラー: {e}")
                return False
        return False
    
    async def search_debug_history(self, query: str) -> str:
        """
        デバッグ履歴検索（DI統合）
        
        Args:
            query: 検索クエリ
            
        Returns:
            フォーマットされた検索結果
        """
        if self.history_service:
            try:
                records = await self.history_service.search_debug_history(query)
                if not records:
                    return f"🔍 '{query}' に該当する記録が見つかりませんでした"
                
                formatted = f"🔍 **検索結果: '{query}'**\n\n"
                for i, record in enumerate(records[:10], 1):
                    timestamp = record.timestamp[:16].replace("T", " ")
                    status_emoji = "✅" if record.status == "analyzed" else "📸"
                    
                    formatted += f"**#{i}** {status_emoji} - {timestamp}\n"
                    formatted += f"🌐 URL: {record.url[:50]}...\n"
                    formatted += f"📝 説明: {record.description[:100]}...\n\n"
                
                return formatted
            except Exception as e:
                return f"❌ 検索エラー: {str(e)}"
        else:
            # フォールバック: レガシー検索
            return self._legacy_search(query)
    
    async def get_debug_history(self) -> str:
        """デバッグ履歴をフォーマット（DI統合版）"""
        if self.history_service:
            try:
                return await self.history_service.get_debug_history_formatted(10)
            except Exception as e:
                print(f"⚠️ DI履歴取得エラー: {e}")
                return f"❌ 履歴取得エラー: {str(e)}"
        else:
            # フォールバック: レガシー実装
            return self._get_legacy_history()
    
    async def get_url_statistics(self, url: str) -> str:
        """URL別統計情報取得（DI統合）"""
        if self.history_service:
            try:
                stats = await self.history_service.get_url_statistics(url)
                
                formatted = f"📊 **URL統計: {url[:50]}...**\n\n"
                formatted += f"📸 総キャプチャ数: {stats['total_captures']}\n"
                formatted += f"🔍 解析済み: {stats['analyzed_captures']}\n"
                formatted += f"📈 解析率: {stats['analysis_rate']:.1%}\n"
                if stats['last_capture']:
                    last_time = stats['last_capture'][:16].replace("T", " ")
                    formatted += f"🕒 最新キャプチャ: {last_time}\n"
                
                return formatted
            except Exception as e:
                return f"❌ 統計取得エラー: {str(e)}"
        else:
            return "⚠️ 統計機能は DI モードでのみ利用可能です"

    def _legacy_search(self, query: str) -> str:
        """レガシーモードでの検索"""
        if not self.debug_history:
            return f"🔍 '{query}' に該当する記録が見つかりませんでした（レガシーモード）"
        
        query_lower = query.lower()
        matches = []
        
        for record in self.debug_history:
            if (query_lower in record.get('description', '').lower() or
                query_lower in record.get('url', '').lower()):
                matches.append(record)
        
        if not matches:
            return f"🔍 '{query}' に該当する記録が見つかりませんでした（レガシーモード）"
        
        formatted = f"🔍 **検索結果: '{query}' (レガシーモード)**\n\n"
        for i, record in enumerate(matches[:5], 1):
            timestamp = record["timestamp"][:16].replace("T", " ")
            formatted += f"**#{i}** 📸 - {timestamp}\n"
            formatted += f"🌐 URL: {record['url'][:50]}...\n"
            formatted += f"📝 説明: {record['description'][:100]}...\n\n"
        
        return formatted
    
    def _get_legacy_history(self) -> str:
        """レガシーモードでの履歴取得"""
        if not self.debug_history:
            return "📭 デバッグ履歴はありません（レガシーモード）"
        
        formatted = "📋 **デバッグ履歴（レガシーモード）**\n\n"
        
        for i, record in enumerate(reversed(self.debug_history[-10:]), 1):
            timestamp = record["timestamp"][:16].replace("T", " ")
            url_short = record["url"][:50] + "..." if len(record["url"]) > 50 else record["url"]
            
            formatted += f"**#{i}** - {timestamp}\n"
            formatted += f"🌐 URL: {url_short}\n"
            formatted += f"📝 説明: {record['description'][:100]}...\n"
            formatted += f"📸 キャプチャ: {Path(record['capture_path']).name}\n\n"
        
        return formatted

    def _generate_analysis_prompt(self, description: str, selector: str = None) -> str:
        """AI解析用プロンプトを生成"""
        
        base_prompt = """
🔍 **RPA キャプチャ画像解析 - Gradio アプリケーション専用**

この画像はGradioベースのWebアプリケーションのキャプチャです。以下の点を重点的に分析してください：

## 📋 **Gradio特有の解析項目**
1. **エラーメッセージの特定**
   - Gradio エラーダイアログ
   - Python トレースバック表示
   - 赤いエラーバナー
   - "Error" や "Exception" の文字

2. **Gradio UI要素の状態**
   - タブの選択状態とエラー表示
   - ボタンの有効/無効状態
   - 入力フィールドのエラー状態
   - プログレスバーの状態

3. **アプリケーション状態**
   - "Running on..." メッセージ
   - 読み込み中インジケーター
   - 接続エラーメッセージ
   - JavaScript console エラー

4. **タブとインターフェース**
   - どのタブが選択されているか
   - エラーが発生しているタブ
   - インターフェースの表示状態

5. **改善提案**
   - Gradio特有のエラー対処法
   - Python/FastAPI の修正点
   - 環境設定の問題"""
        
        if selector:
            base_prompt += f"""

## 🎯 **セレクター指定キャプチャ**
**対象セレクター**: `{selector}`
この特定の要素に焦点を当てて、その部分の問題を詳細に分析してください。
"""
        
        if description:
            base_prompt += f"""

## 👤 **ユーザー報告内容**
**問題の詳細**: {description}
上記の説明を踏まえて、特にその点に関連する問題を重点的に分析してください。
"""
        
        base_prompt += """

## 📊 **出力形式**
- 🚨 **問題の種類**: Gradioエラー / Pythonエラー / UI問題 / 接続問題
- 🔴 **重要度**: 高 / 中 / 低
- ⭐ **難易度**: 簡単 / 中程度 / 困難
- ⏱️ **推定解決時間**: 具体的な時間
- 🛠️ **修正手順**: ステップバイステップの説明
- 💡 **根本原因**: 技術的な原因の特定

Gradioアプリケーションに特化した実用的な分析をお願いします！
"""
        
        return base_prompt

def create_rpa_debug_interface():
    """RPA + AI デバッグシステムのGradioインターフェース（DI統合版）"""
    
    # DI: デフォルトでSQLiteを使用、フォールバックでJSONまたはレガシー
    debug_system = RPADebugSystem(repository_type="sqlite")
    
    def capture_and_analyze_wrapper(url, description, selector=None):
        """キャプチャ・解析のラッパー関数（DI対応）"""
        if not url:
            return None, "❌ URLを入力してください", "", "", ""
        
        try:
            # 非同期関数を同期実行
            img, analysis_result, capture_path, record_id = asyncio.run(
                debug_system.capture_and_analyze(url, description, selector)
            )
            
            # DI対応の履歴取得
            history = asyncio.run(debug_system.get_debug_history())
            
            # record_id情報を追加
            record_info = f"Record ID: {record_id}" if record_id else "レガシーモード"
            
            return img, analysis_result, capture_path, record_info, history
            
        except Exception as e:
            error_msg = f"❌ エラー: {str(e)}"
            return None, error_msg, "", "", asyncio.run(debug_system.get_debug_history())
    
    def capture_fullpage_wrapper(url, description):
        """全画面キャプチャのラッパー"""
        return capture_and_analyze_wrapper(url, description, None)
    
    def capture_selector_wrapper(url, description, selector):
        """セレクター指定キャプチャのラッパー"""
        if not selector.strip():
            return None, "❌ セレクターを入力してください", "", "", ""
        return capture_and_analyze_wrapper(url, description, selector)
    
    def search_history_wrapper(query):
        """履歴検索のラッパー（DI対応）"""
        if not query.strip():
            return "🔍 検索キーワードを入力してください"
        
        try:
            return asyncio.run(debug_system.search_debug_history(query))
        except Exception as e:
            return f"❌ 検索エラー: {str(e)}"
    
    def get_url_stats_wrapper(url):
        """URL統計のラッパー（DI対応）"""
        if not url.strip():
            return "📊 URLを入力してください"
        
        try:
            return asyncio.run(debug_system.get_url_statistics(url))
        except Exception as e:
            return f"❌ 統計取得エラー: {str(e)}"
    
    with gr.Blocks(title="🔍 RPA + AI デバッグ", theme="soft") as interface:
        gr.Markdown("# 🔍 RPA + AI 画像解析デバッグシステム (DI統合版)")
        gr.Markdown("""
        **RPAでキャプチャ → AI解析 → エラー特定・解決策提案**の統合システム
        
        **🔧 DI (依存性注入)**: データベース処理を抽象化し、SQLite/JSONの切り替えが可能
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # キャプチャ設定
                gr.Markdown("## 📸 キャプチャ設定")
                
                url_input = gr.Textbox(
                    label="🌐 対象URL",
                    placeholder="https://example.com または http://localhost:7860",
                    value="https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev/"
                )
                
                selector_input = gr.Textbox(
                    label="🎯 セレクター (オプション)",
                    placeholder="例: .gradio-container, #app, .error-message, button[data-testid='tab-button']",
                    info="特定の要素のみキャプチャしたい場合はCSSセレクターを入力"
                )
                
                description_input = gr.Textbox(
                    label="📝 問題・状況の説明",
                    placeholder="どのような問題が発生していますか？（エラーメッセージ、動作不良など）",
                    lines=3
                )
                
                with gr.Row():
                    capture_btn = gr.Button("📸 全画面キャプチャ", variant="primary")
                    capture_selector_btn = gr.Button("🎯 セレクター指定キャプチャ", variant="secondary")
                
                # 結果表示
                gr.Markdown("## 🎯 解析結果")
                analysis_result = gr.Textbox(
                    label="AI解析結果",
                    lines=15,
                    interactive=False
                )
                
                capture_info = gr.Textbox(
                    label="キャプチャ情報",
                    lines=2,
                    interactive=False
                )
            
            with gr.Column(scale=3):
                # キャプチャ画像表示
                gr.Markdown("## 🖼️ キャプチャ画像")
                captured_image = gr.Image(
                    label="キャプチャ画像",
                    height=400
                )
                
                # DI機能: 検索とURL統計
                gr.Markdown("## 🔍 DI機能: 履歴検索・統計")
                
                with gr.Row():
                    search_query = gr.Textbox(
                        label="履歴検索",
                        placeholder="検索キーワード（URL、説明、エラー内容など）"
                    )
                    search_btn = gr.Button("🔍 検索", variant="secondary")
                
                with gr.Row():
                    stats_url = gr.Textbox(
                        label="URL統計",
                        placeholder="統計を取得したいURL"
                    )
                    stats_btn = gr.Button("📊 統計", variant="secondary")
                
                search_result = gr.Markdown(
                    label="検索・統計結果",
                    value="検索結果・統計情報がここに表示されます"
                )
                
                # デバッグ履歴
                gr.Markdown("## 📋 デバッグ履歴")
                debug_history = gr.Markdown(
                    value=asyncio.run(debug_system.get_debug_history()),
                    label="最近のデバッグ履歴"
                )
        
        # 使用方法の説明
        with gr.Accordion("🔗 使用方法・Tips", open=False):
            gr.Markdown("""
            ### 🚀 基本的な使用方法
            
            1. **URL入力**: 問題が発生している画面のURLを入力
            2. **セレクター指定**: 特定の要素をキャプチャしたい場合はCSSセレクターを入力
            3. **状況説明**: エラーや問題の詳細を記述
            4. **キャプチャ実行**: 全画面またはセレクター指定でキャプチャ
            5. **AI解析**: 画像を元に問題特定・解決策を確認
            
            ### 🔧 新機能: DI統合
            
            - **履歴検索**: キーワードでデバッグ履歴を検索
            - **URL統計**: 特定URLのキャプチャ統計情報
            - **SQLiteDB**: 永続化されたデバッグ記録
            - **レガシー対応**: JSONファイルバックアップ
            
            ### 🎯 Gradio用セレクター例
            
            - **特定のタブ**: `button[data-testid="tab-button"]:nth-child(2)`
            - **エラーメッセージ**: `.error, .gr-error, .gradio-error`
            - **入力フィールド**: `.gr-textbox, input[type="text"]`
            - **ボタン**: `.gr-button, button`
            - **メインコンテナ**: `.gradio-container, #app`
            - **特定のコンポーネント**: `#component-123`
            
            ### 💡 効果的な活用Tips
            
            - **詳細な説明**: 問題の症状を具体的に記述
            - **エラーメッセージ**: 表示されているエラー文を記載
            - **操作手順**: 問題発生までの操作を説明
            - **期待結果**: 本来どうなるべきかを明記
            
            ### 🎯 対応可能な問題例
            
            - Webアプリケーションのエラー画面
            - ダッシュボードの表示不良
            - フォームの送信エラー
            - API接続の問題
            - UIの動作不良
            """)
        
        # イベントハンドラー
        capture_btn.click(
            fn=capture_fullpage_wrapper,
            inputs=[url_input, description_input],
            outputs=[captured_image, analysis_result, capture_info, debug_history]
        )
        
        capture_selector_btn.click(
            fn=capture_selector_wrapper,
            inputs=[url_input, description_input, selector_input],
            outputs=[captured_image, analysis_result, capture_info, debug_history]
        )
        
        # DI機能のイベントハンドラー
        search_btn.click(
            fn=search_history_wrapper,
            inputs=[search_query],
            outputs=[search_result]
        )
        
        stats_btn.click(
            fn=get_url_stats_wrapper,
            inputs=[stats_url],
            outputs=[search_result]
        )
    
    return interface
