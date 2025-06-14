# 🎯 ContBK統合システム - 使用方法

## 🚀 クイックスタート

### 1. メインアプリケーションで使用
```bash
cd /workspaces/fastapi_django_main_live
python3 app.py
```
**結果**: 11個の美しい絵文字タイトル付きインターフェースが自動表示

### 2. ContBKダッシュボード単体起動
```bash
cd /workspaces/fastapi_django_main_live
python3 controllers/contbk_example.py
```
**結果**: ポート7864で7タブ統合ダッシュボード起動

### 3. 最終デモンストレーション
```bash
cd /workspaces/fastapi_django_main_live
python3 controllers/final_demo.py
```
**結果**: 完全なシステムテストとデモンストレーション

## 📊 統合済みインターフェース

### メインシステム (11個)
1. 📊 **ContBK 統合** - ContBKインターフェース統合管理
2. 🎯 **ContBK ダッシュボード** - 7タブ統合ダッシュボード
3. 🔧 **サンプル** - 動的ロード例
4. 🚀 **AI開発プラットフォーム** - LLaMA-Factory統合
5. 📄 **ドキュメント生成** - AI文書作成
6. 🌐 **HTML表示** - ウェブコンテンツ表示
7. 💾 **プロンプト管理システム** - プロンプトDB管理
8. 📁 **ファイル管理** - ファイル操作
9. 💬 **AIチャット** - 対話型AI
10. 🚗 **データベース管理** - データベース操作
11. 🤖 **Open Interpreter** - コード実行環境

### ContBKフォルダー統合 (3個)
- 🌤️ **天気予報** (`gra_09_weather`)
- 🎨 **フロントエンド生成** (`gra_10_frontend`)
- 🖼️ **マルチモーダル** (`gra_11_multimodal`)

## 🔧 カスタマイズ方法

### 新しいインターフェース追加
1. **controllers** フォルダーに配置
2. `gradio_interface` 変数を定義
3. (オプション) `interface_title` で美しいタイトル設定

```python
# controllers/my_interface.py
import gradio as gr

# カスタムタイトル (オプション)
interface_title = "🎨 マイインターフェース"

# 必須: gradio_interface 変数
gradio_interface = gr.Interface(
    fn=my_function,
    inputs="text",
    outputs="text"
)
```

### ContBKインターフェース追加
1. **contbk** フォルダーにサブフォルダー作成
2. `gradio_interface` を持つモジュール配置
3. 自動的にContBKダッシュボードに統合

## 📈 システム拡張

### タイトルマッピング追加
```python
# mysite/routers/gradio.py の title_mapping に追加
title_mapping = {
    'my_module': '🎯 マイモジュール',
    # ... 既存のマッピング
}
```

### ダッシュボードカスタマイズ
```python
# controllers/contbk_example.py を参考に
# 新しいタブやデモインターフェースを追加
```

## 🔍 トラブルシューティング

### よくある問題
1. **ポート競合**: 別のポートを指定 (`server_port=xxxx`)
2. **モジュール未検出**: `gradio_interface` 変数の存在確認
3. **タイトル表示**: `interface_title` または title_mapping 設定

### ログ確認
```bash
# システム動作確認
python3 -c "from mysite.routers.gradio import include_gradio_interfaces; include_gradio_interfaces()"
```

## 📁 重要ファイル

- `mysite/routers/gradio.py` - メイン統合システム
- `controllers/contbk_example.py` - 統合ダッシュボード  
- `controllers/contbk_dashboard.py` - シンプル版ダッシュボード
- `controllers/README_contbk_integration.md` - 詳細ドキュメント
- `controllers/SYSTEM_STATUS_REPORT.md` - システム状況

## 🎯 次のステップ

1. **Gradioアップデート**: `pip install gradio==4.44.1`
2. **新機能追加**: ContBKフォルダーに新しいインターフェース
3. **パフォーマンス改善**: 必要に応じて最適化

---

**🎉 ContBK統合システムを活用して、美しいインターフェースで開発を加速しましょう！**
