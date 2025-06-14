import gradio as gr
import sys
import os

# LlamaFactoryのパスを追加
llamafactory_path = '/workspaces/fastapi_django_main_live/LLaMA-Factory'
sys.path.append(llamafactory_path)

def create_llamafactory_interface():
    """LlamaFactory Gradio インターフェースを作成する"""
    try:
        # 作業ディレクトリをLlamaFactoryに変更
        original_cwd = os.getcwd()
        llamafactory_path = '/workspaces/fastapi_django_main_live/LLaMA-Factory'
        os.chdir(llamafactory_path)
        
        # 環境変数を設定
        os.environ['LLAMAFACTORY_HOME'] = llamafactory_path
        os.environ['PYTHONPATH'] = f"{llamafactory_path}:{os.environ.get('PYTHONPATH', '')}"
        
        # 必要なファイルの存在確認
        dataset_info_path = os.path.join(llamafactory_path, 'data', 'dataset_info.json')
        if not os.path.exists(dataset_info_path):
            print(f"⚠️ Dataset info file not found: {dataset_info_path}")
            os.chdir(original_cwd)
            with gr.Blocks() as missing_file_ui:
                gr.Markdown("## ⚠️ Configuration Missing")
                gr.Markdown(f"データセット情報ファイルが見つかりません: `{dataset_info_path}`")
                gr.Markdown("LlamaFactoryの初期設定が必要です。")
            return missing_file_ui
        
        print(f"✅ Found dataset info: {dataset_info_path}")
        print(f"✅ Working directory: {os.getcwd()}")
        
        # LlamaFactoryのUIを作成
        from llamafactory.webui.interface import create_ui
        ui = create_ui()
        
        # 作業ディレクトリを元に戻す
        os.chdir(original_cwd)
        return ui
        
    except ImportError as e:
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
        print(f"LlamaFactory import error: {e}")
        # フォールバック UI を作成
        with gr.Blocks() as fallback_ui:
            gr.Markdown("## ⚠️ LlamaFactory Unavailable")
            gr.Markdown("LlamaFactoryモジュールが見つかりません。")
            gr.Markdown("### 解決方法:")
            gr.Markdown("1. LlamaFactoryの依存関係をインストール")
            gr.Markdown("2. パスの設定を確認")
            gr.Code("pip install -e /workspaces/fastapi_django_main_live/LLaMA-Factory", language="bash")
        return fallback_ui
    except Exception as e:
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
        print(f"LlamaFactory UI creation error: {e}")
        with gr.Blocks() as error_ui:
            gr.Markdown("## ❌ LlamaFactory Error")
            gr.Markdown(f"エラー: {str(e)}")
            gr.Markdown("### トラブルシューティング:")
            gr.Markdown("1. LlamaFactoryのファイル構成を確認")
            gr.Markdown("2. 必要な依存関係をインストール")
            gr.Markdown("3. 権限設定を確認")
            with gr.Code():
                gr.Textbox(value=f"エラー詳細: {str(e)}", interactive=False)
        return error_ui

# メインGradio インターフェースを作成
with gr.Blocks(title="🤖 AI Development Platform", theme=gr.themes.Soft()) as gradio_interface:
    # ヘッダー
    gr.Markdown("""
    # 🤖 AI開発プラットフォーム
    
    このプラットフォームでは、LlamaFactoryを使用してLLMのファインチューニングを行うことができます。
    """)
    
    with gr.Tabs() as tabs:
        # LlamaFactory タブ
        with gr.TabItem("🦙 LlamaFactory WebUI"):
            gr.Markdown("""
            ## 🦙 LlamaFactory WebUI
            
            LLM（Large Language Models）のファインチューニングを行うためのWebインターフェースです。
            
            ### 主な機能:
            - 🎯 **モデル訓練**: カスタムデータセットでLLMを訓練
            - 📊 **データセット管理**: 訓練用データの管理・前処理
            - ⚙️ **ハイパーパラメータ調整**: 学習パラメータの最適化
            - 📈 **訓練監視**: リアルタイムでの訓練進捗確認
            """)
            
            # LlamaFactory UIを統合
            try:
                llamafactory_ui = create_llamafactory_interface()
                if llamafactory_ui:
                    # LlamaFactory UIを現在のタブに埋め込み
                    with gr.Group():
                        gr.Markdown("### 🔧 LlamaFactory コントロールパネル")
                        llamafactory_ui.render()
            except Exception as e:
                gr.Markdown(f"### ❌ LlamaFactory 読み込みエラー\n\n```\n{str(e)}\n```")
        
        # 情報タブ
        with gr.TabItem("ℹ️ システム情報"):
            gr.Markdown("""
            ## 📋 システム情報
            
            ### 🔧 利用可能な機能:
            - **LlamaFactory**: LLMファインチューニング
            - **OpenInterpreter**: コード実行・解釈
            - **AutoPrompt**: プロンプト自動最適化
            - **BabyAGI**: 自律AIエージェント
            
            ### 🚀 クイックスタート:
            1. 左側の「LlamaFactory WebUI」タブを選択
            2. データセットを準備・アップロード
            3. モデルとパラメータを設定
            4. 訓練を開始
            
            ### 📞 サポート:
            - 📖 ドキュメント: `/docs/` フォルダ
            - 🐛 問題報告: GitHub Issues
            """)
            
            # システム状態表示
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### 🔍 システム状態")
                    
                    # 動的にシステム情報を取得
                    def get_system_info():
                        llamafactory_path = '/workspaces/fastapi_django_main_live/LLaMA-Factory'
                        dataset_info_path = os.path.join(llamafactory_path, 'data', 'dataset_info.json')
                        
                        return f"""
                        - **Python Version**: {sys.version.split()[0]}
                        - **Current Directory**: {os.getcwd()}
                        - **LlamaFactory Path**: {llamafactory_path}
                        - **Dataset Info Exists**: {"✅ Yes" if os.path.exists(dataset_info_path) else "❌ No"}
                        - **LlamaFactory Accessible**: {"✅ Yes" if os.path.exists(llamafactory_path) else "❌ No"}
                        """
                    
                    system_status = get_system_info()
                    gr.Markdown(system_status)
                    
                    # LlamaFactory セットアップボタン
                    with gr.Row():
                        setup_btn = gr.Button("🔧 LlamaFactory セットアップ確認", variant="secondary")
                        
                    setup_output = gr.Textbox(
                        label="セットアップ結果", 
                        lines=10, 
                        interactive=False,
                        visible=False
                    )
                    
                    def check_llamafactory_setup():
                        """LlamaFactoryのセットアップ状況をチェック"""
                        result = []
                        llamafactory_path = '/workspaces/fastapi_django_main_live/LLaMA-Factory'
                        
                        # 1. ディレクトリ存在確認
                        if os.path.exists(llamafactory_path):
                            result.append("✅ LlamaFactoryディレクトリが存在します")
                        else:
                            result.append("❌ LlamaFactoryディレクトリが見つかりません")
                            return "\n".join(result), gr.update(visible=True)
                        
                        # 2. dataset_info.json確認
                        dataset_info_path = os.path.join(llamafactory_path, 'data', 'dataset_info.json')
                        if os.path.exists(dataset_info_path):
                            result.append("✅ dataset_info.jsonが存在します")
                        else:
                            result.append("❌ dataset_info.jsonが見つかりません")
                        
                        # 3. 必要なディレクトリ確認
                        required_dirs = ['src', 'data', 'examples']
                        for dir_name in required_dirs:
                            dir_path = os.path.join(llamafactory_path, dir_name)
                            if os.path.exists(dir_path):
                                result.append(f"✅ {dir_name}/ ディレクトリが存在します")
                            else:
                                result.append(f"❌ {dir_name}/ ディレクトリが見つかりません")
                        
                        # 4. モジュールインポート確認
                        try:
                            sys.path.append(llamafactory_path)
                            import llamafactory
                            result.append("✅ LlamaFactoryモジュールのインポートが可能です")
                        except ImportError as e:
                            result.append(f"❌ LlamaFactoryモジュールのインポートに失敗: {e}")
                        
                        return "\n".join(result), gr.update(visible=True)
                    
                    setup_btn.click(
                        fn=check_llamafactory_setup,
                        outputs=[setup_output, setup_output]
                    )

# 自動検出システム用のメタデータ
interface_title = "🚀 AI開発プラットフォーム"
interface_description = "LlamaFactory WebUIとAI開発ツール"
