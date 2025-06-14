import os
import subprocess
import requests
import string
import random
import shutil

def github(token, folder):
    # GitHubユーザー名とトークンを環境変数として定義
    GITHUB_USERNAME = os.getenv("github_user")
    GITHUB_TOKEN = os.getenv("github_token")

    # ランダムな文字列を生成する関数
    def generate_random_string(length=6):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    # リポジトリ名にランダムな文字列を追加
    REPO_NAME_BASE = "gpt-engeneer"
    REPO_NAME = f"{REPO_NAME_BASE}-{folder}-{generate_random_string()}"

    # controllersディレクトリのパス
    controllers_dir = "/home/user/app/controllers"

    # 指定されたフォルダーのパス
    target_dir = os.path.join(controllers_dir, folder)

    # 指定されたフォルダー内に新しい .git フォルダーを作成
    if os.path.isdir(os.path.join(target_dir, ".git")):
        shutil.rmtree(os.path.join(target_dir, ".git"))

    # GitHub APIを使ってリモートリポジトリを作成
    response = requests.post(
        "https://api.github.com/user/repos",
        auth=(GITHUB_USERNAME, GITHUB_TOKEN),
        json={"name": REPO_NAME,"public": True}
    )

    if response.status_code == 201:
        print(f"Successfully created repository {REPO_NAME}")
    else:
        print(f"Failed to create repository: {response.json()}")
        exit(1)

    # リモートリポジトリのURL (HTTPS形式)
    REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    REPO_WEB_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}"  # リポジトリのWeb URL

    # コマンドを実行するヘルパー関数
    def run_command(command, cwd=None):
        result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=cwd)
        if result.returncode != 0:
            print(f"Command failed: {command}\n{result.stderr}")
            exit(1)
        else:
            print(result.stdout)

    # 指定されたフォルダー内でローカルリポジトリを初期化してコミット
    run_command("git init", cwd=target_dir)
    run_command("git add -f .", cwd=target_dir)
    run_command('git commit -m "Initial commit"', cwd=target_dir)

    # git filter-branchの警告を無視する設定
    os.environ['FILTER_BRANCH_SQUELCH_WARNING'] = '1'

    # コミット履歴から機密情報を削除（必要に応じて修正）
    run_command("git filter-branch --force --index-filter "
                '"git rm --cached --ignore-unmatch githubs.sh" '
                "--prune-empty --tag-name-filter cat -- --all", cwd=target_dir)

    # 既存のリモートリポジトリを削除（存在する場合のみ）
    result = subprocess.run("git remote", shell=True, text=True, capture_output=True, cwd=target_dir)
    if "origin" in result.stdout:
        run_command("git remote remove origin", cwd=target_dir)

    # 新しいリモートリポジトリを追加して強制プッシュ
    run_command(f"git remote add origin {REPO_URL}", cwd=target_dir)
    run_command("git branch -M main", cwd=target_dir)
    run_command("git push -f origin main", cwd=target_dir)

    print(f"Successfully pushed to GitHub repository {REPO_NAME}")
    print(f"Repository URL: {REPO_WEB_URL}")
    return REPO_WEB_URL

# 使用例
#token = "your_github_token"
#folder = "test_folders"
#github(token, folder)
