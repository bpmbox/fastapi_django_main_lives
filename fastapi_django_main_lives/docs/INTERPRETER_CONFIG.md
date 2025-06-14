# Interpreter Process Configuration

## 修正済み: 環境に依存しない動的パス設定

### 概要
`process.py`のBASE_PATH設定が固定値だったため、異なる環境でエラーが発生していた問題を修正しました。現在は環境に応じて動的にパスを設定します。

### 自動検出される環境

1. **環境変数での設定** (最優先)
   ```bash
   export INTERPRETER_BASE_PATH="/custom/path/to/controller/"
   ```

2. **GitHub Codespaces環境**: `/workspaces/` を含むパス
   - 自動設定: `{current_dir}/app/Http/controller/`

3. **Docker環境**: `/home/user/app/` パスで実行
   - 自動設定: `/home/user/app/app/Http/controller/`

4. **ローカル開発環境**: `fastapi_django_main_live` を含むパス
   - 自動設定: `{current_dir}/app/Http/controller/`

5. **フォールバック環境**: 上記以外
   - 自動設定: `{current_dir}/temp_controller/`

### 修正内容

#### 1. 動的パス検出の実装
```python
def get_base_path():
    """環境に応じて動的にベースパスを取得"""
    # 環境変数チェック
    # 現在のディレクトリ分析
    # 適切なパス生成
    # フォールバック処理
```

#### 2. 安全な初期化
```python
# 遅延初期化でimport時エラーを回避
BASE_PATH = None

def get_base_path_safe():
    global BASE_PATH
    if BASE_PATH is None:
        BASE_PATH = get_base_path()
    return BASE_PATH
```

#### 3. 堅牢なエラーハンドリング
```python
def ensure_base_path_exists():
    # パス作成の試行
    # 書き込み権限確認
    # フォールバック処理
    # 詳細なログ出力
```

### 使用例

#### 通常の使用（自動検出）
```python
from mysite.interpreter.process import ensure_base_path_exists, get_base_path_safe

# パスの確認と作成
if ensure_base_path_exists():
    base_path = get_base_path_safe()
    print(f"Base path ready: {base_path}")
```

#### 環境変数での設定
```bash
# .env ファイルまたはシェル
export INTERPRETER_BASE_PATH="/workspace/my_project/controllers/"

# Python
from mysite.interpreter.process import get_base_path
path = get_base_path()  # 設定された環境変数を使用
```

#### Docker環境での使用
```dockerfile
ENV INTERPRETER_BASE_PATH="/app/controllers/"
```

#### Codespaces環境での使用
```json
// .devcontainer/devcontainer.json
{
  "containerEnv": {
    "INTERPRETER_BASE_PATH": "/workspaces/fastapi_django_main_live/app/Http/controller/"
  }
}
```

### トラブルシューティング

#### 権限エラーの場合
```bash
# ディレクトリを手動作成
mkdir -p /path/to/controller
chmod 755 /path/to/controller

# 環境変数設定
export INTERPRETER_BASE_PATH="/path/to/controller/"
```

#### パス確認方法
```python
from mysite.interpreter.process import get_base_path_safe
print(f"Current BASE_PATH: {get_base_path_safe()}")
```

#### 設定検証スクリプト
```bash
cd /workspaces/fastapi_django_main_live
python verify_process_fix.py
```

### ログの確認
```python
from mysite.logger import logger

# 現在のベースパスを確認
from mysite.interpreter.process import get_base_path_safe
logger.info(f"Current BASE_PATH: {get_base_path_safe()}")
```

### 既知の問題と解決策

#### 問題: ImportError
**原因**: Django設定が正しく読み込まれていない  
**解決策**: 
```python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()
```

#### 問題: 権限エラー
**原因**: ディレクトリへの書き込み権限がない  
**解決策**: 環境変数で書き込み可能なパスを指定

#### 問題: パスが見つからない
**原因**: 自動検出が失敗  
**解決策**: INTERPRETER_BASE_PATH環境変数を明示的に設定

### テスト方法

1. **基本テスト**
   ```bash
   python verify_process_fix.py
   ```

2. **Django環境でのテスト**
   ```bash
   python manage.py shell -c "from mysite.interpreter.process import get_base_path; print(get_base_path())"
   ```

3. **カスタムパステスト**
   ```bash
   export INTERPRETER_BASE_PATH="/tmp/test_path/"
   python verify_process_fix.py
   ```
