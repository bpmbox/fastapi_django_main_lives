# ContBK インターフェース統合例

## 📋 概要

`controllers/contbk_example.py` は、`contbk` フォルダーにある全てのGradioインターフェースをタブ表示で統合する例です。

## 🚀 機能

### 📝 デモ機能
- **テキスト変換**: 大文字・小文字変換、文字数カウント、逆順変換
- **計算機**: 基本的な四則演算
- **リスト生成**: テキストから番号付きリスト、ブレットリスト、チェックリストを生成

### 🔧 ContBK統合機能
- **天気予報** (`gra_09_weather.weather`)
- **フロントエンド生成** (`gra_10_frontend.frontend_generator`)
- **マルチモーダル** (`gra_11_multimodal.image_to_ui`)

## 📂 ファイル構成

```
controllers/
├── contbk_example.py          # メインの統合ダッシュボード
├── contbk_dashboard.py        # 旧バージョン（参考用）
└── example_gradio_interface.py # 初期バージョン（参考用）
```

## 🔧 使用方法

### 1. スタンドアロン実行

```bash
cd /workspaces/fastapi_django_main_live
python controllers/contbk_example.py
```

サーバーが http://0.0.0.0:7864 で起動します。

### 2. メインアプリケーションに統合

```python
# mysite/asgimain.py などで

# インポート
from controllers.contbk_example import gradio_interface as contbk_dashboard

# 既存のタブに追加
existing_interfaces = [demo, create_ui(), democ, democs, appdb]
existing_names = ["AIで開発", "FineTuning", "Chat", "仕様書から作成", "DataBase"]

# ContBKダッシュボードを追加
all_interfaces = existing_interfaces + [contbk_dashboard]
all_names = existing_names + ["🎯 ContBK ダッシュボード"]

# タブ付きインターフェースを作成
tabs = gr.TabbedInterface(all_interfaces, all_names)
```

### 3. 個別インターフェースとして使用

```python
from controllers.contbk_example import (
    create_demo_interfaces,
    load_contbk_interfaces,
    create_info_tab
)

# デモ機能のみ使用
demo_interfaces, demo_names = create_demo_interfaces()

# ContBK機能のみ使用
contbk_interfaces, contbk_names = load_contbk_interfaces()

# 情報タブのみ使用
info_tab = create_info_tab()
```

## 🎯 新しいインターフェースの追加

### ContBKフォルダーに新しいインターフェースを追加する方法

1. **新しいフォルダーを作成**
   ```
   contbk/gra_XX_mynewfeature/
   ```

2. **Pythonファイルを作成**
   ```python
   # contbk/gra_XX_mynewfeature/mynewfeature.py
   import gradio as gr
   
   def my_function(input_text):
       return f"処理結果: {input_text}"
   
   gradio_interface = gr.Interface(
       fn=my_function,
       inputs=gr.Textbox(label="入力"),
       outputs=gr.Textbox(label="出力"),
       title="新機能"
   )
   ```

3. **自動検出設定の更新**
   
   `contbk_example.py` の `stable_modules` リストに追加:
   ```python
   stable_modules = [
       ("gra_09_weather.weather", "🌤️ 天気予報"),
       ("gra_10_frontend.frontend_generator", "🎨 フロントエンド生成"),
       ("gra_11_multimodal.image_to_ui", "🖼️ マルチモーダル"),
       ("gra_XX_mynewfeature.mynewfeature", "🆕 新機能"),  # 追加
   ]
   ```

## 🔍 トラブルシューティング

### よくある問題

1. **ModuleNotFoundError: No module named 'mysite'**
   - 原因: ContBKの一部モジュールがmysiteパッケージに依存
   - 解決: `stable_modules` リストから該当モジュールを除外

2. **Port already in use**
   - 原因: 指定したポートが既に使用中
   - 解決: 別のポートを指定 (`server_port=7865` など)

3. **gradio_interface not found**
   - 原因: モジュールに `gradio_interface` 変数が定義されていない
   - 解決: モジュール内で正しく `gradio_interface` を定義

### デバッグ方法

```python
# モジュールのインポートテスト
python -c "
import sys
sys.path.insert(0, '/workspaces/fastapi_django_main_live/contbk')
import gra_XX_yourmodule.yourfile
print(hasattr(gra_XX_yourmodule.yourfile, 'gradio_interface'))
"
```

## 📊 パフォーマンス

- **起動時間**: 約5-10秒（ContBKモジュールの読み込み含む）
- **メモリ使用量**: 基本的な機能で約200MB
- **同時接続**: Gradioの標準制限に従う

## 🔗 関連ファイル

- `contbk/` - 統合対象のインターフェース群
- `mysite/routers/gradio.py` - 既存の動的読み込みシステム
- `app.py` - メインアプリケーション
- `FOLDER_STRUCTURE.md` - プロジェクト全体の構成

## 📝 ライセンス

このプロジェクトのライセンスに従います。
